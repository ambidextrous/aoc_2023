TEST_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

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


WORKFLOWS = {}
XMAS = {"x": 0, "m": 1, "a": 2, "s": 3}


def parse_part(s: str) -> Tuple[int]:
    x = int(s.split("x=")[1].split(",")[0])
    m = int(s.split("m=")[1].split(",")[0])
    a = int(s.split("a=")[1].split(",")[0])
    s = int(s.split("s=")[1].split("}")[0])
    return (x,m,a,s)


def generate_workflows_dict(raw: List[str]) -> Dict[str, Tuple[str]]:
    workflows = {}
    for l in raw:
        key = l.split("{")[0]
        val = tuple(l.split("{")[1][:-1].split(","))
        workflows[key] = val
    return workflows


@cache
def run_sub_flow(part: str, sub_flow: str) -> Any:
    if sub_flow == "R":
        return "R"
    elif sub_flow == "A":
        return "A"
    elif ">" in sub_flow:
        new_destination = sub_flow.split(":")[1]
        index = XMAS[sub_flow[0]]
        target = int(sub_flow.split(">")[1].split(":")[0])
        if part[index] > target:
            return new_destination
        else:
            return "NO_MATCH"
    elif "<" in sub_flow:
        new_destination = sub_flow.split(":")[1]
        index = XMAS[sub_flow[0]]
        target = int(sub_flow.split("<")[1].split(":")[0])
        if part[index] < target:
            return new_destination
        else:
            return "NO_MATCH"
    else:
        return sub_flow
        #raise ValueError(f"part: {part}; sub_flow: {sub_flow}")
        


@cache
def sort_part(part: Tuple[int], workflow: str) -> int:
    workflow = WORKFLOWS[workflow]
    for sub_flow in workflow:
        result = run_sub_flow(part, sub_flow)
        if result == "R":
            return 0
        elif result == "A":
            return part[0] + part[1] + part[2] + part[3]
        elif result == "NO_MATCH":
            continue
        else:
            return sort_part(part, result)


def calculate_valid_size(d: Dict[str, int], valids: List[int]) -> int:
    #print(f"calculate_valid_size: limit_dict = {limit_dict}; valids = {valids}")
    total = 1
    x =  d["x_max"] - d["x_min"] + 1
    m =  d["m_max"] - d["m_min"] + 1
    a =  d["a_max"] - d["a_min"] + 1
    s =  d["s_max"] - d["s_min"] + 1
    print()
    print(f"d = {d}")
    print(f"x = {x}")
    print(f"m = {m}")
    print(f"a = {a}")
    print(f"s = {s}")
    total *= x
    total *= m
    total *= a
    total *= s
    print(f"total = {total}")
    valids += [total]


def update_limits(sub_flow: str, limit_dict: Dict[str, int]) -> Tuple[str, Dict[str, int]]:
    pass_limit_dict = deepcopy(limit_dict)
    fail_limit_dict = deepcopy(limit_dict)
    if sub_flow == "R":
        return "R", pass_limit_dict, fail_limit_dict
    elif sub_flow == "A":
        return "A", pass_limit_dict, fail_limit_dict
    elif ">" in sub_flow:
        new_destination = sub_flow.split(":")[1]
        letter = sub_flow[0]
        target = int(sub_flow.split(">")[1].split(":")[0])
        pass_limit_dict[f"{letter}_min"] = target + 1
        fail_limit_dict[f"{letter}_max"] = target 
        return new_destination, pass_limit_dict, fail_limit_dict
    elif "<" in sub_flow:
        new_destination = sub_flow.split(":")[1]
        letter = sub_flow[0]
        target = int(sub_flow.split("<")[1].split(":")[0])
        pass_limit_dict[f"{letter}_max"] = target - 1
        fail_limit_dict[f"{letter}_min"] = target 
        return new_destination, pass_limit_dict, fail_limit_dict
    else:
        return sub_flow, pass_limit_dict, fail_limit_dict


def slice_possibilities(workflow: str, limit_dict: Dict[str, int], valids: List[int], trail: Tuple[str]) -> None:
    print()
    print(f"slice_possibilites:")
    print(f"trail = {trail}")
    print(f"workflow = {workflow}")
    print(f"limit_dict = {limit_dict}")
    workflow = WORKFLOWS[workflow]
    for sub_flow in workflow:
        result, new_limit_dict, limit_dict = update_limits(sub_flow, limit_dict)
        if result == "R":
            continue
        elif result == "A":
            calculate_valid_size(new_limit_dict, valids)
        elif result == "NO_MATCH":
            continue
        else:
            new_trail = trail + (result,)
            slice_possibilities(result, new_limit_dict, valids, new_trail)


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0]
    print(f"cleaned_list = {cleaned_list}")
    workflows_dict = generate_workflows_dict([l for l in cleaned_list if l[0] != "{"])
    global WORKFLOWS
    WORKFLOWS = workflows_dict
    print(f"WORKFLOWS = {WORKFLOWS}")
    limit_dict = {}
    for l in ["x", "m", "a", "s"]:
        limit_dict[f"{l}_min"] = 1
        limit_dict[f"{l}_max"] = 4000
    print(f"limit_dict = {limit_dict}")
    valids = []
    slice_possibilities("in", limit_dict, valids, ("in",))
    print(f"valids = {valids}")
    result = sum(valids)

    return result


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    workflows_dict = generate_workflows_dict([l for l in cleaned_list if l[0] != "{"])
    global WORKFLOWS
    WORKFLOWS = workflows_dict
    print(f"WORKFLOWS = {WORKFLOWS}")
    parts = [parse_part(l) for l in cleaned_list if l[0] == "{"]
    print(f"parts = {parts}")
    sorted_parts = [sort_part(part, "in") for part in parts]
    print(f"sorted_parts = {sorted_parts}")
    result = sum(sorted_parts)

    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

