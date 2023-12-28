TEST_INPUT = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

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

sys.setrecursionlimit(10000)#0)



def get_possible_steps(lines: Tuple[str], x: int, y: int, history: Tuple[Tuple[Any]]) -> Tuple[Tuple[Any]]:
    new_start_char = lines[y][x]
    forbiden_tiles = ["#", "^", ">", "v", "<"]
    if new_start_char in forbiden_tiles:
        raise ValueError(f"Shoulded have landed on ({x},{y}): {new_start_char}")
    new_positions = tuple()
    directions = [(0,1,"N"),(1,0,"E"),(0,-1,"S"),(-1,0,"W")]
    for d in directions:
        new_x = x + d[0]
        new_y = y + d[1]
        new_direction = d[2]
        new_char = lines[new_y][new_x]
        if new_char == "#":
            new_pos = tuple()
        elif new_char == "^":
            new_pos = ((new_x,new_y,new_char),(new_x,new_y-1,lines[new_y-1][new_x]))
        elif new_char == "v":
            new_pos = ((new_x,new_y,new_char),(new_x,new_y+1,lines[new_y+1][new_x]))
        elif new_char == "<":
            new_pos = ((new_x,new_y,new_char),(new_x-1,new_y,lines[new_y][new_x-1]))
        elif new_char == ">":
            new_pos = ((new_x,new_y,new_char),(new_x+1,new_y,lines[new_y][new_x+1]))
        else:
            new_pos = ((new_x,new_y,new_char),)
        turns_back = False
        for step in new_pos:
            #print(f"step = {step}")
            if step in history:
                turns_back = True
        if turns_back is False:
            new_positions += (new_pos,)
    return [pos for pos in new_positions if len(pos) > 0]
            
       
def walk_map(lines: Tuple[str], history: Tuple[Tuple[Any]], graph: Dict[Tuple[Tuple[int]],int], target_x: int, target_y: int):
    #print(f"walk_map():")
    #print(f"    history = {history}")
    #print_history(lines, history)
    #if len(graph) > 0 and len(graph) % 100 == 0:
    #    print(f"Answers found: {len(graph)}")
    x = history[-1][0]
    y = history[-1][1]
    new_char = lines[y][x]
    if x == target_x and y == target_y:
        graph[history] = len(history)
        #print(f"{len(history)} : {history}")
        #print(f"    history = {history}")
        #print_history(lines, history)
    else:
        next_steps = get_possible_steps(lines,x,y, history)
        #print(f"    next_steps = {next_steps}")
        for step in next_steps:
            walk_map(lines, history + step, graph, target_x, target_y)
    

def print_history(lines: Tuple[str], history: Tuple[Tuple[Any]]) -> None:
    for y in range(len(lines)):
        l = ""
        for x in range(len(lines[0])):
            char = "O"
            for h in history:
                if h[0] == x and h[1] == y:
                    char = h[2]
            l += char
        print(l)


def generate_graph(lines: Tuple[str]) -> Dict[int, Tuple[int]]:
    x = 1
    y = 0
    target_x = len(lines[0])-2
    target_y = len(lines)-1
    graph = {}
    print(f"target_x = {target_x}")
    print(f"target_y = {target_y}")
    walk_map(lines, ((x,y," "),), graph, target_x, target_y)
    return graph


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    graph = generate_graph(cleaned_list)
    print(f"graph = {graph}")
    lengths = [v-1 for _, v in graph.items()]
    print(f"lengths = {lengths}")
    result = max(lengths)

    return result



#print(solve(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve22(f.read()[:-1]))

