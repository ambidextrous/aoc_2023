TEST_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

from typing import List, Dict, Any, Tuple, Iterable
from copy import deepcopy


def get_next_int(l: List[int]) -> int:
    if len(l) == 1:
        raise ValueError()
    if list(set(l)) == [0]:
        return 0
    next_row = []
    i = 0
    j = 1
    diff = None
    while j < len(l):
        cur = l[i]
        nex = l[j]
        # Diffs can be negative 
        diff = nex - cur
        next_row += [diff]
        i += 1
        j += 1
    return diff + get_next_int(next_row)


def get_prev_int(l: List[int]) -> int:
    if len(l) == 1:
        raise ValueError()
    if list(set(l)) == [0]:
        return 0
    next_row = []
    i = 0
    j = 1
    diff = None
    while j < len(l):
        cur = l[i]
        nex = l[j]
        # Diffs can be negative 
        diff = nex - cur
        next_row += [diff]
        i += 1
        j += 1
    c = next_row[0]
    b = get_prev_int(next_row)
    a = c - b
    print(f"next_row = {next_row}")
    print(f"a = {a}; b = {b}; c = {c}")
    return a
        

def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    split_list = [l.split() for l in cleaned_list]
    print(f"split_list = {split_list}")
    int_list = [[int(item) for item in l] for l in split_list]
    print(f"int_list = {int_list}")
    tuples_list = [(l[0], get_prev_int(l)) for l in int_list]
    print(f"tuples_list = {tuples_list}")
    prevs_list = [t[0] - t[1] for t in tuples_list]
    print(f"prevs_list = {prevs_list}")
    result = sum(prevs_list)

    return result
    

def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    split_list = [l.split() for l in cleaned_list]
    print(f"split_list = {split_list}")
    int_list = [[int(item) for item in l] for l in split_list]
    print(f"int_list = {int_list}")
    next_list = [l[-1] + get_next_int(l) for l in int_list]
    print(f"next_list = {next_list}")
    result = sum(next_list)

    return result



#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

