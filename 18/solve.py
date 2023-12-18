#--- Day 18: Lavaduct Lagoon ---
#Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.
#
#However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:
#
TEST_INPUT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
#The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.
#
#When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):
#
########
##.....#
####...#
#..#...#
#..#...#
####.###
##...#..
###..###
#.#....#
#.######
#At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:
#
########
########
########
#..#####
#..#####
########
######..
########
#.######
#.######
#Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.
#
#The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

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


def parse_instruction(line: List[str]) -> Dict[Any, Any]:
    direction = line.split()[0]
    depth = int(line.split()[1])
    color = line.split("(")[1][:-1]
    instruction = {"direction": direction, "metres": depth, "color": color}
    return instruction
    

def move(x: int, y: int, direction: str) -> Tuple[int, int]:
    if direction == "U":
        return (x, y+1)
    elif direction == "D":
        return (x, y-1)
    elif direction == "L":
        return (x-1, y)
    elif direction == "R":
        return (x+1, y)
    else:
        raise ValueError(f"x = {x}; y = {y}; direction = {direction}")


def dig(instructions: List[Dict[str, Any]], start: Tuple[int, int]) -> Dict[Tuple[int, int], Any]:
    i = -1
    pos = start
    path = {}
    while True:
        i = (i + 1)  % len(instructions) 
        instruction = instructions[i]
        for j in range(instruction["metres"]):
            pos = move(pos[0], pos[1], instruction["direction"])
            print(f"instruction = {instruction}")
            print(f"pos = {pos}")
            path[pos] = instruction
        if pos == start:
            return path

def get_limits(path: Dict[Tuple[int, int], Any]) -> Tuple[int]:
    x_min = y_min = inf
    x_max = y_max = -inf
    for x, y in path:
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y
    return x_min, y_min, x_max, y_max
   

def print_path(x_min: int, y_min: int, x_max: int, y_max: int, path: Dict[Tuple[int, int], Any]) -> None:
    for y in range(y_min, y_max+1):
        l = ""
        for x in range(x_min, x_max+1):
            if (x, y) == (0,0):
                l += "😊"
            elif (x, y) in path:
                l += "#"
            else:
                l += "."
        print(l)    


def flood(pos: Tuple[int, int], path: Dict[Tuple[int, int], Any], flooded = List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # Flood needs to start up and to the right
    x = pos[0]
    y = pos[1]
    if pos not in path and pos not in flooded:
        flooded += [pos]
        for new_pos in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]:
            flood(new_pos, path, flooded)
    
    


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    instructions = [parse_instruction(line) for line in cleaned_list]
    print(f"instructions = {instructions}")
    path = dig(instructions, (0,0))
    print(f"path = {path}")
    x_min, y_min, x_max, y_max = get_limits(path)    
    print(f"x_min = {x_min}; y_min = {y_min}; x_max = {x_max}; y_max = {y_max}")
    print_path(x_min, y_min, x_max, y_max, path)
    flooded = []
    flood_start_x = 1
    flood_start_y = -1
    flood_start_pos = (flood_start_x, flood_start_y)
    flood(flood_start_pos,path,flooded)
    print_path(x_min, y_min, x_max, y_max, flooded)
    result = len(path) + len(flooded)

    return result



print(solve(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))
