#--- Day 16: The Floor Will Be Lava ---
#With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.
#
#Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.
#
#Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).
#
#The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.
#
#You note the layout of the contraption (your puzzle input). For example:
#
TEST_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
#The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:
#
#If the beam encounters empty space (.), it continues in the same direction.
#If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
#If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
#If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
#Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.
#
#In the above example, here is how the beam of light bounces around the contraption:
#
#>|<<<\....
#|v-.\^....
#.v...|->>>
#.v...v^.|.
#.v...v^...
#.v...v^..\
#.v../2\\..
#<->-/vv|..
#.|<<<2-|.\
#.v//.|.v..
#Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):
#
#######....
#.#...#....
#.#...#####
#.#...##...
#.#...##...
#.#...##...
#.#..####..
#########..
#.#######..
#.#...#.#..
#Ultimately, in this example, 46 tiles become energized.
#
#The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat

sys.setrecursionlimit(100000)


def get_next_coord(x: int, y: int, h: str, char: str) -> Tuple[int, int, str]:
    if h == "E":
        if char in [".", "-"]:
            return ((x+1, y, h),)
        elif char == "\ "[:1]:
            return ((x, y-1, "S"),)
        elif char == "/":
            return ((x, y+1, "N"),)
        elif char == "|":
            return ((x, y-1, "N"),(x, y+1, "S"),)
    elif h == "W":
        if char in [".", "-"]:
            return ((x-1, y, h),)
        elif char == "\ "[:1]:
            return ((x, y-1, "N"),)
        elif char == "/":
            return ((x, y+1, "S"),)
        elif char == "|":
            return ((x, y+1, "S"),(x, y-1, "N"),)
    elif h == "N":
        if char in [".", "|"]:
            return ((x, y-1, h),)
        elif char == "\ "[:1]:
            return ((x-1, y, "W"),)
        elif char == "/":
            return ((x+1, y, "E"),)
        elif char == "-":
            return ((x-1, y, "W"),(x+1, y, "E"),)
    elif h == "S":
        if char in [".", "|"]:
            return ((x, y+1, h),)
        elif char == "\ "[:1]:
            return ((x+1, y, "E"),)
        elif char == "/":
            return ((x-1, y, "W"),)
        elif char == "-":
            return ((x-1, y, "W"),(x+1, y, "E"),)
    else:
       raise ValueError(f"x = {x}; y = {z}; h = {h}")


def generate_maze(grid: List[str]) -> Dict[str, Tuple[int, int, str]]:
    maze = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            for h in ["E", "W", "N", "S"]:
                current = (x, y, h)
                maze[current] = tuple()
                char = grid[y][x]
                next_positions = get_next_coord(x, y, h, char)
                for pos in next_positions:
                    x_1 = pos[0]
                    y_1 = pos[1]
                    if x_1 >= 0 and x_1 < len(grid[0]) and y_1 >= 0 and y_1 < len(grid[0]):
                        maze[current] += (pos,)
    return maze 


def run_maze(path: Tuple[Tuple[int, int, str]], x: int, y: int, h: str, maze: Dict[Tuple[int, int, str], Tuple[int, int, str]]) -> Tuple[Tuple[int, int]]:
    print(f"x = {x}; y = {y}; h = {h}; path = {path}")
    current_pos = (x, y, h)
    if current_pos in path:
        return ()
    next_positions = maze[current_pos]
    if len(next_positions) == 3:
        next_positions = (next_positions,)
    future_paths = ()
    for pos in next_positions:
        x_1 = pos[0]
        y_1 = pos[1]
        h_1 = pos[2]
        path_1 = path + ((x, y, h),)
        future_path = ((x,y),) + run_maze(path_1, x_1, y_1, h_1, maze)
        for p in future_path:
            if p not in path:
                future_paths += (p,)
    print(f"future_paths =  {future_paths}")
    return future_paths


def print_activated(activated: Tuple[Tuple[int, int]], grid: List[str]) -> None:
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[0])):
            if (x, y) in activated:
                line += "#"
            else:
                line += "."
        print(line)


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    maze = generate_maze(cleaned_list)
    print(f"maze = {maze}")
    activated = run_maze((), 0, 0, "E", maze)
    print(f"activated = {activated}")
    print_activated(activated, cleaned_list)
    result = len(activated)
    print(f'maze[(9,2,"E")] = {maze[(9,2,"E")]}')
    print(f'maze[(8,2,"E")] = {maze[(8,2,"E")]}')
    

    return result



print(solve(TEST_INPUT))
        
#with open("input.txt", "rb") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

