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

def freeze(bricks: List[Tuple[Any]], frozen: Tuple[Tuple[Any]]) -> Tuple[Tuple[Tuple[Any]], Tuple[Tuple[Any]]]:
    active = tuple()
    for brick in bricks:
        is_frozen = False
        bottom_z = min([unit[2] for unit in brick])
        bottom_units = [unit for unit in brick if unit[2] == bottom_z]
        if bottom_z == 1:
            is_frozen = True
        else:
            for unit in bottom_units:
                for b in frozen:
                    for u in b:
                        if unit[0] == u[0] and unit[1] == u[1] and unit[2] - 1 == u[2]:
                            is_frozen = True
        if is_frozen:
            brick = tuple((u[0], u[1], u[2], u[3], "frozen") for u in brick)
            frozen += (brick,)
        else:
            active += (brick,)
    return frozen, active


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


def drop(active: Tuple[Tuple[Any]], frozen: Tuple[Any]) -> Tuple[Any]:
    counter = 0
    while len(active) > 0:
        counter += 1
        print(f"dropping, iteration {counter}")
        dropped_active = tuple()
        for brick in active:
            new_brick = tuple()
            for unit in brick:
                new_unit = (unit[0], unit[1], unit[2]-1, unit[3], unit[4])
                new_brick += (new_unit,)
            dropped_active += (new_brick,)
        new_frozen, new_active = freeze(dropped_active, frozen) 
        active = new_active
        frozen = new_frozen
    return frozen


def disint(bricks: Tuple[Tuple[Any]]) -> int:
    disintigrable_counter = 0
    chain_reaction_counter = 0
    for i in range(len(bricks)):
        print(f"i = {i}: {i/len(bricks)}; counter {disintigrable_counter}")
        temp_pop = bricks[i]
        before = bricks[:i]
        after = bricks[i+1:]
        new_bricks = before + after
        new_frozen, new_active = freeze(new_bricks, tuple())
        print(f"len(new_frozen) = {len(new_frozen)}")
        print(f"len(new_active) = {len(new_active)}")
        if len(new_active) > 0:
            disintigrable_counter += 1
        chain_reaction_counter += len(new_active)
    return disintigrable_counter, chain_reaction_counter


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
    frozen, active = freeze(bricks, tuple())
    dropped = drop(active, frozen)
    print(f"dropped = {dropped}")
    print("dropped:")
    print_bricks(dropped, x_max, y_max, z_max)
    non_disintigrable_count, chain_reaction_count = disint(dropped)
    disintigrable_count = len(bricks) - non_disintigrable_count

    return disintigrable_count, chain_reaction_count



print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve22(f.read()[:-1]))

