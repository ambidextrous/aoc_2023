TEST_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


from typing import List, Dict, Any, Tuple
from copy import deepcopy


def parse_source_dest(s: str) -> Tuple[str, str]:
    source = s.split("-")[0]
    dest = s.split("-")[2].split()[0]
    return source, dest


def generate_mapping_dict(ses: List[str]) -> Dict[str, Dict[str, Any]]:
    mapping_dict = {}
    current_source = None
    current_dest = None
    for s in ses:
        #print()
        #print(f"mapping_dict = {mapping_dict}")
        if s.startswith("seeds"):
            mapping_dict["seeds"] = [int(item) for item in s.split(":")[1].strip().split()]
        elif not s[0].isdigit():
            source, dest = parse_source_dest(s)
            #print(f"source, dest elif {source} {dest}")
            current_source = source
            current_dest = dest
            mapping_dict[current_source] = {"source": source, "dest": dest, "mappings": []}
            #print(f"mapping_dict elif {mapping_dict}")
        else:
            spl = s.split()
            dest_start = int(spl[0])
            source_start = int(spl[1])
            ran = int(spl[2])
            d = {"source_start": source_start, "dest_start": dest_start, "range": ran}
            mapping_dict[current_source]["mappings"] += [d]
    return mapping_dict


def get_location(key: str, index: int, mapping_dict: Dict[str, Any]) -> List[int]:
    #print(f"key={key}; index={index}")
    if key == "location":
       #print()
       return index
    mapping = mapping_dict[key]
    mappings = mapping["mappings"]
    for m in mappings:
        #print(f"m = {m}")
        if index >= m["source_start"] and index <= m["source_start"] + m["range"]:
            offset = index - m["source_start"] 
            #print(f"offset = {offset}")
            dest_index = m["dest_start"] + offset
            #print(f"dest_index = {dest_index}")
            return get_location(mapping["dest"], dest_index, mapping_dict)
    return get_location(mapping["dest"], index, mapping_dict)


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    #print(f"cleaned_list = {cleaned_list}")
    mapping_dict = generate_mapping_dict(cleaned_list)
    #print(f"mapping_dict = {mapping_dict}")
    locations = [get_location("seed", i, mapping_dict) for i in mapping_dict["seeds"]]
    print(f"locations = {locations}")
    result = min(locations)

    return result


#def get_seeds(nums: List[int]):
#    if len(nums) == 0:
#        return []
#    else:
#        seeds = sorted(list(set([i for i in range(nums[0], nums[0]+nums[1])] + get_seeds(nums[2:]))))
#        print(f"len(seeds) = {len(seeds)}")
#        return seeds


def is_seed(num: int, seeds: List[int]) -> bool:
    if len(seeds) == 0:
        return False
    else:
        lower_bound = seeds[0]
        upper_bound = lower_bound + seeds[1]
        if num >= lower_bound and num <= upper_bound:
            return True
        else:
            return is_seed(num, seeds[2:])


def is_mapped(mapping_dict: Dict[str, Dict[str, int]], index: int, key: str, seeds: List[int]) -> bool:
    #print(f"is_mapped: {index} {key}")
    if key == "seed":
        return is_seed(index, seeds)
    else:
        map_dict = mapping_dict[key]
        new_key = map_dict["source"]
        #print(f"new_key = {new_key}")
        for d in map_dict["mappings"]:
            #print(f"d = {d}")
            lower_bound = d["dest_start"]
            #print(f"lower_bound = {lower_bound}")
            upper_bound = d["dest_start"] + d["range"]
            #print(f"upper_bound = {upper_bound}")
            if index >= lower_bound and index <= upper_bound:
                delta = index - d["dest_start"]
                #print(f"delta = {delta}")
                new_index = d["source_start"] + delta
                #print(f"new_index = {new_index}")
                return is_mapped(mapping_dict, new_index, new_key, seeds)
    return is_mapped(mapping_dict, index, new_key, seeds)   



def get_lowest_loc(mapping_dict: Dict[str, Any]) -> int:
    lowest =  100000000000000000
    for d in mapping_dict["location"]["mappings"]:
        if d["dest_start"] < lowest:
            lowest = d["dest_start"]
    return lowest
        

def reverse_mapping_dict(mapping_dict: Dict[str, Any]) -> Dict[str, Any]:
    reversed_dict = {}
    for k, v in mapping_dict.items():
        if k != "seeds":
            reversed_dict[v["dest"]] = v
    return reversed_dict 


def solve_2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    mapping_dict = generate_mapping_dict(cleaned_list)
    print(f"mapping_dict = {mapping_dict}")
    seeds = mapping_dict["seeds"]
    print(f"seeds = {seeds}")
    reversed_dict = reverse_mapping_dict(mapping_dict)
    print(f"reversed_dict = {reversed_dict}")
    lowest_loc = get_lowest_loc(reversed_dict)
    print(f"lowest_loc = {lowest_loc}")
    i = lowest_loc - 1
    while True:
       i += 1
       if i % 10000 == 0:
           print(f"i = {i}")
       mapped = is_mapped(reversed_dict, i, "location", seeds)
       if mapped:
           return i 
       



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve_2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve_2(f.read()[:-1]))


# Notes 8650000 too low
