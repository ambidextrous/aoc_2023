#--- Day 13: Point of Incidence ---
#With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.
#
#There's just one problem: you don't see any lava.
#
#You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?
#
#As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.
#
#You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!
#
#For example:
#
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
#To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.
#
#In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:
#
#123456789
#    ><   
##.##..##.
#..#.##.#.
###......#
###......#
#..#.##.#.
#..##..##.
##.#.##.#.
#    ><   
#123456789
#In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.
#
#The second pattern reflects across a horizontal line instead:
#
#1 #...##..# 1
#2 #....#..# 2
#3 ..##..### 3
#4v#####.##.v4
#5^#####.##.^5
#6 ..##..### 6
#7 #....#..# 7
#This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.
#
#To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.
#
#Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
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

#--- Part Two ---
#You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.
#
#Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.
#
#In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)
#
#Here's the above example again:
#
##.##..##.
#..#.##.#.
###......#
###......#
#..#.##.#.
#..##..##.
##.#.##.#.
#
##...##..#
##....#..#
#..##..###
######.##.
######.##.
#..##..###
##....#..#
#The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:
#
#1 ..##..##. 1
#2 ..#.##.#. 2
#3v##......#v3
#4^##......#^4
#5 ..#.##.#. 5
#6 ..##..##. 6
#7 #.#.##.#. 7
#With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.
#
#In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:
#
#1v#...##..#v1
#2^#...##..#^2
#3 ..##..### 3
#4 #####.##. 4
#5 #####.##. 5
#6 ..##..### 6
#7 #....#..# 7
#Now, the pattern has a different horizontal line of reflection between rows 1 and 2.
#
#Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.
#
#In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?
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

