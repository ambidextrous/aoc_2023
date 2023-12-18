TEST_INPUT = """.....
.S-7.
.|.|.
.L-J.
....."""
TEST_INPUT_2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
TEST_INPUT_3 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J."""
TEST_INPUT_4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
sys.setrecursionlimit(100000)


def get_start(lines: List[str]):
    x = 0
    y = 0
    for y, l in enumerate(lines):
        for x, character in enumerate(l):
            if character == "S":
                return {"x": x, "y": y}
    raise ValueError("No start point found")


def get_heading(tile: str, heading: str) -> str:
    #print(f"get_heading: tile = {tile}; heading = {heading}")
    if tile == "S":
        return "HOME"
    elif tile == "|":
        if heading == "N" or heading == "S": 
            return heading
    elif tile == "-":
        if heading == "E" or heading == "W": 
            return heading
    elif tile == "L":
        if heading == "W":
            return "N"
        elif heading == "S":
            return "E"
    elif tile == "J":
        if heading == "E":
            return "N"
        elif heading == "S":
            return "W"
    elif tile == "7":
        if heading == "N":
            return "W"
        elif heading == "E":
            return "S"
    elif tile == "F":
        if heading == "N":
            return "E"
        elif heading == "W":
            return "S"
    raise ValueError(f"tile = {tile}; heading = {heading}")


def take_step(pos: Dict[str, int], grid: List[List[str]]) -> Dict[str, Any]:
    #print(f"pos = {pos}")
    x = pos["x"]
    y = pos["y"]
    heading = pos["h"]
    counter = pos["counter"]
    if heading == "N":
        new_y = y - 1
        new_x = x
    elif heading == "S":
        new_y = y + 1
        new_x = x
    elif heading == "E":
        new_y = y
        new_x = x + 1
    elif heading == "W":
        new_y = y
        new_x = x - 1
    else:
        raise ValueError(str(f"heading = {heading}; pos = {pos}"))
    new_tile = grid[new_y][new_x]
    #print(f"new_tile = {new_tile}")
    new_heading = get_heading(new_tile, heading)
    #print(f"new_heading = {new_heading}")
    steps = pos["steps"] + [(x, y)]
    hands = pos["headings"] + [new_heading]
    new_pos = {"x": new_x, "y": new_y, "h": new_heading, "t": new_tile, "counter": counter + 1, "steps": steps, "headings": hands}
    if new_heading == "HOME":
        return new_pos
    return take_step(new_pos, grid)



def take_first_step(start: Dict[str, int], grid: List[str]) -> List[List[str]]:
    successful_trips = []
    x = start["x"]
    y = start["y"]
    steps = [(x,y)]
    try:
        next_tile = grid[y][x+1]
        east_pos = {"x": x + 1, "y": y, "h": "E", "t": next_tile, "counter": 1, "steps": steps, "headings": ["E"]}
        if next_tile in ["-", "J", "7"]:
            return take_step(east_pos, grid)
    except Exception as ex:
        print(f"East: {ex}")
    try:
        next_tile = grid[y][x-1]
        west_pos = {"x": x - 1, "y": y, "h": "W", "t": next_tile, "counter": 1, "steps": steps, "headings": ["W"]}
        if next_tile in ["-", "F", "L"]:
            return take_step(west_pos, grid)
    except Exception as ex:
        print(f"West: {ex}")
    try:
        next_tile = grid[y - 1][x]
        north_pos = {"x": x, "y": y - 1, "h": "N", "t": next_tile, "counter": 1, "steps": steps, "headings": ["N"]}
        if next_tile in ["|", "7", "F"]:
            return take_step(north_pos, grid)
    except Exception as ex:
        print(f"North: {ex}")
    try:
        next_tile = grid[y + 1][x]
        south_pos = {"x": x, "y": y + 1, "h": "S", "t": next_tile, "counter": 1, "steps": steps, "headings": ["S"]}
        if next_tile in ["|", "L", "J"]:
            return take_step(south_pos, grid)
    except Exception as ex:
        print(f"South: {ex}")
    

def get_potential_enclosed_starts(tile: str, heading: str, x: int, y: int) -> Tuple[int]:
    # Assumed handedness is left
    encloseds = None
    if heading == "S":
        if tile == "|":
            encloseds = [(x+1,y),]
        elif tile == "7":
            encloseds = [(x,y-1),(x+1,y-1),(x+1,y)]
        elif tile == "F":
            encloseds = [(x+1,y+1),]
    elif heading == "N":
        if tile == "|":
            encloseds = [(x-1,y),]
        elif tile == "L":
            encloseds = [(x,y+1),(x-1,y+1),(x-1,y)]
        elif tile == "J":
            encloseds = [(x-1,y-1),]
    elif heading == "E":
        if tile == "-":
            encloseds = [(x,y-1),]
        elif tile == "L":
            encloseds = [(x+1,y-1),]
        elif tile == "F":
            encloseds = [(x-1,y),(x-1,y-1),(x,y-1)]
    elif heading == "W":
        if tile == "-":
            encloseds = [(x,y+1),]
        elif tile == "7":
            encloseds = [(x-1,y+1),]
        elif tile == "J":
            encloseds = [(x+1,y),(x+1,y+1),(x,y+1)]
    if encloseds is None:
        raise ValueError(f"Error in get_potential_enclosed_starts: tile = {tile}; heading = {heading}; x = {x}; y = {y}")
    return encloseds


def enclose(x: int, y: int, grid: List[str], path: Set[Tuple[int]], encloseds: List[Tuple[int]]) -> Set[Tuple[int]]:
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        #raise ValueError(f"Gone off grid at ({x},{y}): searching wrong side!")
        #print(f"Gone off grid at ({x},{y}): searching wrong side!")
        pass
    elif (x, y) not in path and (x, y) not in encloseds:
        new_enclosed = (x, y)
        #print(f"new_enclosed = {new_enclosed}")
        #encloseds = encloseds.union(set([(x,y),]))
        encloseds += [new_enclosed]
        moves = [-1,0,1]
        for i in moves: 
            for j in moves:
                if not (i == 0 and j == 0):
                    new_x = x+i 
                    new_y = y+j 
                    enclose(new_x, new_y, grid, path, encloseds)


def get_encloseds(path: List[Tuple[int]], headings: List[str],  grid: List[str]) -> List[Tuple[int]]:
    path_set = set(path)
    encloseds = []
    for i in range(1, len(path)):
         #print()
         #print(str(i))
         #print(f"encloseds = {encloseds}")
         coords = path[i]
         #print(f"coords = {coords}")
         x = coords[0]
         y = coords[1]
         tile = grid[y][x]
         #print(f"tile = {tile}")
         heading = headings[i-1]
         #print(f"heading = {heading}")
         potential_enclosed_starts = get_potential_enclosed_starts(tile,heading,x,y)  
         for pot in potential_enclosed_starts:
             enclose(pot[0], pot[1], grid, path, encloseds)
    return encloseds


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    start = get_start(cleaned_list)
    print(f"start = {start}")
    step_dict = take_first_step(start, cleaned_list)
    #print(f"step_dict = {step_dict}")
    path = step_dict["steps"]
    #print(f"path = {path}")
    path_size = len(path)
    #print(f"path_size = {path_size}")
    headings = step_dict["headings"]
    #print(f"headings = {headings}")
    encloseds = get_encloseds(path, headings, cleaned_list)
    #print(f"encloseds = {encloseds}")
    grid_size = len(cleaned_list) * len(cleaned_list[0])
    #print(f"grid_size = {grid_size}")
    non_enclosed_count = grid_size - path_size - len(encloseds)
    
    result_dict = {"grid_size": grid_size, "encloseds": len(encloseds), "path_size": path_size, "non_encloseds": non_enclosed_count}

    return result_dict



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    start = get_start(cleaned_list)
    print(f"start = {start}")
    step_dict = take_first_step(start, cleaned_list)
    print(f"step_dict = {step_dict}")

    result = math.ceil(step_dict["counter"]/2)
    
    return result



#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))
#print(solve2(TEST_INPUT_2))
#print(solve2(TEST_INPUT_3))
print(solve2(TEST_INPUT_4))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

# Note for part 2, answer will either be encloseds or non_encloseds - haven't implemented an algorthim to work out which it is

