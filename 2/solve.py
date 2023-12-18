TEST_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


from typing import List, Dict, Any

def get_hand_dict(s: str) -> Dict[str, int]:
    de_commaed = [item.strip() for item in s.split(",")]
    #print(f"de_commaed {de_commaed}")
    hand_dict = {}
    for item in de_commaed:
        hand_dict[item.split()[1]] = int(item.split()[0])
    #print(hand_dict)
    return hand_dict


def get_game_dict(s: str) -> Dict[str, int]:
    colon_split_string = [item.strip() for item in s.split(":")]
    game_number = int(colon_split_string[0].split()[1]) 
    #print(game_number)
    rounds = [item.strip() for item in colon_split_string[1].strip().split(";")]
    #print(f"rounds = {rounds}")
    hand_dicts = [get_hand_dict(r) for r in rounds]
    #print(f"hand_dicts = {hand_dicts}")
    return hand_dicts

    #result_dict = {1: None, 2, None, 3: None}
    #result_dict[1]["blue"] = int(rounds[1])
    #result_dict["blue"] = int(rounds[1])

def is_possible_game(game_dict: Dict[str, int], config: Dict[str, int]) -> bool:
    #print(f"is_possible_game: {game_dict}; {config}")
    for key, val in config.items():
        #print(f"{key} {val}")
        #if key not in game_dict:
        #    print("key not in game_dict")
        #    return False
        if key in game_dict and game_dict[key] > val:
            #print(f"{game_dict[key]} > {val}")
            return False
    return True
            
def are_possible_games(game_dicts: Dict[str, int], config: Dict[str, int]) -> bool:
    #print(f"are_possible_game: {game_dicts}")
    return all([is_possible_game(game_dict, config) for game_dict in game_dicts])

def solve(input_string: str) -> List[int]:
    config = {"red": 12, "green": 13, "blue": 14}
    raw_list = input_string.split("\n")
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    game_dicts = [get_game_dict(item) for item in cleaned_list]
    #print(f"game_dicts = {game_dicts}")
    possible_games = [are_possible_games(game_dict, config) for game_dict in game_dicts]
    #print(f"possible_games = {possible_games}")
    results = [i+1 for i, pos in enumerate(possible_games) if pos is True]
    #print(results)
    result = sum(results)
    return result

def get_power(game_dicts: Dict[str, int]) -> int:
    highest = {"red": 0, "green": 0, "blue": 0}
    for game_dict in game_dicts:
        for colour, num in game_dict.items():
            if num > highest[colour]:
                highest[colour] = num
    return highest["red"] * highest["green"] * highest["blue"]
     

def solve_2(input_string: str) -> List[int]:
    raw_list = input_string.split("\n")
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    game_dicts = [get_game_dict(item) for item in cleaned_list]
    #print(f"game_dicts = {game_dicts}")
    powers = [get_power(game_dict) for game_dict in game_dicts]
    result = sum(powers)
    return result

print(solve(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve(f.read()[:-1]))

print(solve_2(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve_2(f.read()[:-1]))


