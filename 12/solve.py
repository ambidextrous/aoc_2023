TEST_INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
from functools import cache
sys.setrecursionlimit(100000)


def parse_record(s: str) -> str:
    return s.split()[0]


def parse_schema(s: str) -> List[int]:
    return [int(item) for item in s.split()[1].split(",")]


def extract_schema(record: str, counter: int) -> List[int]:
    #print(f"record = {record}; counter = {counter}")
    if len(record) == 0:
        if counter == 0:
            return []
        else:
            return [counter]
    next_char = record[0]
    if next_char == "#":
        counter += 1
        return extract_schema(record[1:],counter)
    elif next_char == ".":
        if counter > 0:
            return [counter] + extract_schema(record[1:],0)
        else:
            return extract_schema(record[1:],0)
    else:
        raise ValueError(f"Unexpected record {record}; counter {counter}")


@cache
def extract_schema_cached(record: str, counter: int) -> Tuple[int]:
    #print(f"record = {record}; counter = {counter}")
    if len(record) == 0:
        if counter == 0:
            return tuple()
        else:
            return tuple([counter])
    next_char = record[0]
    if next_char == "#":
        counter += 1
        return tuple(extract_schema(record[1:],counter))
    elif next_char == ".":
        if counter > 0:
            return tuple([counter]) + extract_schema(record[1:],0)
        else:
            return tuple(extract_schema(record[1:],0))
    else:
        raise ValueError(f"Unexpected record {record}; counter {counter}")


def is_subschema(schema: List[str], target: List[str]) -> bool:
    #print(f"is_subschema: schema = {schema}; target = {target}")
    if len(schema) == 0:
        return True
    elif len(schema) > len(target):
        return False
    elif len(schema) == 1:
        return schema[0] <= target[0]
    else:
        if schema[0] == target[0]:
            return is_subschema(schema[1:], target[1:])
    return False


@cache
def is_subschema_cached(schema:Tuple[str], target: Tuple[str]) -> bool:
    #print(f"is_subschema: schema = {schema}; target = {target}")
    if len(schema) == 0:
        return True
    elif len(schema) > len(target):
        return False
    elif len(schema) == 1:
        return schema[0] <= target[0]
    else:
        if schema[0] == target[0]:
            return is_subschema(schema[1:], target[1:])
    return False



def get_valid_combs(record: str, state: str, target: List[int], valid_combs: List[str]) -> None:
    #print(f"record = {record}; state = {state}; target = {target}; valid_combs = {valid_combs}")
    if len(record) == 0:
        if extract_schema(state, 0) == target:
            valid_combs += [state]
    else:
        next_char = record[0]
        options = [".", "#"]
        if next_char in options:
            get_valid_combs(record[1:], state+next_char, target, valid_combs)
        elif next_char == "?":
            for option in options:
                new_state = state + option
                #print(f"new_state = {new_state}")
                schema = extract_schema(new_state, 0)
                #print(f"schema = {schema}")
                if is_subschema(schema, target):
                    get_valid_combs(record[1:], new_state, target, valid_combs)
        else:
            raise ValueError(f"Unexpected value {next_char}")
     

def get_valid_combs_count(record: str, state: str, target: List[int], valid_combs_counter: Dict[str, int]) -> None:
    #print(f"record = {record}; state = {state}; target = {target}; valid_combs = {valid_combs}")
    if len(record) == 0:
        if extract_schema(state, 0) == target:
            valid_combs_counter["count"] += 1
    else:
        next_char = record[0]
        options = [".", "#"]
        if next_char in options:
            get_valid_combs_count(record[1:], state+next_char, target, valid_combs_counter)
        elif next_char == "?":
            for option in options:
                new_state = state + option
                #print(f"new_state = {new_state}")
                schema = extract_schema(new_state, 0)
                #print(f"schema = {schema}")
                if is_subschema(schema, target):
                    get_valid_combs_count(record[1:], new_state, target, valid_combs_counter)
        else:
            raise ValueError(f"Unexpected value {next_char}")

@cache
def get_valid_combs_count_cached(record: str, state: str, target: Tuple[int]) -> int:
    #print(f"record = {record}; state = {state}; target = {target}; valid_combs = {valid_combs}")
    valid_combs_count = 0
    if len(record) == 0:
        if extract_schema_cached(state, 0) == target:
            valid_combs_count = 1
    else:
        next_char = record[0]
        options = [".", "#"]
        if next_char in options:
            valid_combs_count += get_valid_combs_count_cached(record[1:], state+next_char, target)
        elif next_char == "?":
            for option in options:
                new_state = state + option
                #print(f"new_state = {new_state}")
                schema = extract_schema_cached(new_state, 0)
                #print(f"schema = {schema}")
                if is_subschema_cached(schema, target):
                    valid_combs_count += get_valid_combs_count_cached(record[1:], new_state, target)
        else:
            raise ValueError(f"Unexpected value {next_char}")
    return valid_combs_count


def record_matches_state(record: str, state: str) -> bool:
    if len(state) > len(record):
        return False


def record_matches_state(record: str, state: str) -> bool:
    if len(state) > len(record):
        return False
    for i, token in enumerate(record):
        if i >= len(state):
            return True
        if token != "?":
            if token != state[i]:
                return False
    return True


def count_solutions(record: str, state: str, schema: List[int], counter: Dict[str, int], target: int):
    #print(f"count_solutions: record = {record}; state = {state}; schema = {schema}; counter = {counter}")
    if len(state) == len(record) and record_matches_state(record, state) and len(state.replace(".","")) == target:
        print(f"match: {record} matches {state}")
        counter["count"] += 1
    elif len(state) <= len(record):
        spaces_required = len(schema) - 1
        brokens_required = sum(schema)
        if len(state) + spaces_required + brokens_required <= len(record):
            dot_state = state + "."
            count_solutions(record, dot_state, schema, counter, target)
            if (len(state) == 0 or state[-1] == ".") and len(schema) > 0:
                break_state = state + "#"*schema[0]
                count_solutions(record, break_state, schema[1:], counter, target)


def solve3(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    records = ["?".join([parse_record(s)] * 5) for s in cleaned_list]
    #records = [parse_record(s) for i, s in enumerate(cleaned_list)]
    print(f"records = {records}")
    schemas = [parse_schema(s) * 5 for s in cleaned_list]
    #schemas = [parse_schema(s) for i, s in enumerate(cleaned_list)]
    print(f"schemas = {schemas}")
    counter = {"count": 0}
    for i in range(len(cleaned_list)):
        count_solutions(records[i],"",schemas[i],counter,sum(schemas[i]))
        print(i+1)
        print(records[i])
        print((i+1)/len(cleaned_list))
        print(counter)
    print(counter)
    result = counter["count"]
    
    return result

def solve_cached(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0]
    print(f"cleaned_list = {cleaned_list}")
    records = ["?".join([parse_record(s)] * 5) for s in cleaned_list]
    print(f"records = {records}")
    schemas = [parse_schema(s) * 5 for s in cleaned_list]
    print(f"schemas = {schemas}")
    counter = 0
    for i in range(len(cleaned_list)):
        counter += get_valid_combs_count_cached(records[i],"",tuple(schemas[i]))
        print(i+1)
        print(f"counter = {counter}")
        print(records[i])
        print((i+1)/len(cleaned_list))
        print(counter)
    print(counter)
    result = counter["count"]

    return result



def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    records = ["?".join([parse_record(s)] * 5) for s in cleaned_list]
    print(f"records = {records}")
    schemas = [parse_schema(s) * 5 for s in cleaned_list]
    print(f"schemas = {schemas}")
    counter = {"count": 0}
    for i in range(len(cleaned_list)):
        get_valid_combs_count(records[i],"",schemas[i],counter)
        print(i+1)
        print(records[i])
        print((i+1)/len(cleaned_list))
        print(counter)
    print(counter)
    result = counter["count"]
    
    return result

def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    records = [parse_record(s) for s in cleaned_list]
    print(f"records = {records}")
    schemas = [parse_schema(s) for s in cleaned_list]
    print(f"schemas = {schemas}")
    valid_combs = [[] for _ in range(len(cleaned_list))]
    for i in range(len(cleaned_list)):
        get_valid_combs(records[i],"",schemas[i],valid_combs[i])
        #print()
    print(f"valid_combs = {valid_combs}")
    valid_counts = [len(item) for item in valid_combs]
    result = sum(valid_counts)
    
    return result


@cache
def arrange(config: Tuple[int], record: str):
    print(f"config = {config}")
    print(f"record = {record}")
    if (len(record) == 0):
        a = int(sum(c == 1 for c in config) == 0)
        return a
    if sum(record) > len(config):
        return 0

   
    if config[0] == 0:
        a = arrange(config[1:], record)
        return a

    no1, no2 = 0, 0
    if config[0] == 2:
        no2 = arrange(config[1:], record)

    if all(c != 0 for c in config[:record[0]]) and (config[record[0]] if len(config) > record[0] else 0) != 1:
        no1 = arrange(config[(record[0] + 1):], record[1:])
    
    return no1 + no2


def solve_memoized(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0]
    int_conversion_dict = {".": 0, "#": 1, "?": 2}
    configs = [l.split(" ")[0] for l in cleaned_list]
    groups = [l.split(" ")[1] for l in cleaned_list]
    configs = [[int_conversion_dict[x] for x in config] for config in configs]
    configs = [((config + [2]) * 5)[:-1] for config in configs]
    groups = [[int(x) for x in group.split(",")] for group in groups]
    groups = [group*5 for group in groups]
    print(f"groups = {groups}")
    print(f"configs = {configs}")
    arrangements = [arrange(tuple(configs[i]), tuple(groups[i])) for i in range(len(cleaned_list))]
    print(f"arrangements = {arrangements}")
    return sum(arrangements)
    


#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve_memoized(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve_memoized(f.read()[:-1]))

#print(solve3(TEST_INPUT))

#with open("input.txt", "r") as f:
#    print(solve3(f.read()[:-1]))
