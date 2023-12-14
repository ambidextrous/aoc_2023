#--- Day 14: Parabolic Reflector Dish ---
#You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.
#
#The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.
#
#This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.
#
#Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.
#
#In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:
#
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
#Start by tilting the lever so all of the rocks will slide north as far as they will go:
#
#OOOO.#.O..
#OO..#....#
#OO..O##..O
#O..#.OO...
#........#.
#..#....#.#
#..O..#.O.O
#..O.......
##....###..
##....#....
#You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.
#
#The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:
#
#OOOO.#.O.. 10
#OO..#....#  9
#OO..O##..O  8
#O..#.OO...  7
#........#.  6
#..#....#.#  5
#..O..#.O.O  4
#..O.......  3
##....###..  2
##....#....  1
#The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.
#
#Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

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


def score_grid(grid: List[str]) -> int:
    total = 0
    for y in range(len(grid)):
         multiplier = len(grid) - y
         score = get_O_count(grid[y])
         print(f"multiplier = {multiplier}")
         print(f"score = {score}")
         total += score * multiplier
    return total


def print_grid(grid: List[str]) -> None:
    for l in grid:
        print(l)
    print()


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



print(solve(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

