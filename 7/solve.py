TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

from typing import List, Dict, Any, Tuple, Iterable
from copy import deepcopy


VAL_DICT = {
    "high_card": 1,
    "one_pair": 2,
    "two_pair": 3,
    "three_kind": 4,
    "full_house": 5,
    "four_kind": 6,
    "five_kind": 7,
}

CARD_DICT = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7, 
    "8": 8,
    "9": 9, 
    "T": 10,
    # J = 1 to solve part 2; J = 11 to solve part 1
    #"J": 11,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Card:
    def __init__(self, s: str):
        self.name = s
        self.value = CARD_DICT[s]

    def __eq__(self, other) -> bool:
        return self.value == other.value


    def __lt__(self, other) -> bool:
        return self.value < other.value


    def __hash__(self) -> str:
        return self.value

    def __str__(self):
        return f"{self.name}={self.value}"


class Cards:
    def __init__(self, l: List[str]):
        self.cards = [Card(item) for item in l]

    def __lt__(self, other):
        for i in range(len(self.cards)):
            self_val = self.cards[i]
            other_val = other.cards[i]
            #print(f"self_val = {self_val}")
            #print(f"other_val = {other_val}")
            if self_val < other_val:
                #print(f"{self_val} < {other_val}")
                return True
            elif self_val > other_val:
                #print(f"{self_val} > {other_val}")
                return False
        raise ValueError(f"Identical cards: {self} -- {other}")

    def __str__(self):
        return f"{self.cards}"
    
    def __repr__(self):
        return str(self)


class Typ:
    def __init__(self, l: List[int]):
        self.name = self._get_name(l)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return VAL_DICT[self.name] < VAL_DICT[other.name]

    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return str(self)
        

    @staticmethod
    def _get_name(l: List[str]) -> str:
        count_dict = get_count_dict(l)
        frequencies = [v for _, v in count_dict.items()]
        card_set = set(l)
        if len(card_set) == 5:
            return "high_card"
        elif len(card_set) == 2 and 4 in frequencies:
            return "four_kind"
        elif len(card_set) == 1:
            return "five_kind"
        elif len(card_set) == 3 and 3 in frequencies:
            return "three_kind"
        elif len([v for  v in frequencies if v == 2]) == 2:
            return "two_pair"
        elif max(frequencies) == 2:
            return "one_pair"
        elif len(set(l)) == 2 and 3 in frequencies:
            return "full_house"
        else:
            #print(f"type(l) = {type(l)}")
            #print(f"count_dict = {count_dict}")
            #print(f"card_set = {card_set}")
            #print(f"frequencies = {frequencies}")
            raise ValueError(str(l))

    def __str__(self):
        return str(self.name)


class Hand:

    def __init__(self, s: str, index: int):
        self.index = index
        self.raw_cards = [item for item in list(s.split()[0])]
        self.bid = int(s.split()[1])
        self.type = Typ(self.raw_cards) 
        self.cards = Cards(self.raw_cards)

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.cards == other.cards

 
    def __lt__(self, other) -> bool:
        if self.type < other.type:
            return True
        elif self.type > other.type:
            return False
        else:
            if self.cards < other.cards:
                return True
            elif self.cards > other.cards:
                return False
            else:
                raise ValueError(f"Identical hands: {self}, {other}")            
    def __str__(self):
        return f"{self.type}: {[card for card in self.raw_cards]}"

    def __repr__(self):
        return str(self)


class JokerHand(Hand):
    def __init__(self, s: str, index: int):
        super().__init__(s, index)
        has_joker = "J" in self.raw_cards
        if has_joker:
            self.best_hand = self._get_best_possible_hand()
        else:
            #print(f"self = {self}")
            self.best_hand = self
            #print(f"self.best_hand = {self.best_hand}") 

    def _get_best_possible_hand(self) -> Hand:
        print(f"self.raw_cards = {self.raw_cards}")
        all_lists = []
        get_joker_hands(self.raw_cards, all_lists,[])
        #print(f"all_lists = {all_lists}")
        for item in all_lists:
            assert "J" not in item
        possible_hands = [JokerHand(f"{''.join(item)} {self.bid}", self.index) for item in all_lists]
        #print(f"possible_hands = {possible_hands}")
        max_possible_hand = max(possible_hands)
        print(f"max_possible_hand = {max_possible_hand}")
        return max_possible_hand

    def __lt__(self, other) -> bool:
        if self.best_hand.type < other.best_hand.type:
            return True
        elif self.best_hand.type > other.best_hand.type:
            return False
        else:
            if self.cards < other.cards:
                return True
            elif self.cards > other.cards:
                return False
            else:
                raise ValueError(f"Identical hands: {self}, {other}")            
            

def get_joker_hands(l: List[str], all_lists: List[str], current_list: List[str], card_dict: Iterable[str] = CARD_DICT) -> List[str]:
    if len(l) == 0:
        all_lists += [current_list]
        return
    next_item = l[0]
    if next_item == "J":
        for card in card_dict:
            if card != "J":
                get_joker_hands(l[1:], all_lists, current_list+[card], card_dict)
    else:
        get_joker_hands(l[1:], all_lists, current_list+[next_item], card_dict)


def get_count_dict(l: Iterable[Any]) -> Dict[Any, int]:
    count_dict = {}
    for item in l:
        if item not in count_dict:
            count_dict[item] = 1
        else:
            count_dict[item] += 1
    return count_dict


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    hands = [Hand(s, i) for i, s in enumerate(cleaned_list)]
    print(f"hands = {hands}")
    sorted_hands = sorted(hands)
    print(f"sorted_hands = {sorted_hands}")
    multiplied_hands = [hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)]  
    print(f"multiplied_hands = {multiplied_hands}")
    result = sum(multiplied_hands)
    return result


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    hands = [JokerHand(s, i) for i, s in enumerate(cleaned_list)]
    print(f"hands = {hands}")
    sorted_hands = sorted(hands)
    print(f"sorted_hands = {sorted_hands}")
    multiplied_hands = [hand.bid * (i + 1) for i, hand in enumerate(sorted_hands)]  
    print(f"multiplied_hands = {multiplied_hands}")
    result = sum(multiplied_hands)
    return result


#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))


# notes 253718982 too low
