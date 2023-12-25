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

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
  

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
        z_min = inf
        z_max = -inf
        for x in range(starts[0], ends[0]+1): 
            for y in range(starts[1], ends[1]+1):
                for z in range(starts[2], ends[2]+1):
                    if z < z_min:
                        z_min = z
                    if z > z_max:
                        z_max = z
                    unit = Unit(x,y,z)
                    units += (unit,)
        self.units = units
        self.volume = len(self.units)
        self.under = []
        self.bottom = [u for u in self.units if u.z == z_min]
        self.top = [u for u in self.units if u.z == z_max]
        self.z_min = z_min
        self.z_max = z_max
        self.is_frozen = False

    def on_ground(self) -> bool:
        return any([u.z == 0 for u in self.units])

    def occupies(self, x: int, y: int, z: int) -> bool:
        return any([u.occupies(x,y,z) for u in self.units])

    def __lt__(self, other):
        return self.z_min < other.z_min

    def set_bricks_under(self, brick_dict: Tuple[Any]):
        under = []
        min_z = min([u.z for u in self.units])
        for u in self.units:
            for z in range(0,min_z):
                coord = (u.x, u.y, z)
                if coord in brick_dict:
                    under += [brick_dict[coord]]
        under.reverse()
        self.under = list(set(under))

    def get_aboves(self, bricks: List[Any]) -> List[Any]:
        aboves = []
        for b in bricks:
            for u in self.units:
                for u_1 in b.units:
                    if b.num != self.num and u.x == u_1.x and u.y == u_1.y and u.z == u_1.z-1:
                        aboves += [b]
        return aboves

    def get_belows(self, bricks: List[Any]) -> List[Any]:
        aboves = []
        for b in bricks:
            for u in self.units:
                for u_1 in b.units:
                    if b.num != self.num and u.x == u_1.x and u.y == u_1.y and u.z == u_1.z+1:
                        aboves += [b]
        return aboves

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
        return f"Brick: [{self.num}] volume={self.volume}; top = {self.top}; bottom = {self.bottom}; units={self.units}"

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
        #print(i)
        #print_bricks(bricks, x_max, y_max, z_max)
        if something_fell is False:
            return bricks
         

def get_disints(bricks: List[Brick]) -> List[Brick]:
    disints = []
    for brick in bricks:
        print()
        print(f"brick = {brick}")
        aboves = brick.get_aboves(bricks)
        print(f"aboves = {aboves}")
        if len(aboves) == 0:
            disints += [brick]
        else:
            belows_of_aboves = [b.get_belows(bricks) for b in aboves]
            print(f"belows_of_aboves = {belows_of_aboves}")
            lengths = [len(item) for item in belows_of_aboves]
            print(f"lengths = {lengths}")
            if min(lengths) >= 2:
                disints += [brick]
        print(f"distints = {[b.num for b in disints]}")
    return disints


def clean_dict(occupation_dict: Tuple[Tuple[int], Brick], brick: Brick):
    d = deepcopy(occupation_dict)
    print([k for k in d])
    print(brick.units)
    for u in brick.units:
        d.pop((u.x, u.y, u.z))
    return d

def test_fall(bricks: List[Brick], x_max: int, y_max: int, z_max: int) -> int:
    occupation_dict = get_occupation_dict(bricks, x_max, y_max, z_max)
    count = 0
    for i in range(1,len(bricks)):
        print(f"i = {i}; {(i+1)/len(bricks)}")
        removed_brick = bricks[i]
        bs = deepcopy(bricks)
        new_bricks = bs[:i-1]+bs[i:]
        for b in new_bricks:
            b.set_bricks_under(occupation_dict)
        copied_bricks = deepcopy(new_bricks)
        fallen = fall(copied_bricks, x_max, y_max, z_max)
        new_starts = sorted([n.units for n in new_bricks])
        fallen_starts = sorted([n.units for n in fallen])
        #print(f"len(new_starts) = {len(new_starts)}")
        #print(f"new_starts = {new_starts}")
        #print(f"fallen_starts = {fallen_starts}")
        is_match = new_starts == fallen_starts
        if is_match:
            count += 1
    return count


class Floor:
    def __init__(self, x_max: int, y_max: int):
        self.x_max = x_max
        self.y_max = y_max
        self.set_zs(0)

    def raise_tile(self, x: int, y: int, z: int) -> None:
        print(f"raise_tile: x={x}; y={y}; z={z}")
        current_z = self.top[x][y].z
        if z < current_z:
            raise ValueError(f"x={x}; y={y}; z={z}; floor={floor}")
        self.top[x][y].z = z

    def set_zs(self, z: int):
        top = [Unit(x, y, z) for x in range(self.x_max+1) for y in range(self.y_max+1)]
        outter_dict = {x: {} for x in range(self.x_max+1)}
        for u in top:
            outter_dict[u.x][u.y] = u
        self.top = outter_dict
                
                
       
    def is_touched_by(self, brick: Brick) -> bool:
        for u in brick.bottom:
            print(f"u = {u}")
            print(f"self.top = {self.top}")
            u_1 = self.top[u.x][u.y]
            print(f"u_1 = {u_1}")
            if u.x == u_1.x and u.y == u_1.y and u.z == u_1.z + 1:
                return True
        return False

    def __str__(self):
        return f"Floor = {self.top}"
 
    def __repr__(self):
        return str(self)
 

def freeze(bricks: List[Brick], floor: Floor) -> Tuple[List[Brick], List[Brick], Floor]:
    frozen = []
    active = []
    floor = deepcopy(floor)
    for i, brick in enumerate(bricks):
        print(f"i = {i}")
        print(f"brick = {brick}")
        if floor.is_touched_by(brick):
            print(f"brick.units = {brick.units}")
            for u in brick.units:
                print(f"u = {u}")
                print(f"u.x = {u.x}")
                floor.raise_tile(u.x, u.y, u.z)
            frozen += [brick]
        else:
            active += [brick]
    return active, frozen, floor

    
def drop(bricks: List[Brick], floor: Floor) -> List[Brick]:
    frozen = []
    active = []


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    bricks = sorted([Brick(l, i) for i, l in enumerate(cleaned_list)])
    print(f"bricks = {bricks}")
    x_max, y_max, z_max = get_limits(bricks)
    floor = Floor(x_max, y_max) 
    print(f"floor = {floor}")
    active, frozen, floor = freeze(bricks, floor)
    print(f"active = {active}")
    print(f"len(active) = {len(active)}")
    print(f"frozen = {frozen}")
    print(f"len(frozen) = {len(frozen)}")
    print(f"floor = {floor}")


    return result



print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve22(f.read()[:-1]))

# 670 is too high
