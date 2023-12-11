import os
from math import ceil


test_file1 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 11/day11_input_test1.txt"
test_file2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 11/day11_input_test2.txt"
test_file3 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 11/day11_input_test3.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 11/day11_input.txt"

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

    maze = build_pipes(input_data)

    start_x, start_y = find_start(maze)

    pipe = traverse_maze(maze, (start_x, start_y))
    vertices = find_vertices(list(pipe.keys()))
    area = points_inside(maze, pipe)
    """ 
    vertices = scale_vertices(vertices)
    area1 = get_area(vertices)"""

    return f"The furthest point is this many steps away from the start: {ceil(len(pipe.keys()) / 2)}." \
    + f"{os.linesep}\tThe total area of this pipe is: {area}."

def main() -> None:
    # Run test case
    print("Test Case 1 (Should be 1):")
    print("\t" + run_case(test_file1))

    print("Test Case 2 (Should be 1):")
    print("\t" + run_case(test_file2))

    print("Test Case 3 (Should be 4):")
    print("\t" + run_case(test_file3))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()