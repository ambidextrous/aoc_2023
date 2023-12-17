#--- Day 17: Clumsy Crucible ---
#The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.
#
#As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!
#
#You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.
#
#The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.
#
#To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.
#
#Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.
#
#For example:
#
TEST_INPUT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
#Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)
#
#Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.
#
#One way to minimize heat loss is this path:
#
#2>>34^>>>1323
#32v>>>35v5623
#32552456v>>54
#3446585845v52
#4546657867v>6
#14385987984v4
#44578769877v6
#36378779796v>
#465496798688v
#456467998645v
#12246868655<v
#25465488877v5
#43226746555v>
#This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.
#
#Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?
TEST_INPUT_2 = """19111
11191
99911
99919
99911"""

#--- Part Two ---
#The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.
#
#Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a straight line, but they also have trouble turning!
#
#Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.
#
#In the above example, an ultra crucible could follow this path to minimize heat loss:
#
#2>>>>>>>>1323
#32154535v5623
#32552456v4254
#34465858v5452
#45466578v>>>>
#143859879845v
#445787698776v
#363787797965v
#465496798688v
#456467998645v
#122468686556v
#254654888773v
#432267465553v
#In the above example, an ultra crucible would incur the minimum possible heat loss of 94.
#
#Here's another example:
#
#111111111111
#999999999991
#999999999991
#999999999991
#999999999991
#Sadly, an ultra crucible would need to take an unfortunate path like this one:
#
#1>>>>>>>1111
#9999999v9991
#9999999v9991
#9999999v9991
#9999999v>>>>
#This route causes the ultra crucible to incur the minimum possible heat loss of 71.
#
#Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?


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


TURN_DICT = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
    "NO_CURRENT_HEADING": "NO_CURRENT_HEADING",
}


def get_child_coord(
    x: int,
    y: int,
    h: str,
    grid: List[str]
) -> Tuple[int, int]:
    y_bound = len(grid)
    x_bound = len(grid[0])
    new_pos = ()
    if h == "N":
        y_1 = y - 1
        if y_1 >= 0:
            return (x, y_1, h)
    elif h == "S":
        y_1 = y + 1
        if y_1 < y_bound:
            return (x, y_1, h)
    elif h == "E":
        x_1 = x + 1
        if x_1 < x_bound:
            return (x_1, y, h)
    elif h == "W":
        x_1 = x - 1
        if x_1 >= 0:
            return (x_1, y, h)
    else:
        raise ValueError(f"x = {x}, y = {y}; grid:\n{grid}")
    return ()


def get_children_for_headings(
    x: int, 
    y: int, 
    permitted_headings: Tuple[str],
    grid: List[str], 
    path: List[Tuple[int, int]],
) -> Tuple[int, int, int]:
    #print(f"                 get_children_for_headings():")
    #print(f"                 permitted_headings = {permitted_headings}:")
    child_coords = ()
    for h in permitted_headings:
        child_coord = get_child_coord(x, y, h, grid)
        if len(child_coord) > 0:
            child_coords += (child_coord,)
    children = [(coords[0], coords[1], coords[2], int(grid[coords[1]][coords[0]])) for coords in child_coords]
    unvisited_children = [child for child in children if (child[0], child[1]) not in path]
    return unvisited_children
     

def get_permitted_headings(
    previous_headings: List[str],
) -> Tuple[str]:
    print(f"                 get_permitted_headings():")
    print(f"                   previous_headings = {previous_headings}:")
    current_heading = previous_headings[-1] if len(previous_headings) > 0 else "NO_CURRENT_HEADING"
    print(f"                   current_heading = {current_heading}:")
    last_three_headings = previous_headings[-3:]
    banned_heading = current_heading if len(set(last_three_headings)) == 1 and len(last_three_headings) == 3 else "NO_BANNED_HEADING"
    print(f"                   banned_heading = {banned_heading}:")
    possible = ["N", "S", "E", "W"]
    permitted = [h for h in possible if h != TURN_DICT[current_heading] and h != banned_heading]
    print(f"                   permitted = {permitted}:")
    return permitted
    

def get_children_with_heat_loss(
    heat_loss: int,
    target_heat_loss: int,
    current_pos: Tuple[int, int],
    visited: List[Tuple[int, int]], 
    path: List[Tuple[int, int]], 
    headings: List[str], 
    grid: List[str],
) -> List[Dict[str, Any]]:
    print(f"            get_children_with_heat_loss():")
    print(f"            current_pos = {current_pos}")
    x = current_pos[0]
    y = current_pos[1]
    permitted_headings = get_permitted_headings(headings)
    path_coords = [(item[0], item[1]) for item in path]
    children = get_children_for_headings(x, y, permitted_headings, grid, path_coords)
    #print(f"            children = {children}")
    filtered_children = []
    for child in children:
        new_current_pos = (child[0], child[1])
        new_heat_loss = heat_loss + child[3]
        new_path = path + [current_pos]
        new_heading = child[2]
        new_headings = headings + [new_heading] 
        if new_heat_loss == target_heat_loss:
            child_dict = {
                "current_pos": new_current_pos,
                "heat_loss": new_heat_loss,
                "path": new_path,
                "headings": new_headings
            }
            visited += [new_current_pos]
            filtered_children += [child_dict]
    return filtered_children
   

def get_neighbouring_nodes(x: int, y: int) -> Tuple[int, int]:
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
 

def is_exhausted_node(
    current_pos: Tuple[int, int],
    visited: List[Tuple[int, int]], 
    grid: List[str]
) -> Tuple[int, int]:
    x = current_pos[0]
    y = current_pos[1]
    viable_children = []
    #print(f"is_exhausted_node: ({x},{y}); visited = {visited}")
    for neighbour in get_neighbouring_nodes(x, y):
        #print(f"    neighbour = {neighbour}")
        x_1 = neighbour[0]
        y_1 = neighbour[1]
        x_bound = len(grid[0])
        y_bound = len(grid)
        is_visited = (x_1, y_1) in visited
        #print(f"    x_1 = {x_1}")
        #print(f"    y_1 = {y_1}")
        #print(f"    x_bound = {x_bound}")
        #print(f"    y_bound = {y_bound}")
        #print(f"    is_visited = {is_visited}")
        if x_1 >= 0 and y_1 >= 0 and x_1 < x_bound and y_1 < y_bound and not is_visited: 
            #print("    is not exhausted")
            return False
    #print("    is exhausted") 
    return True


def print_visited(grid: List[str], visited: List[Tuple[int,int]]) -> None:
    for y in range(len(grid)):
        l = ""
        for x in range(len(grid[0])):
            if (x, y) in visited:
                l += "#"
            else:
                l += "."
        print(l) 


def minimize(
    grid: List[str],
    current_pos: Tuple[int, int],
    target: Tuple[int, int],
    headings: List[str],
) -> int:
    start_x = current_pos[0]
    start_y = current_pos[1]
    current_heat_loss = int(grid[start_y][start_x])
    target_heat_loss = current_heat_loss
    visited = [current_pos]
    path = []
    headings = []
    start_dict = {
        "current_pos": current_pos,
        "heat_loss": current_heat_loss,
        "path": path,
        "headings": headings,
    }
    node_backlog = [start_dict]
    i = 0
    while True:
        i += 1
        target_heat_loss += 1
        print()
        print(f"i = {i}")
        print(f"current_heat_loss = {current_heat_loss}")
        print(f"target_heat_loss = {target_heat_loss}")
        print(f"node_backlog:")
        for n in node_backlog:
            print(f"     {json.dumps(n)}")
        print(f"state where target = {target_heat_loss -1}")
        print_visited(grid, visited)
        current_heat_loss += 1
        node_backlog = [node for node in node_backlog if not is_exhausted_node(node["current_pos"], visited, grid)]
        #print(f"node_backlog_filtered = {node_backlog}")
        print(f"visited = {visited}")
        #if i == 14:
        #    assert 1 == 2
        for node in node_backlog:
            children_with_target_heat_loss = get_children_with_heat_loss(node["heat_loss"], target_heat_loss, node["current_pos"], visited, node["path"], node["headings"], grid)
            print(f"    parent_node = {node}")
            #print(f"        children_with_target_heat_loss = {children_with_target_heat_loss}")
            node_backlog += children_with_target_heat_loss
            #print(f"NODE_BACKLOG = {node_backlog}")
            for n in node_backlog:
                node_pos = tuple(n["current_pos"])
                #print(f"        node_pos = {node_pos}")
                #print(f"        target = {target}")
                if tuple(n["current_pos"]) == target:
                    print(n)
                    print_visited(grid, n["path"])
                    return current_heat_loss


def dijkstra(grid: List[str], low: int, high: int) -> int:
    y_bound = len(grid)
    x_bound = len(grid[0])
    dists = defaultdict(lambda: inf)
    heap = [(0, (0, 0, (0, 1))), (0, (0, 0, (1, 0)))]

    while heap:

        print(f"heap = {heap}")
        cost, (i, j, d) = heappop(heap)
        print(f"cost = {cost}")
        print(f"i = {i}")
        print(f"j = {j}")
        print(f"d = {d}")

        if (i, j) == (y_bound -1, x_bound - 1):
            return cost

        dist = dists[i, j, d]
        print(f"dist = {dist}")
        if cost > dist:
            continue

        di, dj = d

        for ndi, ndj in ((-dj, di), (dj, -di)):
            print(f"ndi = {ndi}")
            print(f"ndj = {ndj}")
            ncost = cost 

            for dist in range(1, high + 1):
                ni = i + ndi * dist 
                nj = j + ndj * dist

                if 0 <= ni < y_bound and 0 <= nj < x_bound:
                    ncost += int(grid[ni][nj])
                     
                    if dist < low:
                        continue

                    k = (ni, nj, (ndi, ndj))

                    if ncost < dists[k]:

                        dists[k] = ncost
                        heappush(heap, (ncost, k))
    return None


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    result = dijkstra(cleaned_list, 4, 10)
    
    return result


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    result = dijkstra(cleaned_list, 1, 3)
    
    return result



print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

# TODO: re-implement minimize function to only filter out nodes if target exceeds total of highest child
