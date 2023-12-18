TEST_INPUT = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
TEST_INPUT_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
TEST_INPUT_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


from typing import List, Dict, Any, Tuple, Iterable
from copy import deepcopy


class Node:
    def __init__(self, s: str):
        self.name = s.split()[0]
        self.left = s.split("(")[1].split(",")[0]
        self.right = s.split(", ")[1][:-1]

    def __str__(self):
        return f"{self.name}: ({self.left}, {self.right})"

    def __repr__(self):
        return str(self)


def take_steps(node_dict: Dict[str, Node], start_pos: str, end_pos: str, directions: List[str]) -> str:
    step_counter = 0
    current_pos = start_pos
    directions_index = 0
    print(f"start_pos = {start_pos}")
    while True:
        direction = directions[directions_index]
        current_node = node_dict[current_pos]
        if current_node.name == end_pos:
            return step_counter
        if direction == "L":
            current_pos = current_node.left
        elif direction == "R":
            current_pos = current_node.right
        else:
            raise ValueError(str(direction))
        directions_index += 1
        if directions_index == len(directions):
            directions_index = 0
        step_counter += 1
        if step_counter % 10000000 == 0:
            print(f"step_counter = {step_counter}")
        #print()
        #print(f"current_node = {current_node}")
        #print(f"direction = {direction}")
        #print(f"directions_index = {directions_index}")
        #print(f"current_pos = {current_pos}")
        #print(f"step_counter = {step_counter}")
        

def take_steps_to_z(node_dict: Dict[str, Node], start_pos: str, directions: List[str]) -> str:
    step_counter = 0
    current_pos = start_pos
    directions_index = 0
    print(f"start_pos = {start_pos}")
    while True:
        direction = directions[directions_index]
        current_node = node_dict[current_pos]
        if current_node.name.endswith("Z"):
            return step_counter
        if direction == "L":
            current_pos = current_node.left
        elif direction == "R":
            current_pos = current_node.right
        else:
            raise ValueError(str(direction))
        directions_index += 1
        if directions_index == len(directions):
            directions_index = 0
        step_counter += 1
        if step_counter % 10000000 == 0:
            print(f"step_counter = {step_counter}")
        #print()
        #print(f"current_node = {current_node}")
        #print(f"direction = {direction}")
        #print(f"directions_index = {directions_index}")
        #print(f"current_pos = {current_pos}")
        #print(f"step_counter = {step_counter}")
        

def take_simultaneous_steps(node_dict: Dict[str, Node], start_positions: List[str], directions: List[str]) -> str:
    step_counter = 0
    current_positions = start_positions
    directions_index = 0
    while True:
        direction = directions[directions_index]
        current_nodes = [node_dict[pos] for pos in current_positions]
        at_end = all([node.name.endswith("Z") for node in current_nodes])
        if at_end:
            return step_counter
        if direction == "L":
            current_positions = [node.left for node in current_nodes]
        elif direction == "R":
            current_positions = [node.right for node in current_nodes]
        else:
            raise ValueError(str(direction))
        directions_index += 1
        if directions_index == len(directions):
            directions_index = 0
        step_counter += 1
        if step_counter % 100000 == 0:
            print(f"step_counter = {step_counter}")
            print(f"current_nodes = {current_nodes}")
            print(f"direction = {direction}")
            print(f"directions_index = {directions_index}")
            print(f"current_positions = {current_positions}")
            print(f"step_counter = {step_counter}")
        


def solve3(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    directions = list(cleaned_list[0])
    print(f"directions = {directions}")
    nodes = [Node(l) for l in cleaned_list[1:]]
    print(f"nodes = {nodes}")
    node_dict = {n.name: n for n in nodes}
    print(f"node_dict = {node_dict}")
    start_positions = [k for k in node_dict if k.endswith("A")]
    print(f"start_positions = {start_positions}")
    distances = [take_steps_to_z(node_dict, pos, directions) for pos in start_positions] 
    print(f"distances = {distances}")
    import math
    result = math.lcm(*distances)

    return result


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    directions = list(cleaned_list[0])
    print(f"directions = {directions}")
    nodes = [Node(l) for l in cleaned_list[1:]]
    print(f"nodes = {nodes}")
    node_dict = {n.name: n for n in nodes}
    print(f"node_dict = {node_dict}")
    start_positions = [k for k in node_dict if k.endswith("A")]
    print(f"start_positions = {start_positions}")
    step_count = take_simultaneous_steps(node_dict, start_positions, directions)
    result = step_count

    return result



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    directions = list(cleaned_list[0])
    print(f"directions = {directions}")
    nodes = [Node(l) for l in cleaned_list[1:]]
    print(f"nodes = {nodes}")
    node_dict = {n.name: n for n in nodes}
    print(f"node_dict = {node_dict}")
    step_count = take_steps(node_dict, "AAA", "ZZZ", directions)
    result = step_count

    return result



#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve3(TEST_INPUT_3))
#        
with open("input.txt", "r") as f:
    print(solve3(f.read()[:-1]))

