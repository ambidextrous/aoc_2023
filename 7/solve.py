#--- Day 7: Camel Cards ---
#Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.
#
#"Did you bring the parts?"
#
#You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.
#
#"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.
#
#"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.
#
#After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.
#
#You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.
#
#Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.
#
#In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
#
#Every hand is exactly one type. From strongest to weakest, they are:
#
#Five of a kind, where all five cards have the same label: AAAAA
#Four of a kind, where four cards have the same label and one card has a different label: AA8AA
#Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
#Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
#Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
#One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
#High card, where all cards' labels are distinct: 23456
#Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.
#
#If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.
#
#So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).
#
#To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:
#
TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
#This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.
#
#So, the first step is to put the hands in order of strength:
#
#32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
#KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
#T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
#Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.
#
#Find the rank of every hand in your set. What are the total winnings?

#--- Part Two ---
#To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.
#
#To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
#
#J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.
#
#Now, the above example goes very differently:
#
TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
#32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
#KK677 is now the only two pair, making it the second-weakest hand.
#T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
#With the new joker rule, the total winnings in this example are 5905.
#
#Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
#

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
