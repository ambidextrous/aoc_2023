#--- Day 10: Pipe Maze ---
#You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.
#
#You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.
#
#The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.
#
#Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).
#
#The pipes are arranged in a two-dimensional grid of tiles:
#
#| is a vertical pipe connecting north and south.
#- is a horizontal pipe connecting east and west.
#L is a 90-degree bend connecting north and east.
#J is a 90-degree bend connecting north and west.
#7 is a 90-degree bend connecting south and west.
#F is a 90-degree bend connecting south and east.
#. is ground; there is no pipe in this tile.
#S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
#Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.
#
#For example, here is a square loop of pipe:
#
#.....
#.F-7.
#.|.|.
#.L-J.
#.....
#If the animal had entered this loop in the northwest corner, the sketch would instead look like this:
#
#.....
#.S-7.
#.|.|.
#.L-J.
#....."""
#In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.
#
#Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:
#
#-L|F7
#7S-7|
#L|7||
#-L-J|
#L|-JF
#In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).
#
#Here is a sketch that contains a slightly more complex main loop:
#
#..F7.
#.FJ|.
#SJ.L7
#|F--J
#LJ...
#Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:
#
#7-F7-
#.FJ|7
#SJLL7
#|F--J
#LJ.LJ
#If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.
#
#In the first example with the square loop:
#
TEST_INPUT = """.....
.S-7.
.|.|.
.L-J.
....."""
#You can count the distance each tile in the loop is from the starting point like this:
#
#.....
#.012.
#.1.3.
#.234.
#.....
#In this example, the farthest point from the start is 4 steps away.
#
#Here's the more complex loop again:
#
TEST_INPUT_2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
#Here are the distances for each tile on that loop:
#
#..45.
#.236.
#01.78
#14567
#23...
#Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

#--- Part Two ---
#You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?
#
#To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:
#
#...........
#.S-------7.
#.|F-----7|.
#.||.....||.
#.||.....||.
#.|L-7.F-J|.
#.|..|.|..|.
#.L--J.L--J.
#...........
#The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:
#
#...........
#.S-------7.
#.|F-----7|.
#.||OOOOO||.
#.||OOOOO||.
#.|L-7OF-J|.
#.|II|O|II|.
#.L--JOL--J.
#.....O.....
#In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:
#
TEST_INPUT_3 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J."""
#..........
#In both of the above examples, 4 tiles are enclosed by the loop.
#
#Here's a larger example:
#
#.F----7F7F7F7F-7....
#.|F--7||||||||FJ....
#.||.FJ||||||||L7....
#FJL7L7LJLJ||LJ.L-7..
#L--J.L7...LJS7F-7L7.
#....F-J..F7FJ|L7L7L7
#....L7.F7||L7|.L7L7|
#.....|FJLJ|FJ|F7|.LJ
#....FJL-7.||.||||...
#....L---J.LJ.LJLJ...
#The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):
#
#OF----7F7F7F7F-7OOOO
#O|F--7||||||||FJOOOO
#O||OFJ||||||||L7OOOO
#FJL7L7LJLJ||LJIL-7OO
#L--JOL7IIILJS7F-7L7O
#OOOOF-JIIF7FJ|L7L7L7
#OOOOL7IF7||L7|IL7L7|
#OOOOO|FJLJ|FJ|F7|OLJ
#OOOOFJL-7O||O||||OOO
#OOOOL---JOLJOLJLJOOO
#In this larger example, 8 tiles are enclosed by the loop.
#
#Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:
#
TEST_INPUT_4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
#Here are just the tiles that are enclosed by the loop marked with I:
#
#FF7FSF7F7F7F7F7F---7
#L|LJ||||||||||||F--J
#FL-7LJLJ||||||LJL-77
#F--JF--7||LJLJIF7FJ-
#L---JF-JLJIIIIFJLJJ7
#|F|F-JF---7IIIL7L|7|
#|FFJF7L7F-JF7IIL---7
#7-L-JL7||F7|L7F-7F7|
#L.L7LFJ|||||FJL7||LJ
#L7JLJL-JLJLJL--JLJ.L
#In this last example, 10 tiles are enclosed by the loop.
#
#Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?



from typing import List, Dict, Any, Tuple, Iterable, Set
from copy import deepcopy
import math
import sys
sys.setrecursionlimit(100000)


def get_start(lines: List[str]):
    x = 0
    y = 0
    for y, l in enumerate(lines):
        for x, character in enumerate(l):
            if character == "S":
                return {"x": x, "y": y}
    raise ValueError("No start point found")


def get_heading(tile: str, heading: str) -> str:
    #print(f"get_heading: tile = {tile}; heading = {heading}")
    if tile == "S":
        return "HOME"
    elif tile == "|":
        if heading == "N" or heading == "S": 
            return heading
    elif tile == "-":
        if heading == "E" or heading == "W": 
            return heading
    elif tile == "L":
        if heading == "W":
            return "N"
        elif heading == "S":
            return "E"
    elif tile == "J":
        if heading == "E":
            return "N"
        elif heading == "S":
            return "W"
    elif tile == "7":
        if heading == "N":
            return "W"
        elif heading == "E":
            return "S"
    elif tile == "F":
        if heading == "N":
            return "E"
        elif heading == "W":
            return "S"
    raise ValueError(f"tile = {tile}; heading = {heading}")


def take_step(pos: Dict[str, int], grid: List[List[str]]) -> Dict[str, Any]:
    #print(f"pos = {pos}")
    x = pos["x"]
    y = pos["y"]
    heading = pos["h"]
    counter = pos["counter"]
    if heading == "N":
        new_y = y - 1
        new_x = x
    elif heading == "S":
        new_y = y + 1
        new_x = x
    elif heading == "E":
        new_y = y
        new_x = x + 1
    elif heading == "W":
        new_y = y
        new_x = x - 1
    else:
        raise ValueError(str(f"heading = {heading}; pos = {pos}"))
    new_tile = grid[new_y][new_x]
    #print(f"new_tile = {new_tile}")
    new_heading = get_heading(new_tile, heading)
    #print(f"new_heading = {new_heading}")
    steps = pos["steps"] + [(x, y)]
    hands = pos["headings"] + [new_heading]
    new_pos = {"x": new_x, "y": new_y, "h": new_heading, "t": new_tile, "counter": counter + 1, "steps": steps, "headings": hands}
    if new_heading == "HOME":
        return new_pos
    return take_step(new_pos, grid)



def take_first_step(start: Dict[str, int], grid: List[str]) -> List[List[str]]:
    successful_trips = []
    x = start["x"]
    y = start["y"]
    steps = [(x,y)]
    try:
        next_tile = grid[y][x+1]
        east_pos = {"x": x + 1, "y": y, "h": "E", "t": next_tile, "counter": 1, "steps": steps, "headings": ["E"]}
        if next_tile in ["-", "J", "7"]:
            return take_step(east_pos, grid)
    except Exception as ex:
        print(f"East: {ex}")
    try:
        next_tile = grid[y][x-1]
        west_pos = {"x": x - 1, "y": y, "h": "W", "t": next_tile, "counter": 1, "steps": steps, "headings": ["W"]}
        if next_tile in ["-", "F", "L"]:
            return take_step(west_pos, grid)
    except Exception as ex:
        print(f"West: {ex}")
    try:
        next_tile = grid[y - 1][x]
        north_pos = {"x": x, "y": y - 1, "h": "N", "t": next_tile, "counter": 1, "steps": steps, "headings": ["N"]}
        if next_tile in ["|", "7", "F"]:
            return take_step(north_pos, grid)
    except Exception as ex:
        print(f"North: {ex}")
    try:
        next_tile = grid[y + 1][x]
        south_pos = {"x": x, "y": y + 1, "h": "S", "t": next_tile, "counter": 1, "steps": steps, "headings": ["S"]}
        if next_tile in ["|", "L", "J"]:
            return take_step(south_pos, grid)
    except Exception as ex:
        print(f"South: {ex}")
    

def get_potential_enclosed_starts(tile: str, heading: str, x: int, y: int) -> Tuple[int]:
    # Assumed handedness is left
    encloseds = None
    if heading == "S":
        if tile == "|":
            encloseds = [(x+1,y),]
        elif tile == "7":
            encloseds = [(x,y-1),(x+1,y-1),(x+1,y)]
        elif tile == "F":
            encloseds = [(x+1,y+1),]
    elif heading == "N":
        if tile == "|":
            encloseds = [(x-1,y),]
        elif tile == "L":
            encloseds = [(x,y+1),(x-1,y+1),(x-1,y)]
        elif tile == "J":
            encloseds = [(x-1,y-1),]
    elif heading == "E":
        if tile == "-":
            encloseds = [(x,y-1),]
        elif tile == "L":
            encloseds = [(x+1,y-1),]
        elif tile == "F":
            encloseds = [(x-1,y),(x-1,y-1),(x,y-1)]
    elif heading == "W":
        if tile == "-":
            encloseds = [(x,y+1),]
        elif tile == "7":
            encloseds = [(x-1,y+1),]
        elif tile == "J":
            encloseds = [(x+1,y),(x+1,y+1),(x,y+1)]
    if encloseds is None:
        raise ValueError(f"Error in get_potential_enclosed_starts: tile = {tile}; heading = {heading}; x = {x}; y = {y}")
    return encloseds


def enclose(x: int, y: int, grid: List[str], path: Set[Tuple[int]], encloseds: List[Tuple[int]]) -> Set[Tuple[int]]:
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        #raise ValueError(f"Gone off grid at ({x},{y}): searching wrong side!")
        #print(f"Gone off grid at ({x},{y}): searching wrong side!")
        pass
    elif (x, y) not in path and (x, y) not in encloseds:
        new_enclosed = (x, y)
        #print(f"new_enclosed = {new_enclosed}")
        #encloseds = encloseds.union(set([(x,y),]))
        encloseds += [new_enclosed]
        moves = [-1,0,1]
        for i in moves: 
            for j in moves:
                if not (i == 0 and j == 0):
                    new_x = x+i 
                    new_y = y+j 
                    enclose(new_x, new_y, grid, path, encloseds)


def get_encloseds(path: List[Tuple[int]], headings: List[str],  grid: List[str]) -> List[Tuple[int]]:
    path_set = set(path)
    encloseds = []
    for i in range(1, len(path)):
         #print()
         #print(str(i))
         #print(f"encloseds = {encloseds}")
         coords = path[i]
         #print(f"coords = {coords}")
         x = coords[0]
         y = coords[1]
         tile = grid[y][x]
         #print(f"tile = {tile}")
         heading = headings[i-1]
         #print(f"heading = {heading}")
         potential_enclosed_starts = get_potential_enclosed_starts(tile,heading,x,y)  
         for pot in potential_enclosed_starts:
             enclose(pot[0], pot[1], grid, path, encloseds)
    return encloseds


def solve2(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    start = get_start(cleaned_list)
    print(f"start = {start}")
    step_dict = take_first_step(start, cleaned_list)
    #print(f"step_dict = {step_dict}")
    path = step_dict["steps"]
    #print(f"path = {path}")
    path_size = len(path)
    #print(f"path_size = {path_size}")
    headings = step_dict["headings"]
    #print(f"headings = {headings}")
    encloseds = get_encloseds(path, headings, cleaned_list)
    #print(f"encloseds = {encloseds}")
    grid_size = len(cleaned_list) * len(cleaned_list[0])
    #print(f"grid_size = {grid_size}")
    non_enclosed_count = grid_size - path_size - len(encloseds)
    
    result_dict = {"grid_size": grid_size, "encloseds": len(encloseds), "path_size": path_size, "non_encloseds": non_enclosed_count}

    return result_dict



def solve(input_string: str) -> List[int]:
    result = None
    raw_list = input_string.split("\n")
    raw_list = [l.strip() for l in raw_list]
    cleaned_list = [item for item in raw_list if len(item) > 0] 
    print(f"cleaned_list = {cleaned_list}")
    start = get_start(cleaned_list)
    print(f"start = {start}")
    step_dict = take_first_step(start, cleaned_list)
    print(f"step_dict = {step_dict}")

    result = math.ceil(step_dict["counter"]/2)
    
    return result



#print(solve(TEST_INPUT))
#print(solve(TEST_INPUT_2))
        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

#print(solve2(TEST_INPUT))
#print(solve2(TEST_INPUT_2))
#print(solve2(TEST_INPUT_3))
print(solve2(TEST_INPUT_4))
#        
with open("input.txt", "r") as f:
    print(solve2(f.read()[:-1]))

# Note for part 2, answer will either be encloseds or non_encloseds - haven't implemented an algorthim to work out which it is

