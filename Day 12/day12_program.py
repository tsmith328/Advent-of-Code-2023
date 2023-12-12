import os
from itertools import combinations

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 12/day12_input_test.txt"

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

def unfolded(data_list):
    new_list = []

    for line in data_list:
        springs, nums = line.split()
        springs = '?'.join([springs] * 5)
        nums = ','.join([nums] * 5)
        new_line = f"{springs} {nums}"
        new_list.append(new_line)
    
    return new_list

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    total_combos_1 = get_combos(input_data)

    input_data = unfolded(input_data)

    total_combos_2 = get_combos(input_data)

    return f"The total number of valid combinations is: {total_combos_1}." \
          + f"{os.linesep}\tThe total number of valid unfolded combinations is: {total_combos_2}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()