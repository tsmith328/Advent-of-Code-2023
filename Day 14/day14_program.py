import os
from enum import Enum
from functools import cache

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 14/day14_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 14/day14_input.txt"

def read_file(file_name: str) -> list[list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        return [l.strip() for l in file.readlines() if len(l.strip()) > 0]

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

def load_mirror(input_data):
    mirror = []
    for line in input_data:
        mirror_line = [x for x in line]
        mirror.append(mirror_line)
    
    return mirror

def find_new_pos(mirror: list[list[str]], x: int, y: int, direction: Direction) -> tuple[int, int]:
    # Determine which direction we should traverse.
    dx = 0
    dy = 0
    curr_x = x
    curr_y = y
    max_x = len(mirror[0])
    max_y = len(mirror)
    if direction == Direction.UP:
        dy = -1
    elif direction == Direction.DOWN:
        dy = 1
    elif direction == Direction.LEFT:
        dx = -1
    elif direction == Direction.RIGHT:
        dx = 1
    else:
        return (x, y)
    
    curr_char = mirror[curr_y][curr_x]
    next_x = curr_x + dx
    next_y = curr_y + dy

    num_rocks = 0

    while curr_x >= 0 and curr_y >= 0 and curr_x < max_x and curr_y < max_y:
        curr_char = mirror[curr_y][curr_x]
        if curr_char == '#':
            break
        # Count how many other rocks we'll pass.
        if curr_char == 'O': 
            num_rocks += 1
        # Move in direction
        curr_x += dx
        curr_y += dy
        
    
    # curr_char should be the first # rock we hit in this direction.
    # Now move back by the number of round rocks we passed.
    curr_x -= (dx * num_rocks) 
    curr_y -= (dy * num_rocks)

    # Should be the new position of our rock.
    return (curr_x, curr_y)

def move_mirror(mirror: list[list[str]], direction: Direction) -> list[tuple[int,int]]:
    rocks = [(x,y) for y,row in enumerate(mirror) for x,char in enumerate(row) if char == 'O']
    new_rocks = []
    for rock in rocks:
        new_pos = find_new_pos(mirror, rock[0], rock[1], direction)
        new_rocks.append(new_pos)
    
    return new_rocks

def calculate_weight(num_rows: int, rocks: list[tuple[int,int]]) -> int:
    weight = 0
    for rock in rocks:
        rock_row = rock[1]
        rock_weight = num_rows - rock_row
        weight += rock_weight
    
    return weight

def clear_mirror(mirror: list[list[str]]):
    return [['.' if char == 'O' else char for char in line] for line in mirror]

def add_rocks(mirror: list[list[str]], rocks: list[tuple[int,int]]):
    for y, line in enumerate(mirror):
        for x, char in enumerate(line):
            if (x, y) in rocks:
                mirror[y][x] = 'O'
    return mirror

def spin_cycle_stage(mirror: list[list[str]], direction: Direction) -> list[list[str]]:
    new_rocks = move_mirror(mirror, direction)
    new_mirror = clear_mirror(mirror)
    new_mirror = add_rocks(new_mirror, new_rocks)
    return new_mirror

def find_rocks(mirror: list[list[str]]):
    rocks = [(x,y) for y,line in enumerate(mirror) for x,char in enumerate(line) if char == 'O']
    return rocks

def spin_cycle(mirror: list[list[int]]) -> list[tuple[int,int]]:
    num_cycles = 1_000_000_000
    new_rocks = []
    states = dict()
    new_mirror = mirror
    cycle_len = 0
    # Find the cycle
    for i in range(num_cycles):
        new_mirror = spin_cycle_stage(new_mirror, Direction.UP)
        new_mirror = spin_cycle_stage(new_mirror, Direction.LEFT)
        new_mirror = spin_cycle_stage(new_mirror, Direction.DOWN)
        new_mirror = spin_cycle_stage(new_mirror, Direction.RIGHT)
        rocks = find_rocks(new_mirror)
        rock_tuple = tuple(rocks)

        if rock_tuple in states.keys():
            print(f"Found repeat at {i} with {states[rock_tuple]}.")
            cycle_len = i - states[rock_tuple]
            break
        else:
            states[rock_tuple] = i
        
    # cycle_len should be the length of the cycle
    # i - cycle_len is where the cycle started
    cycle_start = i - cycle_len
    remainder = num_cycles % (cycle_len - 1)
    target_cycle = cycle_start + remainder
    new_mirror = mirror # Reset mirror
    for i in range(target_cycle):
        new_mirror = spin_cycle_stage(new_mirror, Direction.UP)
        new_mirror = spin_cycle_stage(new_mirror, Direction.LEFT)
        new_mirror = spin_cycle_stage(new_mirror, Direction.DOWN)
        new_mirror = spin_cycle_stage(new_mirror, Direction.RIGHT)
    rocks = find_rocks(new_mirror)
    
    return rocks

def run_case(file_name: str) -> str:
    #input_data = read_file(file_name)
    
    input_str = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    input_data = [l.strip() for l in input_str.splitlines() if len(l.strip()) > 0]

    mirror = load_mirror(input_data)
    #Move Mirror broke
    rock_locations = move_mirror(mirror, Direction.UP)
    weight = calculate_weight(len(mirror), rock_locations)

    rock_locations = spin_cycle(mirror)
    new_weight = calculate_weight(len(mirror), rock_locations)

    return f"The total weight is: {weight}." \
          + f"{os.linesep}\tThe total weight after the spin cycle is: {new_weight}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()