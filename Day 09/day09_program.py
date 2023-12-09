import os
from functools import reduce


test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 09/day09_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 09/day09_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines
    
def get_next_value(data: list[int], backwards: bool = False) -> int:
    # Sanity check?
    if len(data) == 0:
        return 0

    distinct_vals = len(set(data))
    if distinct_vals == 1:
        # Only have one value, we can return it up to the prev. call.
        # Base case
        return data[0]
    
    differences = get_differences(data)
    next_diff = get_next_value(differences, backwards)
    if backwards:
        next_val = data[0] - next_diff
    else:
        next_val = data[-1] + next_diff
    return next_val

def get_differences(nums: list[int]) -> list[int]:
    diffs = []
    for i in range(len(nums) - 1):
        diffs.append(nums[i + 1] - nums[i])
    return diffs

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    extrapolated_vals = [get_next_value([int(x) for x in data.split()]) for data in input_data]
    extrapolated_prev_vals = [get_next_value([int(x) for x in data.split()], True) for data in input_data]
    
    return f"The total sum of the extrapolated values is: {sum(extrapolated_vals)}." \
    + f"{os.linesep}\tThe total sum of the previous extrapolated values is: {sum(extrapolated_prev_vals)}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()
