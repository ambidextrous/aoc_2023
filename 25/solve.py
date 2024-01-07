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
import networkx as nx
import random
from networkx.algorithms.connectivity import minimum_st_edge_cut
from igraph import Graph
from collections import defaultdict, deque


sys.setrecursionlimit(10000)#0)

def find_cut_edges(edges: Tuple[Tuple[str]], nodes: Tuple[str]) -> Tuple[str]:
    graph = nx.Graph(edges)
    # Find the cut edges (bridges) in the graph
    #min_cut_edges = list(nx.k_edge_components(graph,k=3))
    #print(f"len(min_cut_edges) = {len(min_cut_edges)}")
    #return min_cut_edges
    while True:
        edge_1 = random.choice(nodes)
        edge_2 = random.choice(nodes)
        min_cut_edges = list(minimum_st_edge_cut(graph,edge_1,edge_2))
        sorted_edges = [tuple(sorted(list(edge))) for edge in min_cut_edges]
        print(f"sorted_edges = {sorted_edges}")
        if len(sorted_edges) == 3:
            return tuple(sorted_edges)


def visualize_undirected_graph(nodes: Tuple[str], edges: Tuple[Tuple[str]]) -> None:
    # Create an undirected graph
    g = ig.Graph(directed=False)

    # Add nodes to the graph
    g.add_vertices(nodes)

    # Add edges to the graph
    g.add_edges(edges)

    # Plot the graph
    layout = g.layout("circle")
    ig.plot(g, layout=layout, bbox=(1200, 1200), vertex_label=nodes, target='part_1.pdf')
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
        if counter % 100 == 0:
            print(f"counter = {counter}")
        node_dict = generate_node_dict(nodes, config)
        group_size_dict = count_groups(nodes, node_dict)
        if len(group_size_dict) == 2:
            print(f"config = {config}")
            print(f"group_size_dict = {group_size_dict}")
            return group_size_dict[0] * group_size_dict[1]
        #print(f"group_size_dict = {group_size_dict}")


def min_unplug(nodes: Tuple[str], edges: Tuple[Tuple[str]], min_cut_edges: Tuple[Tuple[str]]) -> int:
    cleaned_edges = [edge for edge in edges if edge not in min_cut_edges]
    node_dict = generate_node_dict(nodes, cleaned_edges)
    group_size_dict = count_groups(nodes, node_dict)
    #print(f"cleaned_edges = {cleaned_edges}")
    print(f"group_size_dict = {group_size_dict}")
    return group_size_dict[0] * group_size_dict[1]


def group_by_unique_paths(data: List[str]):
    components_map = defaultdict(set)

    # mapping components to components
    for line in data:
        l, r = line.strip().split(': ')
        r = r.split(' ')
        for comp in r:
            components_map[l].add(comp)
            components_map[comp].add(l)

    group_1 = 1
    group_2 = 0

    first_comp = list(components_map.keys())[0]

    for component in list(components_map.keys())[1:]:
        connections = 0
        used_components = {first_comp}
        # Find shortest path for considered component
        # for each of starting component without repeating used components
        for s_component in components_map[first_comp]:
            if s_component == component:
                connections += 1
                continue
            qed = set()
            q = deque()
            q.append((s_component, [s_component]))
            found = False
            while q and not found and connections < 4:
                comp, path = q.popleft()
                for c in components_map[comp]:
                    if component == c:
                        connections += 1
                        used_components.update(path)
                        found = True
                        break
                    elif c not in qed and c not in path and c not in used_components:
                        q.append([c, path + [c]])
                        qed.add(c)
        # If it finds more than 3 unique ways to get to given component then it is in group 1
        if connections >= 4:
            group_1 += 1
        else:
            group_2 += 1

    return group_1 * group_2    

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
    result = group_by_unique_paths(cleaned_list)

    return result



#print(solve(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))
