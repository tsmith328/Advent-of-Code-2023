import os
from enum import Enum

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input.txt"

def read_file(file_name: str) -> list[list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        return [l.strip() for l in file.readlines() if len(l.strip()) > 0]

class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    return f"The number of spots energized is: {''}." \
          + f"{os.linesep}\tThe highest possible energy level is: {''}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()