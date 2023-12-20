TEST_INPUT = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
TEST_INPUT_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
output -> output"""


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


class OutputNode:
   def __init__(self, name: str, destinations: Tuple[str]):
       self.name = name
       self.type = "output"
       self.destinations = destinations
       self.state = "out"

   def __repr__(self):
       return str(self)

   def __str__(self):
       return f"OutputNode : {self.name}; {self.type}; {self.destinations}; {self.state}"

   def receive(self, sender: str, pulse: str) -> Tuple[Tuple[str, str]]:
       return ()


class BroadcasterNode:
   def __init__(self, name: str, destinations: Tuple[str]):
       self.name = name
       self.type = "broadcaster"
       self.destinations = destinations
       self.state = "broad"

   def __repr__(self):
       return str(self)

   def __str__(self):
       return f"BroacasterNode : {self.name}; {self.type}; {self.destinations}; {self.state}"

   def receive(self, sender: str, pulse: str) -> Tuple[Tuple[str, str]]:
       outputs = tuple()
       for d in self.destinations:
           outputs += ((d, "low", self.name),)
       for o in outputs:
           print(f"{self.name} -{o[1]}-> {o[0]}")
       return outputs


class ConjunctionNode:
   def __init__(self, name: str, destinations: Tuple[str]):
       self.name = name
       self.type = "conjunction"
       self.destinations = destinations
       self.state = "flip"
       self.received = []
       self.input_nodes = {}
       self.sent = []

   def __repr__(self):
       return str(self)

   def __str__(self):
       return f"ConjunctionNode : {self.name}; {self.type}; {self.destinations}; {self.state}; input_nodes = {self.input_nodes}"

   def add_input(self, input_name: str):
       self.input_nodes[input_name] = "low"

   def get_output_pulse(self) -> str:
       if all([val == "high" for k, val in self.input_nodes.items()]):
           return "low"
       else:
           return "high"

   def receive(self, sender: str, pulse: str) -> Tuple[Tuple[str, str]]:
       #print(f"CN : receive() : sender = {sender}; pulse = {pulse}")
       if sender not in self.input_nodes:
           raise ValueError(f"Recieved input from unexpected sender {sender}: {self.input_nodes}")
       else:
           self.input_nodes[sender] = pulse
           outputs = tuple()
           for d in self.destinations:
               pulse = self.get_output_pulse()
               output = (d, pulse, self.name)
               self.sent += output
               outputs += (output,)
           for o in outputs:
               print(f"{self.name} -{o[1]}-> {o[0]}")
           return outputs
       

class FlipFlopNode:
   def __init__(self, name: str, destinations: Tuple[str]):
       self.name = name
       self.type = "flipflop"
       self.destinations = destinations
       self.received = []
       self.state = "off"
       self.memory = tuple()

   def receive(self, sender: str, pulse: str) -> Tuple[Tuple[str, str]]:
       if pulse == "high":
           return tuple()
       elif pulse == "low":
           if self.state == "off":
               self.state = "on"
               outputs = tuple([(d, "high", self.name) for d in self.destinations])
               self.memory += outputs
               for o in outputs:
                   print(f"{self.name} -{o[1]}-> {o[0]}")
               return outputs
           elif self.state == "on":
               self.state = "off"
               outputs = tuple([(d, "low", self.name) for d in self.destinations])
               self.memory += outputs
               for o in outputs:
                   print(f"{self.name} -{o[1]}-> {o[0]}")
               return outputs
           else:
               raise ValueError(f"pulse = {pulse}; state = {self.state}")
       else:
           raise ValueError(f"pulse = {pulse}; state = {self.state}")
 
   def __repr__(self):
       return str(self)

   def __str__(self):
       return f"FlipFlopNode : {self.name}; {self.type}; {self.destinations}; {self.state}"
   

def parse_nodes(lines: List[str]) -> Dict[str, Any]:
    nodes = {}
    print(f"lines = {lines}")
    for l in lines:
        #print(f"l = {l}")
        raw_name = l.split()[0]
        #print(f"raw_name = {raw_name}")
        destinations = tuple(l.split(" -> ")[1].split(", "))
        if raw_name == "broadcaster":
             name = raw_name
             node = BroadcasterNode("broadcaster", destinations)
        elif raw_name == "output":
             name = raw_name
             node = OutputNode("output", destinations)
        elif raw_name[0] == "%":
             name = raw_name[1:]
             node = FlipFlopNode(name, destinations)
        elif raw_name[0] == "&":
             name = raw_name[1:]
             node = ConjunctionNode(name, destinations)
        else: 
             raise ValueError(f"{name}; {destinations}")
        nodes[name] = node
    print(f"nodes:")
    for n, v in nodes.items():
        print(f"    {n} : {v}")
    for name, node in nodes.items():
        for destination in node.destinations:
             destination_node = nodes[destination]
             if destination_node.type == "conjunction":
                  destination_node.add_input(name)
    print(f"nodes with destinations = {nodes}")
    for n, v in nodes.items():
        print(f"    {n} : {v}")
    return nodes


def run_nodes(nodes: Dict[str, Any]) -> Tuple[Dict[str, Any], Tuple[int, int]]:
    history = (("broadcaster", "low", "button"),)
    #history = tuple()
    backlog = [("broadcaster", "low", "button")]
    print(f"button -low-> broadcaster")
    while len(backlog) > 0:
        nex = backlog.pop(0) 
        result = nodes[nex[0]].receive(nex[2], nex[1])
        print(f"result = {result}")
        history += result
        print(f"history = {history}")
        backlog = backlog + list(result)
    return nodes, history


def count_highs_and_lows(history: Tuple[Tuple[str]]) -> Tuple[int, int]:
    highs = 0
    lows = 0
    for h in history:
        if h[1] == "high":
            highs += 1
        elif h[1] == "low":
            lows += 1
        else:
            raise ValueError(str(history))
    return highs, lows


def make_runs(nodes: Dict[str, Any], n_runs: int) -> Tuple[Tuple[str]]:
    histories = []
    for i in range(n_runs):
        print()
        nodes, history = run_nodes(nodes)
        print(f"history = {history}")
        histories += [history]
    return histories
 

def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l for l in raw_list]
    cleaned_list = [item.replace("\n","") for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    nodes = parse_nodes(cleaned_list)
    print(f"nodes = {nodes}")
    n_runs = 1000
    histories = make_runs(nodes, n_runs)
    #print(f"histories = {histories}")
    highs_and_lows = [count_highs_and_lows(history) for history in histories]
    #print(f"highs_and_lows = {highs_and_lows}")
    high_count = sum([item[0] for item in highs_and_lows])
    print(f"high_count = {high_count}")
    low_count = sum([item[1] for item in highs_and_lows])
    print(f"low_count = {low_count}")
    result = high_count * low_count

    return result



print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve2(f.read()[:-1]))

