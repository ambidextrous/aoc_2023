TEST_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
TEST_INPUT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


from typing import List

NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def get_first_num(s: str) -> int:
    if s[0].isdigit():
        return int(s[0])
    return get_first_num(s[1:])

def get_first_num_or_word(s: str) -> int:
    for num_word, val in NUM_WORDS.items():
       if s.startswith(num_word):
          return str(val)
    if s[0].isdigit():
        return int(s[0])
    return get_first_num_or_word(s[1:])


def get_last_num(s: str) -> int:
    if s[-1].isdigit():
        return int(s[-1])
    return get_last_num(s[:-1])


def get_last_num_or_word(s: str) -> int:
    for num_word, val in NUM_WORDS.items():
       if s.endswith(num_word):
          return str(val)
    if s[-1].isdigit():
        return int(s[-1])
    return get_last_num_or_word(s[:-1])
    

def solve(input_string: str) -> List[int]:
    raw_list = input_string.split("\n")
    numbers = []
    pairs = [f"{get_first_num(line)}{get_last_num(line)}" for line in raw_list if len(line) > 0]
    #print(pairs)
    nums = [int(pair) for pair in pairs]
    #print(nums)
    return sum(nums)

def solve_2(input_string: str) -> List[int]:
    raw_list = input_string.split("\n")
    #print(raw_list)
    numbers = []
    pairs = [f"{get_first_num_or_word(line)}{get_last_num_or_word(line)}" for line in raw_list if len(line) > 0]
    #print(pairs)
    nums = [int(pair) for pair in pairs]
    #print(nums)
    return sum(nums)


#print(solve(TEST_INPUT))
#        
#with open("input.txt", "r") as f:
#    print(solve(f.read()[:-1]))

print(solve_2(TEST_INPUT))
        
with open("input.txt", "r") as f:
    print(solve_2(f.read()[:-1]))


