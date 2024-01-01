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
        if len(graph) % 100 == 0:
            print(f"Answers found: {len(graph)}")
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


def get_possible_steps2(lines: Tuple[str], x: int, y: int, history: Tuple[Tuple[Any]]) -> Tuple[Tuple[Any]]:
    new_start_char = lines[y][x]
    forbiden_tiles = ["#"]
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
        else:
            new_pos = ((new_x,new_y,new_char),)
        turns_back = False
        for step in new_pos:
            if step in history:
                turns_back = True
        if turns_back is False:
            new_positions += (new_pos,)
    return [pos for pos in new_positions if len(pos) > 0]


def get_nodes(lines: Tuple[str], target_x: int, target_y: int) -> Tuple[Tuple[int]]:
    start_x = 1
    start_y = 0
    nodes = ((start_x,start_y),)
    for y in range(len(lines)-1):
        for x in range(len(lines[0])-1):
            char = lines[y][x]
            if char == "." and not (y == target_y and x == target_x):
                neighbours = tuple()
                offsets= [(0,1),(0,-1),(1,0),(-1,0)]
                for o in offsets:
                    new_x = x + o[0]
                    new_y = y + o[1]
                    if new_x >= 0 and new_y >= 0 and new_x < len(lines[0]) and new_y < len(lines):
                        new_char = lines[new_y][new_x]
                        if new_char == ".":
                            neighbours += ((new_x,new_y),)
                if len(neighbours) > 2:
                    nodes += ((x,y),)
    return nodes + ((target_x, target_y),)


def generate_children(
    history: Tuple[Tuple[int]],
    lines: Tuple[str], 
    nodes: Tuple[Tuple[int]],
) -> Tuple[Tuple[int], int]:
    x = history[-1][0]
    y = history[-1][1]
    start_x = history[0][0]
    start_y = history[0][1]
    if (x, y) in nodes and not (x, y) == (start_x, start_y):
        new_val = (((x, y), len(history), history),)
        return new_val
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    new_coords = []
    for direction in directions:
        new_x = x + direction[0]
        new_y = y + direction[1]
        if new_x >= 0 and new_y >= 0 and new_x < len(lines[0]) and new_y < len(lines) and (new_x, new_y) not in history:
            if new_x == 140 and new_y == 140:
                new_char = "#" # Hack to fix random bug where final character of final line is deleted
            else:
                new_char = lines[new_y][new_x]
            if new_char == ".":
                new_coords += ((new_x,new_y),)
    children = tuple()
    for coord in new_coords:
        children += generate_children(history+((coord[0],coord[1]),), lines, nodes)
    return children
        


def generate_node_dict(nodes: Tuple[Tuple[int]], children_data: Tuple[Any]) -> Dict[Tuple[int], List[Tuple[int]]]:
    node_dict = {}
    for i in range(len(nodes)):
        node = nodes[i]
        node_dict[node] = []
        for sub in children_data[i]:
            node_dict[node] += ((sub[0], sub[1]),)
    return node_dict


def depth_first_search(
    graph: Dict[Tuple[int, int], List[Tuple[Tuple[int, int], int]]], 
    history: Tuple[Tuple[int], int],
    target_node: Tuple[int, int],
    longest: Dict[str, int],
):
    current_node_data = history[-1]
    current_node = current_node_data[0]
    if current_node == target_node:
        hist_total = sum([dist for _, dist in history]) - len(history) + 1
        print(f"hist_total = {hist_total}")
        if hist_total > longest["val"]:
            longest["val"] = hist_total
            longest["path"] = history
    else:
        children = [item for item in graph[current_node] if item[0] not in [h[0] for h in history]]
        for child in children:
            depth_first_search(graph, history + (child,), target_node, longest) 
    

def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","").replace(">",".").replace("v",".") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    target_x = len(cleaned_list[0])-2
    target_y = len(cleaned_list)-1
    nodes = get_nodes(cleaned_list, target_x, target_y)
    print(f"nodes = {nodes}")
    children_data = [generate_children((node,), cleaned_list, nodes) for node in nodes]
    print(f"children_data = {children_data}")
    node_dict = generate_node_dict(nodes, children_data)
    print(f"node_dict = {node_dict}")
    longest = {"val": 0, "path": None}
    depth_first_search(node_dict, ((nodes[0],0),), nodes[-1], longest)
    print(f"longest = {longest}")
    result = longest["val"]

    return result


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
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

