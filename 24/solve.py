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
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1], 200000000000000, 400000000000000))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

# Notes: 150 is too low