#--- Day 3: Gear Ratios ---
#You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
#
#It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
#
#"Aaah!"
#
#You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
#
#The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
#
#The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
#
#Here is an example engine schematic:

TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
#In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
#
#Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

TEST_INPUT = """...............................930...................................283...................453.34.............................867....282....
....=.........370...........................48..456......424...-.341*.....554...*807.571............971..958............166......*..........
..159.........../..........539*.....73......-...*.......+....954.........*.....7.......*........*.....*....*.....405$..*.......31.........15"""

# Test with duplicates
TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
.......755
...$..*...
.664.598.."""

#--- Part Two ---
#The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
#
#You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
#
#Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.
#
#The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
#
#This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
#
#Consider the same engine schematic again:

TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
#In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
#
#What is the sum of all of the gear ratios in your engine schematic?

from typing import List, Dict, Any

def get_num_co_ords(s: str) -> List[Dict[str, int]]:
    co_ords = []
    num = ""
    start = None
    for i, ch in enumerate(s):
        if ch.isdigit():
            num += ch
            if start is None:
                start = i
        else:
            if num != "":
                entry = {"start": start, "end": i-1, "num": int(num)}
                co_ords += [entry]
                num = ""
                start = None
    # Handle number at end of line case
    if num != "":
        entry = {"start": start, "end": i-1, "num": int(num)}
        co_ords += [entry]
    return co_ords
            

def get_symbol_co_ords(s: str) -> List[Dict[str, int]]:
    co_ords = {}
    for i, ch in enumerate(s):
        if not ch.isdigit() and ch != ".":
            co_ords[i] = ch
    return co_ords
            

def is_valid(co_ord_dict: Dict[str, int], syms: List[Dict[int, str]]) -> bool:
    print()
    print(f"co_ord_dict = {co_ord_dict}")
    print(f"syms = {syms}")
    for sym_locs in syms:
        print(f"sym_locs = {sym_locs}")
        for sym_loc in sym_locs:
            print(f"sym_loc = {sym_loc}")
            #if sym_loc >= co_ord_dict["start"] - 1 and sym_loc <= co_ord_dict["end"]+ 1:
            start_limit = co_ord_dict["start"] - 1 
            end_limit = co_ord_dict["end"] + 1
            print(f"start_limit = {start_limit}")
            print(f"end_limit = {end_limit}")
            if sym_loc >= start_limit and sym_loc <= end_limit:
                return True
    return False


def filter_nums(num_cos: List[Dict[str, int]], sym_cos: List[Dict[int, str]]) -> List[Dict[str, int]]:
    filtered = []
    for i, num_co in enumerate(num_cos):
        print(f"num_co = {num_co}")
        if i == 0:
           prev = {}
        else:
           prev = sym_cos[i-1]
        if i == len(sym_cos)-1:
           subsequent = {}
        else:
           subsequent = sym_cos[i+1]
        current = sym_cos[i]
        syms = [prev, current, subsequent]
        #filtered_num_cos = [filter_valids(n, syms) for n in num_co]
        filtered_num_cos = [d for d in num_co if is_valid(d, syms)]
        filtered += [filtered_num_cos]
    return filtered


def get_gear_score(num_cos: List[Dict[str, int]], sym: int) -> int:
    gears = [num_co for num_co in num_cos if sym >= num_co["start"] - 1 and sym <= num_co["end"] + 1]
    print(f"gears = {gears}")
    if len(gears) == 2:
        return gears[0]["num"] * gears[1]["num"]
    return 0
   

def get_gear_ratios(num_cos: List[Dict[str, int]], sym_cos: List[Dict[int, str]]) -> List[int]:
    gear_ratio_scores = []
    gear_ratio_total = 0
    for i, line in enumerate(sym_cos):
        print(f"line = {line}")
        line_ratios = []
        for entry in line:
            print(f"entry = {entry}")
            if i == 0:
                prev = []
            else:
                prev = num_cos[i-1]
            if i == len(sym_cos) - 1:
                subsequent = []
            else:
                subsequent = num_cos[i+1]
            current = num_cos[i]
            combined = prev + current + subsequent
            #gear_ratio_scores = [get_gear_score(combined,sym) for sym in line]
            gear_ratio_score = get_gear_score(combined,entry)
            gear_ratio_total += gear_ratio_score
            print(f"gear_ratio_score = {gear_ratio_score}")
            line_ratios += [gear_ratio_score]
            print(f"line_ratios = {line_ratios}")
        gear_ratio_scores += [line_ratios]
    return gear_ratio_scores, gear_ratio_total


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    co_ords = [get_num_co_ords(l) for l in cleaned_list]
    print(f"co_ords =  {co_ords}")
    sym_co_ords = [get_symbol_co_ords(l) for l in cleaned_list]
    print(f"sym_co_ords = {sym_co_ords}")
    filtered = filter_nums(co_ords, sym_co_ords)
    print(f"filtered = {filtered}")
    nums = [[d["num"] for d in l] for l in filtered]
    print(f"nums = {nums}")
    num_totals = [sum(l) for l in nums]
    print(f"num_totals = {num_totals}") 
    result = sum(num_totals)
    return result


def solve_2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    co_ords = [get_num_co_ords(l) for l in cleaned_list]
    print(f"co_ords =  {co_ords}")
    sym_co_ords = [get_symbol_co_ords(l) for l in cleaned_list]
    print(f"sym_co_ords = {sym_co_ords}")
    gear_ratio_scores, gear_ratio_total  = get_gear_ratios(co_ords, sym_co_ords)
    print(f"gear_ratio_scores = {gear_ratio_scores}")
    return gear_ratio_total


#print(solve(TEST_INPUT))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))
#
print(solve_2(TEST_INPUT))
#        
with open("input.txt", "r") as f:
    print(solve_2(f.read()[:-1]))
#

# Notes
# Part 1
# 535158 too low
