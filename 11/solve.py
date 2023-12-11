#--- Day 11: Cosmic Expansion ---
#You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.
#
#He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.
#
#Maybe you can help him with the analysis to speed things up?
#
#The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:
#
TEST_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
#The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.
#
#Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.
#
#In the above example, three columns and two rows contain no galaxies:
#
#   v  v  v
# ...#......
# .......#..
# #.........
#>..........<
# ......#...
# .#........
# .........#
#>..........<
# .......#..
# #...#.....
#   ^  ^  ^
#These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:
#
#....#........
#.........#...
##............
#.............
#.............
#........#....
#.#...........
#............#
#.............
#.............
#.........#...
##....#.......
#Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:
#
#....1........
#.........2...
#3............
#.............
#.............
#........4....
#.5...........
#............6
#.............
#.............
#.........7...
#8....9.......
#In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)
#
#For example, here is one of the shortest paths between galaxies 5 and 9:
#
#....1........
#.........2...
#3............
#.............
#.............
#........4....
#.5...........
#.##.........6
#..##.........
#...##........
#....##...7...
#8....9.......
#This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:
#
#Between galaxy 1 and galaxy 7: 15
#Between galaxy 3 and galaxy 6: 17
#Between galaxy 8 and galaxy 9: 5
#In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.
#
#Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

#--- Part Two ---
#The galaxies are much older (and thus much farther apart) than the researcher initially estimated.
#
#Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.
#
#(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)
#
#Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?


from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
sys.setrecursionlimit(100000)


def expand_rows(universe: List[str]) -> List[str]:
    expanded = []
    for row in universe:
        if list(set(row)) == ["."]:
            expanded += [row, row]
        else:
            expanded += [row]
    return expanded


def expand_columns(universe: List[str]) -> List[str]:
    expanded = ["" for _ in universe]
    for i in range(len(universe[0])):
        col_vals = []
        for j in range(len(universe)):
            col_vals += universe[j][i]
        if list(set(col_vals)) == ["."]:
            for k in range(len(expanded)):
                expanded[k] += ".."
        else:
            for k in range(len(expanded)):
                expanded[k] += universe[k][i]
    return expanded


def expand(universe: List[str])-> List[str]:
    row_expanded = expand_rows(universe)
    column_expanded = expand_columns(row_expanded)
    return column_expanded
    

def get_galaxies(universe: List[str]) -> Dict[int, Tuple[int]]:
    galaxies = {}
    counter = 0
    for y in range(len(universe)):
        for x in range(len(universe[0])):
            if universe[y][x] == "#":
                galaxies[counter] = tuple([x, y, 0])
                counter += 1
    return galaxies 


def get_abs_dist(a: int, b: int) -> int:
    if a == b:
        return 0
    low, high = sorted([a, b])
    if low >= 0 and high >= 0:
        return high - low
    elif low <= 0 and high >= 0:
        return abs(low) + high
    return get_abs_dist(abs(low), abs(high))


def get_galaxy_pair_dist(a: Tuple[int], b: Tuple[int]) -> int:
    x_dist = get_abs_dist(a[0], b[0])
    y_dist = get_abs_dist(a[1], b[1])
    return x_dist + y_dist


def get_galaxy_dists(galaxies: Dict[int, Tuple[int]])-> Dict[Tuple[Tuple[int]], int]:
    dist_dict = {}
    for _, g in galaxies.items():
        for _, h in galaxies.items():
            if g != h and tuple([h, g]) not in dist_dict:
                dist_dict[tuple([g, h])] = get_galaxy_pair_dist(g, h)
    return dist_dict


def expand_rows(universe: List[str]) -> List[str]:
    expanded = []
    for row in universe:
        if list(set(row)) == ["."]:
            expanded += [row, row]
        else:
            expanded += [row]
    return expanded


def expand_galaxy_xs(galaxies: Dict[int, Tuple[int]], universe: List[str]) -> Dict[int, Tuple[int]]:
    for i in range(len(universe[0])):
        col_vals = []
        for j in range(len(universe)):
            col_vals += universe[j][i]
        if list(set(col_vals)) == ["."]:
            for identifier, galaxy in galaxies.items():
                x = galaxy[0]
                y = galaxy[1]
                multiples = galaxy[2]
                if x > i:
                    new_vals = tuple([x, y, multiples+1])
                    galaxies[identifier] = new_vals
    return galaxies


def expand_galaxy_ys(galaxies: Dict[int, Tuple[int]], universe: List[str]) -> Dict[int, Tuple[int]]:
    for i in range(len(universe)):
        row = universe[i]
        if list(set(row)) == ["."]:
            for identifier, galaxy in galaxies.items():
                x = galaxy[0]
                y = galaxy[1]
                multiples = galaxy[2]
                if y > i:
                    new_vals = tuple([x, y, multiples+1])
                    galaxies[identifier] = new_vals 
    return galaxies


def expand_galaxy(galaxies: List[str], universe: List[str], factor: int)-> List[str]:
    y_galaxies = deepcopy(galaxies)
    y_expanded_galaxies = expand_galaxy_ys(y_galaxies, universe)
    print(f"y_expanded_galaxies = {y_expanded_galaxies}")
    x_galaxies = deepcopy(galaxies)
    x_expanded_galaxies = expand_galaxy_xs(x_galaxies, universe)
    print(f"x_expanded_galaxies = {x_expanded_galaxies}")
    combined_galaxies = {}
    for identifier in galaxies:
        x = x_expanded_galaxies[identifier][0] + (factor-1) * x_expanded_galaxies[identifier][2] 
        y = y_expanded_galaxies[identifier][1] + (factor-1) * y_expanded_galaxies[identifier][2] 
        combined_galaxies[identifier] = tuple([x,y])
    return combined_galaxies


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    galaxies = get_galaxies(cleaned_list)
    print(f"galaxies = {galaxies}")
    factor = 1000000
    expanded_galaxies = expand_galaxy(galaxies, cleaned_list, factor)
    print(f"expanded_galaxies = {expanded_galaxies}")
    dists = get_galaxy_dists(expanded_galaxies)
    print(f"dists = {dists}")
    result = sum([d for _, d in dists.items()])
    
    return result


def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    expanded = expand(cleaned_list)
    print(f"expanded = {expanded}")
    galaxies = get_galaxies(expanded)
    print(f"galaxies = {galaxies}")
    dists = get_galaxy_dists(galaxies)
    print(f"dists = {dists}")
    dist_sum = sum([d for _, d in dists.items()])
    
    return dist_sum



#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve2(TEST_INPUT))
#print(solve2(TEST_INPUT_2))
#print(solve2(TEST_INPUT_3))
#print(solve2(TEST_INPUT_4))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))


# Note: 76680158 is too low

