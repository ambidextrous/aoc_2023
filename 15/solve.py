TEST_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat

sys.setrecursionlimit(100000)


def hash_string(s: str) -> int:
    total = 0
    for char in s:
        ascii_val = ord(char)
        total += ascii_val
        total *= 17
        total = total % 256
    return total

assert hash_string("HASH") == 52


def remove_lens(instruction: str, box: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    target = instruction[:-1]
    cleaned_box = [lens for lens in box if lens[0] != target]
    return cleaned_box
    

def fill_boxes(instructions: List[str]) -> List[List[Tuple[str, int]]]:
    boxes = [[] for i in range(256)]
    for instruction in instructions:
        is_remove = instruction.endswith("-")
        label = instruction[:-1] if is_remove else instruction.split("=")[0]
        loc = hash_string(label)
        if is_remove:
            boxes[loc] = remove_lens(instruction, boxes[loc])
        else:
            boxes[loc] = adjust_box(instruction, boxes[loc])
        print()
        print(f'After "{instruction}":')
        for i in range(5):
            if len(boxes[i]) > 0:
                print(f"Box {i}: = {boxes[i]}")
    return boxes
        

def score_box(box: List[Tuple[str, int]], box_index: int) -> int:
    scores = [(box_index + 1) * (i+1) * item[1] for i, item in enumerate(box)]
    print(f"scores = {scores}")
    return sum(scores)


def adjust_box(instruction: str, box: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    target = instruction.split("=")[0]
    val = int(instruction.split("=")[1])
    target_in_box = any([item[0] == target for item in box])
    if target_in_box:
        adjusted = []
        for item in box:
            if item[0] == target:
                adjusted += [(target, val)]
            else:
                adjusted += [item]
    else:
        adjusted = box + [(target, val)]
    return adjusted


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    split = cleaned_list[0].split(",")
    print(f"split = {split}")
    boxes = fill_boxes(split)
    print(f"boxes = {boxes}")
    scores = [score_box(box, i) for i, box in enumerate(boxes)]
    print(f"scores = {scores}")
    result = sum(scores)

    return result



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    split = cleaned_list[0].split(",")
    print(f"split = {split}")
    hashes = [hash_string(s) for s in split]
    print(f"hashes = {hashes}")
    result = sum(hashes)

    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

