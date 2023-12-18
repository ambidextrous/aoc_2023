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


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
from functools import reduce
from operator import concat

sys.setrecursionlimit(100000)

MAZE = {}


def get_next_coord(x: int, y: int, h: str, char: str) -> Tuple[int, int, str]:
    if h == "E":
        if char in [".", "-"]:
            return ((x+1, y, h),)
        elif char == "\ "[:1]:
            return ((x, y+1, "S"),)
        elif char == "/":
            return ((x, y-1, "N"),)
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

@cache
#def run_maze(path: Tuple[Tuple[int, int, str]], x: int, y: int, h: str, maze: Dict[Tuple[int, int, str], Tuple[int, int, str]]) -> Tuple[Tuple[int, int]]:
def run_maze(path: Tuple[Tuple[int, int, str]], x: int, y: int, h: str, grid: Tuple[str]) -> Tuple[Tuple[int, int]]:
    maze = MAZE
    if len(path) % 1000 == 0:
        print(len(path))
        print_activated(path, grid)
        #print(f"x = {x}; y = {y}; h = {h}; path = {path}")
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
        future_path = ((x,y),(x_1, y_1)) + run_maze(path_1, x_1, y_1, h_1, grid)
        for p in future_path:
            if p not in path and p not in future_paths:
                future_paths += (p,)
    #print(f"future_paths =  {future_paths}")
    return future_paths


def run_maze_with_list(activated: List[Tuple[int,int,str]], x: int, y: int, h: str, maze: Dict[Tuple[int, int, str], Tuple[Tuple[int, int, str]]]) -> Tuple[Tuple[int, int]]:
    current_pos = (x, y, h)
    if current_pos not in activated:
        activated += [current_pos]
        next_positions = maze[current_pos]
        if len(next_positions) == 3:
            next_positions = (next_positions,)
        future_paths = ()
        for pos in next_positions:
            x_1 = pos[0]
            y_1 = pos[1]
            h_1 = pos[2]
            run_maze_with_list(activated, x_1, y_1, h_1, maze)


def print_activated(activated: Tuple[Tuple[int, int]], grid: List[str]) -> None:
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[0])):
            if (x, y) in activated or (x, y, "N") in activated or (x, y, "S") in activated or (x, y, "E") in activated or (x, y, "W") in activated:
                line += "#"
            else:
                line += "."
        print(line)


def dedup_activated(activated: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    return sorted(list(set([(item[0],item[1]) for item in activated])))


def evaluate_config(x: int, y: int, h: str, maze: Tuple[Tuple[int, int, str]]) -> int:
    activated = []
    run_maze_with_list(activated, x, y, h, maze)
    deduped = dedup_activated(activated)
    return len(deduped)


def run_configs(maze: Tuple[Tuple[int, int, str]], grid: List[str]) -> List[int]:
    scores = []
    for x in range(len(grid[0])):
        scores += [evaluate_config(x,0,"S",maze)]
        scores += [evaluate_config(x,len(grid)-1,"N",maze)]
        print(f"x = {x} {x/len(grid[0])}")
    for y in range(len(grid)):
        scores += [evaluate_config(0,y,"E",maze)]
        scores += [evaluate_config(len(grid[0])-1,y,"W",maze)]
        print(f"y = {y} {y/len(grid)}")
    return scores


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0]
    print(f"cleaned_list = {cleaned_list}")
    maze = generate_maze(cleaned_list)
    print(f"maze = {maze}")
    scores = run_configs(maze, cleaned_list)
    print(f"scores = {scores}")
    result = max(scores)

    return result



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    maze = generate_maze(cleaned_list)
    print(f"maze = {maze}")
    activated = [] 
    run_maze_with_list(activated, 0, 0, "E", maze)
    print(f"activated = {activated}")
    deduped = dedup_activated(activated)
    print(f"deduped = {deduped}")
    print_activated(deduped, cleaned_list)
    result = len(deduped)
    
    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

