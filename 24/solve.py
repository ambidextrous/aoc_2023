TEST_INPUT = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

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



def get_intersection_point(
    line1_point1: Tuple[int], 
    line1_point2: Tuple[int], 
    line2_point1: Tuple[int], 
    line2_point2: Tuple[int], 
) -> Tuple[float]:
    print(f"line1_point1 = {line1_point1}")

    x1, y1 = line1_point1
    x2, y2 = line1_point2
    x3, y3 = line2_point1
    x4, y4 = line2_point2

    if x2 - x1 != 0:
        m1 = (y2 - y1) / (x2 - x1)
    else:
        m1 = float("inf")

    if x4 - x3 != 0:
        m2 = (y4 - y3) / (x4 - x3)
    else:
        m2 = float("inf")

    if m1 == m2:
        return None

    if m1 == float("inf"):
        x_intersect = x1
        y_intersect = m2 * (x_intersect - x3) + y3
    elif m2 == float("inf"):
        x_intersect = x3
        y_intersect = m1 * (x_intersect - x1) + y1
    else:
        x_intersect = (m1 * x1 - m2 * x3 + y3 - y1) / (m1 - m2)
        y_intersect = m1 * (x_intersect - x1) + y1

    return x_intersect, y_intersect


def get_intersections(
    hail: Tuple[Tuple[int]], 
    hails: Tuple[Tuple[Tuple[int]]],
    lower_bound: int,
    upper_bound: int,
) -> Tuple[Tuple[int]]:
    intersections = {}
    for h in hails:
        intersection = get_intersection_point(hail[0][:2], hail[1][:2], h[0][:2], h[1][:2]) 
        is_self = h == hail 
        has_intersection = intersection is not None
        if (not is_self) and has_intersection:
            is_future_intersection_for_self = get_dist(hail[0][:2], intersection) > get_dist(hail[1][:2], intersection)
            is_future_intersection_for_other = get_dist(h[0][:2], intersection) > get_dist(h[1][:2], intersection)
            is_in_bounds = intersection[0] >= lower_bound and intersection[0] <= upper_bound and intersection[1] >= lower_bound and intersection[1] <= upper_bound
            if is_future_intersection_for_self and is_future_intersection_for_other and is_in_bounds:
                intersections[h] = intersection
    return intersections


def get_dist(point_1: Tuple[int], point_2: Tuple[int]) -> float:
    return math.dist(point_1, point_2)


def parse_hail(s: str) -> Tuple[Tuple[int], Tuple[int]]:
    position_1 = tuple(int(num) for num in s.split(" @ ")[0].split(", "))
    velocity = tuple(int(num) for num in s.split(" @ ")[1].split(", "))
    position_2 = (position_1[0] + velocity[0], position_1[1] + velocity[1], position_1[2] + velocity[2])
    return tuple([position_1, position_2, velocity])


def dedup_intersections(intersections: Dict[Tuple[Any], Tuple[Any]]) -> Tuple[Tuple[int]]:
    deduped = []
    for outer_key, outer_val in intersections.items():
        for inner_key, inner_val in outer_val.items():
            pair = tuple(sorted([inner_key[0][:2], outer_key[0][:2]]))
            if pair not in deduped:
                deduped += [pair]
    return tuple(deduped)


def parse_all_hail(s: str, num_points: int) -> Tuple[Tuple[int], Tuple[int]]:
    position_1 = tuple(int(num) for num in s.split(" @ ")[0].split(", "))
    velocity = tuple(int(num) for num in s.split(" @ ")[1].split(", "))
    positions = tuple(tuple([position_1[0] + velocity[0]*i, position_1[1] + velocity[1]*i, position_1[2] + velocity[2]*i]) for i in range(num_points))
    return tuple([positions, velocity])


def get_distances(hails: Tuple[Tuple[Tuple[int]], Tuple[int]]) -> int:
    distances_dict = {}
    num_points = len(hails)
    print(f"num_points = {num_points}")
    for i in range(1,num_points-1):
        print(f"i = {i}")
        for hail in hails:
            for other_hail in hails:
                if hail != other_hail:
                    first = hail[0][i]
                    print(f"first = {first}")
                    second = other_hail[0][i+1]
                    print(f"second = {second}")
                    dist = round(get_dist(first, second),1)
                    print(f"dist = {dist}")
                    if i == 1:
                        distances_dict[dist] = [[hail, other_hail]]
                    else:
                        if dist in distances_dict:
                            distances_dict[dist] += [[hail, other_hail]]
                    #else:
                    #    distances_dict[dist] += [[hail, other_hail]]
    return distances_dict


def get_next_point(i: int, j: int) -> int:
    sign = 1 if j >= i else -1
    diff = abs(i-j)
    return diff * sign


def get_paths(hails: Tuple[Tuple[Tuple[int]], Tuple[int]]) -> int:
    path_dict = {}
    starting_positions = [hail[0][1] for hail in hails]
    all_points = []
    for hail in hails:
        all_points += hail[0]
    all_points = set(all_points)
    print(f"all_points = {sorted(list(all_points))}")
    exploration_depth = 10
    positions_max_depth = 4
    for starting_position in starting_positions:
        #second_positions = [hail[0][2] for hail in hails if hail[0][1] != starting_position]
        for layer in range(2, positions_max_depth):
            print(f"layer = {layer} : {layer / positions_max_depth}")
            nth_positions = [hail[0][layer] for hail in hails if hail[0][1] != starting_position]
            velocities = []
            for nth_position in nth_positions:
                x_velocity = get_next_point(starting_position[0], nth_position[0])
                y_velocity = get_next_point(starting_position[1], nth_position[1])
                z_velocity = get_next_point(starting_position[2], nth_position[2])
                velocities += [tuple([x_velocity, y_velocity, z_velocity])]
            for velocity in velocities:
                current_poss = starting_position
                for i in range(exploration_depth):
                    current_poss = (current_poss[0]+velocity[0], current_poss[1]+velocity[1], current_poss[2]+velocity[2])
                    if current_poss in all_points:
                        if (starting_position, velocity) not in path_dict:
                            path_dict[(starting_position, velocity)] = [(current_poss, layer-1)]
                        else:
                            path_dict[(starting_position, velocity)] += [(current_poss, layer-1)]
    return path_dict
        

def get_score(hits: Dict[Tuple[Tuple[int]], Tuple[Tuple[int]]]) -> int:
    # hits = {((21, 14, 12), (-6, 2, 4)): [((15, 16, 16), 2), ((9, 18, 20), 2)]}
    winning_hits = 0
    winner = None
    for hit, results in hits.items():
        if len(results) > winning_hits:
            winning_hits = len(results)
            winner = hit
    intersections = hits[winner]
    first_intersection = winner[0]
    velocity = winner[1]
    factor = intersections[0][1]
    start_x = first_intersection[0] + (-1 * (velocity[0]/factor))
    start_y = first_intersection[1] + (-1 * (velocity[1]/factor))
    start_z = first_intersection[2] + (-1 * (velocity[2]/factor)) 
    return (start_x, start_y, start_z)

def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    hails = [parse_all_hail(l, 10) for l in cleaned_list]
    print(f"hails = {hails}")
    path_dict = get_paths(hails)
    print(f"path_dict = {path_dict}")
    for k, v in path_dict.items():
        print(f"    {k}: {len(v)} : {v}")
    hits = {k: v for k, v in path_dict.items() if len(v) > 1}
    print(f"hits = {hits}")
    start_pos = get_score(hits)
    print(f"start_pos = {start_pos}")
    result = sum(start_pos)

    return result


def solve(input_string: str, lower_bound: int, upper_bound: int) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    hails = [parse_hail(l) for l in cleaned_list]
    print(f"hails = {hails}")
    print(f"hails[0] = {hails[0]}")
    print(f"hails[0][0] = {hails[0][0]}")
    intersections = {hail: get_intersections(hail, hails, lower_bound, upper_bound) for hail in hails}
    print(f"intersections = {intersections}")
    deduped = dedup_intersections(intersections)
    print(f"deduped = {deduped}")
    for item in deduped:
        print(item)
    result = len(deduped)


    return result



#print(solve(TEST_INPUT,7,27))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1], 200000000000000, 400000000000000))

#print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

# Notes: 150 is too low