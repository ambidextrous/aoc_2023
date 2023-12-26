TEST_INPUT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat
import json
from collections import defaultdict
from heapq import heappop, heappush
from math import inf

sys.setrecursionlimit(100000)


def parse_brick(s: str, num: int) -> Tuple[Tuple[Any]]:
    start = [int(item) for item in s.split("~")[0].split(",")]
    end = [int(item) for item in s.split("~")[1].split(",")]
    brick = tuple()
    for x in range(start[0],end[0]+1):
       for y in range(start[1],end[1]+1):
           for z in range(start[2],end[2]+1):
               brick += ((x, y, z, num, "active"),)
    return brick

#def freeze(bricks: List[Tuple[Any]], x_max: int, y_max: int, z_max: int) -> Tuple[Any]:
#    frozen = []
#    for 

def get_maxes(bricks: List[Tuple[Any]]) -> Tuple[int]:
    x_max = 0
    y_max = 0
    z_max = 0
    for brick in bricks:
        for unit in brick:
            x = unit[0]
            y = unit[1]
            z = unit[2]
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if z > z_max:
                z_max = z
    return x_max, y_max, z_max


def print_bricks(bricks: Tuple[Tuple[Any]], x_max: int, y_max: int, z_max: int) -> None:
    print("y:")
    for z in range(z_max,-1,-1):
        l = ""
        for y in range(y_max+1):
            char = "."
            for x in range(x_max+1):
                for brick in bricks:
                    for unit in brick:
                        if unit[0] == x and unit[1] == y and unit[2] == z:
                            char = "#"
            l += char
        print(f"{l} : {z}")
    print("x:")
    for z in range(z_max,-1,-1):
        l = ""
        for x in range(x_max+1):
            char = "."
            for y in range(y_max+1):
                for brick in bricks:
                    for unit in brick:
                        if unit[0] == x and unit[1] == y and unit[2] == z:
                            char = "#"
            l += char
        print(f"{l} : {z}")


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    bricks = sorted([parse_brick(s, i) for i, s in enumerate(cleaned_list)], key=lambda x: min([y[2] for y in x]))
    print(f"bricks = {bricks}")
    x_max, y_max, z_max = get_maxes(bricks)
    print(f"x_max = {x_max}; y_max = {y_max}; z_max = {z_max}")
    print_bricks(bricks, x_max, y_max, z_max)


    return result



print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve22(f.read()[:-1]))

# 670 is too high
