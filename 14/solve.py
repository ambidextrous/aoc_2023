TEST_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat

sys.setrecursionlimit(100000)


@cache
def get_O_count(s: str) -> int:
    return s.count("O") 


def get_column(grid: List[str], x: int) -> str:
    col = "".join([grid[y][x] for y in range(len(grid))])
    #print(f"col = {col}")
    return col


def turn(grid: List[str]) -> List[str]:
    turned = []
    for x in range(len(grid[0])):
        col = get_column(grid, x)
        turned += [col]
    return list(reversed(turned))

turn_res = turn(["O.O","...", ".O."]) 
print(turn_res)
assert turn_res == ['O..', '..O', 'O..']


@cache
def tilt_sub(s: str) -> str:
    o_count = s.count("O")
    dot_count = s.count(".")
    result = "O"*o_count + "."*dot_count
    assert len(result) == len(s)
    return result


def tilt_line(l: str):
    new_line = ""
    sub = ""
    for char in l:
        if char == "#":
            if len(sub) > 0:
                new_line += tilt_sub(sub)
            sub = ""
            new_line += "#"
        else:
            sub += char
    if len(sub) > 0:
        new_line += tilt_sub(sub)
    assert len(new_line) == len(l)
    return new_line


def tilt_grid(grid: List[str]) -> List[str]:
    tilted_grid = [tilt_line(l) for l in grid]
    return tilted_grid

@cache
def score_grid(grid: List[str]) -> int:
    total = 0
    for y in range(len(grid)):
         multiplier = len(grid) - y
         score = get_O_count(grid[y])
         #print(f"multiplier = {multiplier}")
         #print(f"score = {score}")
         total += score * multiplier
    return total


def print_grid(grid: List[str]) -> None:
    for l in grid:
        print(l)
    print()


@cache
def cycle(grid: Tuple[str]) -> Tuple[Tuple[str]]:
    north_tilted = turn(turn(turn(tilt_grid(turn(grid)))))
    #print("north_tilted:")
    print_grid(north_tilted)
    west_tilted = tilt_grid(north_tilted)
    #print("west_tilted:")
    print_grid(west_tilted)
    south_tilted = turn(tilt_grid(turn(turn(turn(west_tilted)))))
    #print("south_tilted:")
    print_grid(south_tilted)
    east_tilted = tuple(turn(turn(tilt_grid(turn(turn(south_tilted))))))
    score = score_grid(east_tilted)
    return tuple(east_tilted), score
    

def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0]
    original_grid = tuple(cleaned_list) 
    print("original_grid:")
    print_grid(original_grid)
    n = 1000000000
    cycled_grid = deepcopy(original_grid)
    score = None
    for i in range(n):
        cycled_grid, score = cycle(cycled_grid)
        if i % 1000000 == 0:
            print(f"{i}: {i/n}: {score}")
    result = score

    return result


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    print("original_grid:")
    print_grid(cleaned_list)
    turned_grid = turn(cleaned_list)
    print("turned_grid:")
    print_grid(turned_grid)
    tilted_grid = tilt_grid(turned_grid)
    print("tilted_grid:")
    print_grid(tilted_grid)
    returned_grid = turn(turn(turn(tilted_grid)))
    print("returned_grid")
    print_grid(returned_grid)
    score = score_grid(returned_grid)
    result = score

    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

# Brute for solution finished in 17 minutes for part 2
