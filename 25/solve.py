TEST_INPUT = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
import itertools
from functools import cache
from functools import reduce
from operator import concat
import json
from collections import defaultdict
from heapq import heappop, heappush
from math import inf
import sympy as sp
from typing import Tuple
import igraph as ig
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)#0)


def visualize_undirected_graph(nodes: Tuple[str], edges: Tuple[Tuple[str]]) -> None:
    # Create an undirected graph
    g = ig.Graph(directed=False)

    # Add nodes to the graph
    g.add_vertices(nodes)

    # Add edges to the graph
    g.add_edges(edges)

    # Plot the graph
    layout = g.layout("circle")
    ig.plot(g, layout=layout, bbox=(900, 900), vertex_label=nodes, target='part_1.pdf')
    #plt.show()


def parse_nodes(lines: List[str]) -> Tuple[str]:
    nodes = []
    for line in lines:
        cleaned_line = line.replace(":","").split()
        nodes += cleaned_line
    return tuple(sorted(list(set(nodes))))


def parse_edges(lines: List[str]) -> Tuple[str]:
    edges = []
    for line in lines:
        parent = line.split(": ")[0]
        children = line.split(": ")[1].split()
        for child in children:
            edge = tuple(sorted([parent, child]))
            edges += [edge]
    return tuple(sorted(list(set(edges))))


def get_children(node: str, edges: Tuple[Tuple[str]]) -> Tuple[str]:
    relevant_edges = [edge for edge in edges if edge[0] == node or edge[1] == node]

    def get_child(node: str, edge: Tuple[str]) -> str:
        for item in edge:
            if item != node:
                return item

    children = [get_child(node, edge) for edge in relevant_edges]

    return tuple(sorted(list(set(children))))


def generate_node_dict(nodes: Tuple[str], edges: Tuple[Tuple[str]]) -> Dict[str, Tuple[str]]:
    node_dict = {node: get_children(node, edges) for node in nodes}
    return node_dict


def count_groups(nodes: str, node_dict: Dict[str, Tuple[str]]) -> int:
    group_size_dict = {0: 0}
    visited = set()
    group_count = 0
    node = nodes[0]
    node_set = set(nodes)
    node = node_set.pop()
    backlog = set()
    while True:
        visited.add(node)
        #print(f"node = {node}")
        group_size_dict[group_count] += 1
        children = node_dict[node]
        backlog = backlog.union(children).difference(visited)
        if len(backlog) == 0:
            node_set = node_set.difference(visited)
            if len(node_set) == 0:
                return group_size_dict
            else:
                node = node_set.pop()
            group_count += 1
            #print(f"group_count = {group_count}")
            group_size_dict[group_count] = 0
        else:
            node = backlog.pop()


def unplug(nodes: Tuple[str], edges: Tuple[Tuple[str]]) -> int:
    configuations = itertools.combinations(edges, len(edges) - 3)
    counter = 0
    for config in configuations:
        counter += 1
        if counter % 1000 == 0:
            print(f"counter = {counter}")
        node_dict = generate_node_dict(nodes, config)
        group_size_dict = count_groups(nodes, node_dict)
        if len(group_size_dict) == 2:
            print(f"config = {config}")
            print(f"group_size_dict = {group_size_dict}")
            return group_size_dict[0] * group_size_dict[1]
        #print(f"group_size_dict = {group_size_dict}")



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    nodes = parse_nodes(cleaned_list)
    print(f"nodes = {nodes}")
    edges = parse_edges(cleaned_list)
    print(f"edges = {edges}")
    visualize_undirected_graph(nodes, edges)
    result = unplug(nodes, edges)

    return result



print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))
