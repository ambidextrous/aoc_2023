TEST_INPUT = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
TEST_INPUT_2 = """.##.##....##...
.....#.#.#..#.#
.....#.#.#..#.#
.##.##....##...
..###.#.##..#.#
#.###.#.#######
##..#..###.####
##.#.#.######.#
..#.#....##..#.
..###..##......
....#...#.#...#
....#...#.#...#
..###..##.#....
..#.#....##..#.
##.#.#.######.#

##..#...#.#..#.
##.###...###..#
...#.#####....#
..##.#####....#
##.###...###..#
##..#...#.#..#.
..#..###.#####."""
TEST_INPUT_3 = """#####.###
..######.
####..###
####..###
##......#
###.##.##
..######."""

TEST_INPUT_4 = """.#.#....#
#.......#
#..#.###.
...#.#...
...#.##..
#..#.###.
#.......#
.#.#....#
##....##.
.##.###.#
.##.###.#"""


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat

sys.setrecursionlimit(100000)


def parse_grids(world: List[str]) -> List[List[str]]:
    grids = []
    new_grid = []
    for l in world:
        if l == "":
            grids += [new_grid]
            new_grid = []
        if l != "":
            new_grid += [l]
    if len(new_grid) > 0:
        grids += [new_grid]
    return grids


def get_column(grid: List[str], x: int) -> str:
    column = ""
    for y in range(len(grid)):
        column += grid[y][x]
    return column
    

def vertical_scan(grid: List[str]) -> int:
    for x in range(len(grid[0])-1):
        left_col = get_column(grid, x)
        right_col = get_column(grid, x+1)
        if left_col == right_col:
            if is_vert_mirror(grid, x-1, x+2):
                return x+1
    return None


def vertical_scan_multi(grid: List[str]) -> List[int]:
    ret_vals = []
    for x in range(len(grid[0])-1):
        left_col = get_column(grid, x)
        right_col = get_column(grid, x+1)
        if left_col == right_col:
            if is_vert_mirror(grid, x-1, x+2):
                ret_vals += [x+1]
    return ret_vals


def is_vert_mirror(grid: List[str], x_1: int, x_2: int) -> bool:
    if x_1 < 0 or x_2 >= len(grid[0]):
        return True
    col_1 = get_column(grid, x_1)
    col_2 = get_column(grid, x_2)
    if col_1 != col_2:
        return False
    return is_vert_mirror(grid, x_1-1, x_2+1) 
    

def horizontal_scan(grid: List[str]) -> int:
    for y in range(len(grid)-1):
        if grid[y] == grid[y+1]:
            if is_horiz_mirror(grid, y-1,y+2):
                return (y+1) * 100
    return None   


def horizontal_scan_multi(grid: List[str]) -> List[int]:
    ret_vals = []
    for y in range(len(grid)-1):
        if grid[y] == grid[y+1]:
            if is_horiz_mirror(grid, y-1,y+2):
                ret_vals += [(y+1) * 100]
    return ret_vals


def is_horiz_mirror(grid: List[str], y_1: int, y_2: int) -> bool:
    if y_1 < 0 or y_2 >= len(grid):
        return True
    row_1 = grid[y_1]
    row_2 = grid[y_2]
    if row_1 != row_2:
        return False
    return is_horiz_mirror(grid, y_1-1, y_2+1) 
    
     
def combine(vert: List[int], horiz: List[int]) -> List[int]:
    combined = []
    for i in range(len(vert)):
        assert not (vert[i] is not None and horiz[i] is not None)
        if vert[i] is not None:
            combined += [vert[i]]
        else:
            combined += [horiz[i]]
    return combined


def get_unsmudged_grid(grid: List[str], x: int, y: int) -> List[str]:
    val_to_flip = grid[y][x]
    flip_dict = {"#": ".", ".": "#"}
    flipped = flip_dict[val_to_flip]
    unsmudged = []
    for i in range(len(grid)):
        line = ""
        for j in range(len(grid[0])):
            if i == y and j == x:
                line += flipped
            else:
                line += grid[i][j]
        unsmudged += [line]
    return unsmudged


def get_unsmudged_grids(grid: List[str]) -> List[List[str]]:
    new_grids = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            new_grid = get_unsmudged_grid(grid, x, y)
            new_grids += [new_grid] 
    return new_grids            


def get_other(nums: List[int], old: int) -> int:
    for num in nums:
        if num is not None and num != old:
            return num
    return None


def find_unsmudged_score(grid: List[str]) -> int:
    horiz_score = horizontal_scan(grid)
    vert_score = vertical_scan(grid)
    new_grids = get_unsmudged_grids(grid)
    vert = [vertical_scan_multi(grid) for grid in new_grids]
    horiz = [horizontal_scan_multi(grid) for grid in new_grids] 
    cleaned_vert = [get_other(v, vert_score) for v in vert if len(v) > 0]
    cleaned_horiz = [get_other(h, horiz_score) for h in horiz if len(h) > 0]
    combined = sorted(list(set([item for item in cleaned_vert + cleaned_horiz if item is not None])))
    for item in combined:
        if item != horiz_score and item != vert_score:
            return item
    return combined[0]


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list] 
    print(f"cleaned_list = {cleaned_list}")
    grids = parse_grids(cleaned_list)
    print(f"grids = {grids}")
    print(f"len(grids) = {len(grids)}")
    unsmudged_scores = [find_unsmudged_score(grid) for grid in grids]
    print(f"unsmudged_scores = {unsmudged_scores}")
    result = sum(unsmudged_scores)
  
    return result

            
def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list] 
    print(f"cleaned_list = {cleaned_list}")
    grids = parse_grids(cleaned_list)
    print(f"grids = {grids}")
    print(f"len(grids) = {len(grids)}")
    vert = [vertical_scan(grid) for grid in grids]
    print(f"vert = {vert}")
    horiz = [horizontal_scan(grid) for grid in grids]
    print(f"horiz = {horiz}")
    combined = combine(vert, horiz)
    print(f"combined = {combined}")
    result = sum(combined)

    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))
#print(solve2(TEST_INPUT_2))
print(solve2(TEST_INPUT_4))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

