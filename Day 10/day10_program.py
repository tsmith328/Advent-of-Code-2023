import os
from functools import reduce


test_file1 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test1.txt"
test_file2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test2.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines
    
def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    extrapolated_vals = [get_next_value([int(x) for x in data.split()]) for data in input_data]
    extrapolated_prev_vals = [get_next_value([int(x) for x in data.split()], True) for data in input_data]
    
    return f"The total sum of the extrapolated values is: {sum(extrapolated_vals)}." \
    + f"{os.linesep}\tThe total sum of the previous extrapolated values is: {sum(extrapolated_prev_vals)}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file1))

    print("Test Case 2:")
    print("\t" + run_case(test_file2))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()
