import os
from itertools import combinations

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 12/day12_input_test.txt"
test_file = "C:/Users/tms/Downloads/AOC/Advent-of-Code-2023/Day 12/day12_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 12/day12_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines

def get_possible_positions(line: str, num_positions: int) -> list[int]:
    return combinations([i for i, x in enumerate(line) if x == "?"], num_positions)

def is_valid(springs, line, numbers):
    valid = []
    for combo in list(springs):
        ok = True
        this_line = ''.join(['#' if i in combo else '.' if x == "?" else x for i, x in enumerate(line)])
        groups = [x for x in this_line.split('.') if len(x) > 0]
        if len(groups) != len(numbers):
            ok = False
            continue
        for i, group in enumerate(groups):
            if len(group) != numbers[i]:
                ok = False
        if ok:
            valid.append(combo)

    return len(valid)

def get_combos(input_data):
    total_combos = 0

    for line in input_data:
        springs = line.split()[0]
        num_springs = list(map(int, line.split()[1].split(',')))
        num_broken = sum([1 if x == "#" else 0 for x in springs])
        combos = get_possible_positions(springs, sum(num_springs) - num_broken)
        total_combos += is_valid(combos, springs, num_springs)
    
    return total_combos

def get_combos_rec(springs: str, groups: list[int]) -> int:
    # Start with base cases
    if len(springs) == 0:
        if len(groups) == 0:
            # Nothing left, we can consider it a success
            return 1
        else:
            # No more springs left, but we have groups of broken springs left
            return 0
    
    if len(groups) == 0:
        # No broken springs should be left
        if "#" in springs:
            # Broken springs are left
            return 0
        else:
            # None left, yay.
            return 1
    
    # we have some springs and some groups left.
    next_spring = springs[0]
    next_group = groups[0]
    if next_spring == '.':
        # If first char is a dot, handle it
        return get_combos_dot(springs, groups)
    
    if next_spring == '#':
        # If a hash/pound, handle it
        return get_combos_pound(springs, groups)
    
    # Next spring must be ?
    return get_combos_dot(springs, groups) + get_combos_pound(springs.replace('?', '#', 1), groups)
    
def get_combos_pound(springs: str, groups: list[int]) -> int:
    # This is called when the next character is a #, which means the first N chars need to be # or ?
    n = groups[0] # Number of broken springs in this group
    # if we need more characters than we have left, it's a bad combo.
    if n > len(springs):
        return 0
    next_n = springs[:n] # chars that need to be broken for this group to be ok
    if '.' in next_n:
        # If a . is here, we don't have enough room to fit all the broken springs
        return 0
    if n == len(springs):
        # length of springs is the same as the group that's left and we have no .'s.
        return 1
    next_char = springs[n] # Next character after this group of broken springs. Should be unbroken.
    if next_char in '?.':
        # It can be unbroken. Check the rest of the string.
        return get_combos_rec(springs[n:], groups[1:])
    
    # Next char is broken, this group is too big
    return 0        

def get_combos_dot(springs: str, groups: list[int]) -> int:
    # If first char is a dot, we can just take it out and check the resulting string.
    return get_combos_rec(springs[1:], groups)
    

def unfolded(data_list):
    new_list = []

    for line in data_list:
        springs, nums = line.split()
        springs = '?'.join([springs] * 5)
        nums = ','.join([nums] * 5)
        new_line = f"{springs} {nums}"
        new_list.append(new_line)
    
    return new_list

def find_combos_recursively(input_data: list[str]) -> int:
    total_combos = 0
    for line in input_data:
        springs = line.split()[0]
        groups = tuple([int(x) for x in line.split()[1].split(',')])
        combos = get_combos_rec(springs, groups)
        print(f"{line} -> {combos}.")
        total_combos += combos
    
    return total_combos

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    total_combos_1 = get_combos(input_data)
    total_combos_1 = find_combos_recursively(input_data)

    input_data = unfolded(input_data)
    total_combos_2 = 0
    total_combos_2 = get_combos(input_data) 

    return f"The total number of valid combinations is: {total_combos_1}." \
          + f"{os.linesep}\tThe total number of valid unfolded combinations is: {total_combos_2}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    """https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/"""

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()