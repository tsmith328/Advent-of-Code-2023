import os
from itertools import combinations


test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 11/day11_input_test.txt"

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
    
def build_universe(data_lines: list[str]) -> list[list[str]]:
    ret_data = []
    for line in data_lines:
        ret_data.append([x for x in line])
    return ret_data

def expand_universe(chart: list[list[str]], expansion_factor: int = 1) -> list[list[str]]:
    expanded_universe = []
    empty_columns, empty_rows = find_empty(chart)
    empty_line = [x for x in "." * ((len(empty_columns) * expansion_factor) + len(chart[0]))]
    for y, line in enumerate(chart):
        expanded_line = []
        for x, item in enumerate(line):
            expanded_line.append(item)
            if x in empty_columns:
                for t in range(expansion_factor):
                    expanded_line.append('.')
        expanded_universe.append(expanded_line)
        if y in empty_rows:
            for t in range(expansion_factor):
                expanded_universe.append(empty_line)

    return expanded_universe

def find_empty(chart: list[list[str]]) -> tuple[list[int], list[int]]:
    empty_rows = set(range(len(chart)))
    empty_columns = set(range(len(chart[0])))
    for y, line in enumerate(chart):
        for x, item in enumerate(line):
            if item == "#":
                # remove this row and column from the lists of empty
                empty_rows -= set([y])
                empty_columns -= set([x])
    
    return (list(empty_columns), list(empty_rows))

def find_galaxies(chart: list[list[str]]) -> list[tuple[int,int]]:
    galaxies = []
    for y, line in enumerate(chart):
        for x, item in enumerate(line):
            if item == "#":
                galaxies.append((x, y))
    return galaxies

def get_pairs(items: list[tuple[int,int]]) -> list[tuple[tuple[int,int],tuple[int,int]]]:
    return list(combinations(items, 2))

def get_distances(galaxies: list[tuple[tuple[int,int],tuple[int,int]]]) -> list[int]:
    distances = []
    for galaxy1, galaxy2 in galaxies:
        g1_x, g1_y = galaxy1
        g2_x, g2_y = galaxy2
        distance = abs(g1_x - g2_x) + abs(g1_y - g2_y)
        distances.append(distance)
    
    return distances

def get_distances_2(galaxies: list[tuple[tuple[int,int],tuple[int,int]]], empty_rows, empty_columns, expansion_factor) -> list[int]:
    distances = []
    for galaxy1, galaxy2 in galaxies:
        g1_x, g1_y = galaxy1
        g2_x, g2_y = galaxy2
        empty_rows_between = items_between(empty_rows, g1_y, g2_y)
        empty_cols_between = items_between(empty_columns, g1_x, g2_x)
        distance = abs(g1_x - g2_x) + (len(empty_cols_between) * (expansion_factor)) + abs(g1_y - g2_y) + (len(empty_rows_between) * expansion_factor)
        distances.append(distance)
    
    return distances

def items_between(items, bound1, bound2):
    ret = []
    lower = min(bound1, bound2)
    upper = max(bound1, bound2)
    for item in items:
        if item >= lower and item <= upper:
            ret.append(item)
    
    return ret

def run_case2(file_name: str) -> str:
    cases = []
    for expansion_factor in [2,10,100,1_000_000]:

        input_data = read_file(file_name)

        universe = build_universe(input_data)
        empty_cols, empty_rows = find_empty(universe)
        
        galaxies = find_galaxies(universe)
        galaxy_pairs = get_pairs(galaxies)
        galaxy_distances = get_distances_2(galaxy_pairs, empty_rows, empty_cols, expansion_factor - 1)

        cases.append(f"The sum of all distances between all galaxy pairs after expanding by {expansion_factor} is: {sum(galaxy_distances)}.")


    return f"{os.linesep}\t".join(cases)


def run_case(file_name: str) -> str:
    cases = []
    for expansion_factor in [2]:

        input_data = read_file(file_name)

        universe = build_universe(input_data)
        universe = expand_universe(universe, expansion_factor - 1)

        galaxies = find_galaxies(universe)
        galaxy_pairs = get_pairs(galaxies)
        galaxy_distances = get_distances(galaxy_pairs)

        cases.append(f"The sum of all distances between all galaxy pairs after expanding by {expansion_factor} is: {sum(galaxy_distances)}.")


    return f"{os.linesep}\t".join(cases)

def main() -> None:
    # Run test case
    print("Test Case 1:")
    #run_case(test_file)
    print("\t" + run_case2(test_file))
    
    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case2(input_file))


if __name__ == "__main__":
    main()