TEST_INPUT = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


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

OBSTRUCTIONS = None
X_LEN = None
Y_LEN = None



def parse_grid(l: List[str]) -> Tuple[Tuple[Tuple[int, int, Any]]]:
    grid = tuple()
    for x in range(len(l[0])):
        for y in range(len(l)):
            if l[y][x] == ".":
                grid += ((x, y, 0),)
            elif l[y][x] == "S":
                grid += ((x, y, 1),)
            elif l[y][x] == "#":
                grid += ((x, y, -1),)
            else:
                raise ValueError(str(l[y][x]))
    return grid


def print_grid(grid: Tuple[int]) -> None:
    grid_dict = {(item[0], item[1]) : item[2] for item in grid}
    for y in range(Y_LEN):
        l = ""
        for x in range(X_LEN):
            cur = grid_dict[(x, y)]
            if cur == 0:
                l += "."
            elif cur == 1:
                l += "O"
            else:
                l += "#"
        print(l)


@cache
def take_step(x: int, y: int) -> Tuple[int]:
    positions = tuple()
    for step in [(0,1),(0,-1),(1,0),(-1,0)]:
        pos = (x + step[0], y + step[1])
        if pos not in OBSTRUCTIONS and pos[0] >= 0 and pos[0] < X_LEN and pos[1] >= 0 and pos[1] < Y_LEN:
            positions += (pos,)
    return positions


@cache
def take_steps(grid: Tuple[Tuple[int]]) -> Tuple[int]: 
    elf_coords = set()
    for square in grid:
        x = square[0]
        y = square[1]
        content = square[2]
        if content == -1:
            continue
        elif content == 0:
            continue
        else:
            positions = take_step(x, y)
            for pos in positions:
                elf_coords.add(pos)
    new_grid = tuple()
    for square in grid:
        x = square[0]
        y = square[1]
        content = square[2]
        if content == -1:
            new_grid += ((x, y, -1),)
        elif (x, y) in elf_coords:
            new_grid += ((x, y, 1),)
        else:
            new_grid += ((x, y, 0),)
    return new_grid


@cache
def count_elves(grid: Tuple[int]) -> int:
    return len([item for item in grid if item[2] == 1])


def run_simulation(grid: Tuple[Tuple[int]], n: int) -> int:
    elf_count = None
    for i in range(n):
        print()
        grid = take_steps(grid)
        print_grid(grid)
        elf_count = count_elves(grid)
        print(f"step_count = {i+1}")
        print(f"elf_count = {elf_count}")
    return elf_count
        

def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    global X_LEN 
    global Y_LEN
    X_LEN = len(cleaned_list[0])
    Y_LEN = len(cleaned_list)
    grid = parse_grid(cleaned_list)
    global OBSTRUCTIONS
    OBSTRUCTIONS = set([(item[0], item[1]) for item in grid if item[2] == -1])
    print(f"grid = {grid}")
    print_grid(grid)
    num_steps = 6
    result = run_simulation(grid, num_steps)

    return result



print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

