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

#--- Part Two ---
#The Elves were right to be concerned; the planned lagoon would be much too small.
#
#After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.
#
#Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
#
#So, in the above example, the hexadecimal codes can be converted into the true instructions:
#
##70c710 = R 461937
##0dc571 = D 56407
##5713f0 = R 356671
##d2c081 = D 863240
##59c680 = R 367720
##411b91 = D 266681
##8ceee2 = L 577262
##caa173 = U 829975
##1b58a2 = L 112010
##caa171 = D 829975
##7807d2 = L 491645
##a77fa3 = U 686074
##015232 = L 5411
##7a21e3 = U 500254
#Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.
#
#Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?

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
            #print(f"instruction = {instruction}")
            #print(f"pos = {pos}")
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


def parse_hex(line: str) -> Dict[str, Any]:
    color = line.split("#")[1][:-1]
    last = color[-1]
    if last == "0":
        direction = "R"
    elif last == "1":
        direction = "D"
    elif last == "2":
        direction = "L"
    elif last == "3":
        direction = "U"
    else:
        raise ValueError(f"last = {last}")
    metres = int(color[:-1],16)
    instruction = {"direction": direction, "metres": metres, "color": color}
    return instruction


def count_fill(x_min: int, y_min: int, x_max: int, y_max: int, path: Dict[Tuple[int, int], Any]) -> None:
    counter = 0
    crossing_fill_zone = False
    i = 0
    for y in range(y_min, y_max+1):
        i += 1
        for x in range(x_min, x_max+1):
            if (x, y) in path:
                if crossing_fill_zone is True:
                    crossing_fill_zone = False
                elif crossing_fill_zone is False:
                    crossing_fill_zone = True
            if crossing_fill_zone:
                counter += 1
        print(f"({x},{y}); {i/abs(y_min-y_max)}; {counter}")
    return counter


def get_vertices(instructions: List[Dict[str, Any]], start: Tuple[int, int]) -> Dict[Tuple[int, int], Any]:
    i = -1
    pos = start
    vertices = [start]
    k = 0
    while True:
        k += 1 
        i = (i + 1)  % len(instructions)
        instruction = instructions[i]
        for j in range(instruction["metres"]):
            pos = move(pos[0], pos[1], instruction["direction"])
        vertices += [pos]
        if pos == start:
            return vertices


def calculate_polygon_area(vertices: List[Tuple[int, int]]):
    """
    Calculate the area of a polygon using the Shoelace Formula.

    Parameters:
    - vertices (list of tuples): List of (x, y) coordinates representing the vertices of the polygon.

    Returns:
    float: Area of the polygon.
    """
    n = len(vertices)

    if n < 3:
        # Not enough vertices to form a polygon
        return 0.0

    # Use the Shoelace Formula to calculate the area
    area = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Wrap around for the last vertex
        area += (x1 * y2 - x2 * y1)

    area = abs(area) / 2.0

    return area

    
def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    instructions = [parse_hex(line) for line in cleaned_list]
    #instructions = [parse_instruction(line) for line in cleaned_list]
    print(f"instructions = {instructions}")
    vertices = get_vertices(instructions,(0,0))
    print(f"vertices = {vertices}")
    shoelace_area = calculate_polygon_area(vertices)
    print(f"shoelace_area = {shoelace_area}")
    path = dig_big(instructions, (0,0))
    perimeter_area = len(path)
    print(f"perimetere_area = {perimeter_area}")
    result = shoelace_area + (perimeter_area/2) + 1 
    
    return result
    


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



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

# Part 2 notes:
#len(path) = 165266734
#x_min = -4077264; y_min = -9608263; x_max = 9490626; y_max = 5072958
