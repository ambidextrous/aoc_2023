TEST_INPUT = """Time:      7  15   30
Distance:  9  40  200"""
EXAMPLE_RACE_DICT = {
    "dist": 9,
    "time": 7,
    "hold_times": {
        0: {
           "hold": 0,
           "dist": 0,
           "speed": 0,
        },
        1: {
           "hold": 1,
           "dist": 6,
           "speed": 1,
        },
        2: {
           "hold": 2,
           "dist": 10,
           "speed": 2,
        },
        3: {
           "hold": 3,
           "dist": 12,
           "speed": 3,
        },
        4: {
           "hold": 4,
           "dist": 12,
           "speed": 4,
        },
        5: {
           "hold": 5,
           "dist": 10,
           "speed": 5,
        },
        6: {
           "hold": 6,
           "dist": 6,
           "speed": 6,
        },
        7: {
           "hold": 7,
           "dist": 0,
           "speed": 7,
        },
    }
}



from typing import List, Dict, Any, Tuple
from copy import deepcopy


def get_races_dict(times_raw: str, dists_raw: str) -> Dict[str, int]:
    times = [int(item) for item in times_raw.split(":")[1].strip().split()]
    dists = [int(item) for item in dists_raw.split(":")[1].strip().split()]
    race_dicts = [{"time": times[i], "dist": dists[i]} for i in range(len(times))]
    return race_dicts


def get_race_dict(times_raw: str, dists_raw: str) -> Dict[str, int]:
    time = int("".join([item for item in times_raw.split(":")[1].strip().split()]))
    dist = int("".join([item for item in dists_raw.split(":")[1].strip().split()]))
    race_dict = {"time": time, "dist": dist}
    return race_dict


def get_win_count(dist: int, record: int) -> List[Dict[str, Any]]:
    #print(f"dist={dist}; record={record}")
    distances = [run_race_strategy(dist, i) for i in range(dist+1)]
    #print(f"distances = {distances}")
    beat_records = [dist > record for dist in distances]
    return sum(beat_records)


def run_race_strategy(race_dist: int, hold_time: int) -> int:
    #print(f"raced_dist={race_dist}; hold_time{hold_time}")
    return hold_time * (race_dist - hold_time)  


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    races_dict = get_races_dict(cleaned_list[0], cleaned_list[1])
    print(f"races_dict = {races_dict}")
    win_counts = [get_win_count(race["time"], race["dist"]) for race in races_dict]
    print(f"win_counts = {win_counts}")
    result = 1
    for count in win_counts:
        result *= count
    return result
       

def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    race_dict = get_race_dict(cleaned_list[0], cleaned_list[1])
    print(f"race_dict = {race_dict}")
    win_count = get_win_count(race_dict["time"], race_dict["dist"])
    print(f"win_count = {win_count}")
    result = win_count
    return result



#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

