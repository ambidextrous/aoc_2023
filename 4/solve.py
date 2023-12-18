TEST_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
TEST_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

from typing import List, Dict, Any
from copy import deepcopy


def get_card_dict(s: str, i: int) -> Dict[str, int]:
    card_dict = {"index": i+1, "winners": [int(num) for num in s.split(":")[1].strip().split("|")[0].strip().split()], "drawn": [int(num) for num in s.split("|")[-1].strip().split()]}
    return card_dict


def get_points(card_dict: Dict[str, Any]) -> int:
    valid = [item for item in card_dict["drawn"] if item in card_dict["winners"]]
    print(f"valid = {valid}")
    if len(valid) == 0:
        return 0
    else:
        result = 1
        for _ in range(len(valid)-1):
            result *= 2
    print(result)
    return result

def get_match_count(card_dict: Dict[str, Any]) -> int:
    valid = [item for item in card_dict["drawn"] if item in card_dict["winners"]]
    return len(valid)


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    card_dicts = [get_card_dict(l, i) for i, l in enumerate(cleaned_list)]
    points = [get_points(d) for d in card_dicts]
    result = sum(points)

    return result


def count_copies(card_dicts: List[Dict[str, Any]], totals_dict: Dict[int, int]) -> List[Dict[str, Any]]:
    copies = deepcopy(card_dicts)
    for d in copies:
        recurr_counts(totals_dict, card_dicts, d["index"])


def recurr_counts(totals_dict: Dict[str, int], card_dicts: List[Dict[str, Any]], card_num: int) -> None:
    current_card = card_dicts[card_num-1]
    current_index = current_card["index"]
    if current_index not in totals_dict:
        totals_dict[current_index] = 1
    else: 
        totals_dict[current_index] += 1
    match_count = get_match_count(current_card)
    new_cards = card_dicts[current_index:current_index+match_count]
    for card in new_cards:
        recurr_counts(totals_dict, card_dicts, card["index"])


def solve_2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    card_dicts = [get_card_dict(l, i) for i, l in enumerate(cleaned_list)]
    print(f"card_dicts = {card_dicts}")
    totals_dict = {}
    count_copies(card_dicts, totals_dict)
    print(f"totals_dict = {totals_dict}")
    result = sum([val for _, val in totals_dict.items()])

    return result




#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve_2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve_2(f.read()[:-1]))
