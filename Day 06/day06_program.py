import os
from math import floor
from math import ceil

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 06/day06_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 06/day06_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines

def parse_races(race_list: str, remove_spaces: bool = False) -> list[tuple[int,int]]:
    if not remove_spaces:
        return [(int(time), int(dist)) for time, dist in zip(race_list[0].split()[1:], race_list[1].split()[1:])]
    
    times = race_list[0].split(":")[1]
    distances = race_list[1].split(":")[1]
    time = times.replace(" ", "")
    dist = distances.replace(" ", "")
    return [(int(time), int(dist))]

def run_races(races: list[tuple[int,int]]) -> int:
    num_ways = 1
    for max_time, max_dist in races:
        sqrt = (0.5 * (max_time ** 2 - 4 * max_dist) ** (0.5))
        t_max = floor((max_time / 2) + sqrt)
        t_min = ceil((max_time / 2) - sqrt)
        dist_max = (max_time * t_max) - (t_max ** 2)
        dist_min = (max_time * t_min) - (t_min ** 2)
        num_winners = 1 + t_max - t_min - (1 if dist_max <= max_dist else 0) - (1 if dist_min <= max_dist else 0)
        num_ways *= num_winners
    
    return num_ways

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    # Build list of races
    races = parse_races(input_data)

    single_race = parse_races(input_data, True)

    num_winners = run_races(races)

    num_winners_single = run_races(single_race)

 

    return f"The product of number of ways to win is: {num_winners}." \
    + f"{os.linesep}\tThe number of ways to win the single race is: {num_winners_single}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()