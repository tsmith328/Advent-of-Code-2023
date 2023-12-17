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

def build_field(file_data: list[list[str]]) -> dict[tuple[int,int],int]:
    field = dict()
    for y, line in enumerate(file_data):
        for x, char in enumerate(line):
            field[(x, y)] = int(char)
    
    return field

def get_diag_weight(field: dict[tuple[int,int],int]) -> int:
    """Gets weight of diagonal path as a baseline for comparing weights of other paths."""
    max_x = max([point[0] for point in field.keys()])
    max_y = max([point[1] for point in field.keys()])
    curr_x = 0
    curr_y = 0
    total_weight = 0
    while curr_x < max_x and curr_y < max_y:
        # Move right
        curr_x += 1
        weight = field[(curr_x, curr_y)]
        total_weight += weight
        # Move down
        curr_y += 1
        weight = field[(curr_x, curr_y)]
        total_weight += weight
    
    return total_weight


def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    field = build_field(input_data)

    diag_weight = get_diag_weight(field)

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