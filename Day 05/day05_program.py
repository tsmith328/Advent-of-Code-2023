import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 05/day05_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 05/day05_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.read().split('\n' * 2) if len(l.strip()) > 0]
        return file_lines

def parse_seeds(seed_list: str) -> list[int]:
    return [int(seed) for seed in seed_list.split(": ")[1].split()]

def parse_map(mapping: str) -> dict[tuple[int, int], int]:
    maps = mapping.splitlines()[1:] # Drop map header
    map_dict = {}
    for mapping in maps:
        destination_start, source_start, length = map(int, mapping.split())
        diff = destination_start - source_start
        source_end = source_start + length - 1
        map_dict[(source_start, source_end)] = diff

    return map_dict

def build_seed_ranges(seeds: list[int]):
    new_seeds = []
    for i in range(0, len(seeds), 2):
        for j in range(seeds[i + 1]):
            yield seeds[i] + j
    
    #return new_seeds

def run_maps(seeds, maps) -> int:
    min_location = -1

    for seed in seeds:
        spot = seed
        for mapping in maps:
            for (range_start, range_end), diff in mapping.items():
                if spot >= range_start and spot <= range_end:
                    spot += diff
                    break
        
        if min_location < 0 or spot < min_location:
            min_location = spot
    
    return min_location

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    # Build list of seeds
    seeds = parse_seeds(input_data[0])

    # Build Maps
    maps = [parse_map(data) for data in input_data[1:]]

    # Build big seed list
    seeds2 = build_seed_ranges(seeds)

    locations1 = run_maps(seeds, maps)
    locations2 = run_maps(seeds2, maps)

    return f"The lowest location number for the small number of seeds is: {locations1}." \
    + f"{os.linesep}\tThe lowest location number for the stupid number of seeds is: {locations2}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()