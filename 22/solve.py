TEST_INPUT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

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

class Unit:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.below = None
        self.above = None

    def occupies(self, x: int, y:int, z: int) -> bool:
        return x == self.x and y == self.y and z == self.z

    def __str__(self):
        return f"Unit: ({self.x},{self.y},{self.z})"

    def __repr__(self):
        return str(self)


class Brick:
    def __init__(
        self, 
        s: str,
        num: int,
    ):
        starts = [int(item) for item in s.split("~")[0].split(",")]
        self.starts = starts
        self.num = num
        ends = [int(item) for item in s.split("~")[1].split()[0].split(",")]
        self.ends = ends
        for i in range(len(starts)):
            assert starts[i] <= ends[i], s
        units = ()
        for x in range(starts[0], ends[0]+1): 
            for y in range(starts[1], ends[1]+1):
                for z in range(starts[2], ends[2]+1):
                    unit = Unit(x,y,z)
                    units += (unit,)
        self.units = units
        self.volume = len(self.units)
        self.under = []

    def on_ground(self) -> bool:
        return any([u.z == 0 for u in self.units])

    def occupies(self, x: int, y: int, z: int) -> bool:
        return any([u.occupies(x,y,z) for u in self.units])

    def set_bricks_under(self, brick_dict: Tuple[Any]):
        under = []
        min_z = min([u.z for u in self.units])
        for u in self.units:
            for z in range(0,min_z):
                coord = (u.x, u.y, z)
                if coord in brick_dict:
                    under += [brick_dict[coord]]
        under.reverse()
        self.under = under

    def try_falling(self) -> bool:
        is_on_ground = self.on_ground()
        is_supported = any([self.is_supported_by(b) for b in self.under]) if len(self.under) > 0 else False
        if is_on_ground or is_supported:
            return False
        else:
            self.starts = (self.starts[0], self.starts[1], self.starts[2]-1)
            self.ends = (self.ends[0], self.ends[1], self.ends[2]-1)
            units = []
            for u in self.units:
                new_unit = Unit(u.x, u.y, u.z-1)
                units += [new_unit]
            self.units = units
            return True

    def is_supported_by(self, other) -> bool:
        for u in self.units:
            for u_1 in other.units:
                if u.z - u_1.z == 1:
                    return True
        return False
 
    def __str__(self):
        return f"Brick: [{self.num}] start={self.starts}; end={self.ends}; under = {[b.num for b in self.under]}; volume={self.volume}; units={self.units}"

    def __repr__(self):
        return str(self)


def get_occupation_dict(bricks: List[Brick], x_max: int, y_max: int, z_max: int) -> Dict[Tuple[int], Brick]:
    d = {}
    for x in range(x_max+1):
        for y in range(y_max+1):
            for z in range(z_max+1):
                for b in bricks:
                    if b.occupies(x, y, z):
                        d[(x,y,z)] = b
    return d
    

def print_bricks(bricks: List[Brick], x_max: int, y_max: int, z_max: int) -> None:
    print("x")
    occupation_dict = get_occupation_dict(bricks, x_max, y_max, z_max)
    for z in range(z_max,-1,-1):
        line = ""
        for x in range(0,x_max+1):
            ch = "."
            for y in range(0,z_max+1):
                if (x, y, z) in occupation_dict:
                    ch = "#"
            line += ch
        print(line + f" {z}")
    print("y")
    for z in range(z_max,-1,-1):
        line = ""
        for y in range(0,y_max+1):
            ch = "."
            for x in range(0,x_max+1):
                if (x, y, z) in occupation_dict:
                    ch = "#"
            line += ch
        print(line + f" {z}")


def get_limits(bricks: List[Brick]) -> Tuple[int]:
    x_max = 0
    y_max = 0
    z_max = 0
    for b in bricks:
        b_x = b.ends[0]
        b_y = b.ends[1]
        b_z = b.ends[2]
        if b_x > x_max:
            x_max = b_x 
        if b_y > y_max:
            y_max = b_y 
        if b_z > z_max:
            z_max = b_z 
    return x_max, y_max, z_max


def fall(bricks: List[Brick], x_max: int, y_max: int, z_max: int) -> List[Brick]:
    i = 0
    while True:
        something_fell = False
        i += 1
        for b in bricks:
            brick_fell = b.try_falling()
            if brick_fell:
                something_fell = True
        print(i)
        print_bricks(bricks, x_max, y_max, z_max)
        if something_fell is False:
            return bricks
         

def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    bricks = [Brick(l, i) for i, l in enumerate(cleaned_list)]
    print(f"bricks = {bricks}")
    x_max, y_max, z_max = get_limits(bricks)
    print(f"x_max = {x_max}, y_max = {y_max}, z_max = {z_max}")
    occupation_dict = get_occupation_dict(bricks, x_max, y_max, z_max)
    print(f"occupation_dict = {occupation_dict}")
    for b in bricks:
        print(f"    {b}")
        b.set_bricks_under(occupation_dict)
    print(f"bricks = {bricks}")
    print_bricks(bricks, x_max, y_max, z_max)
    fallen_bricks = fall(bricks, x_max, y_max, z_max)

    return result



print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve22(f.read()[:-1]))
