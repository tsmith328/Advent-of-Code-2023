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
    for i in range(0, len(seeds), 2):
        for j in range(seeds[i + 1]):
            yield seeds[i] + j

def build_seed_ranges_better(seeds: list[int]):
    return [(seed_start, seed_end + seed_start - 1) for seed_start, seed_end in zip(seeds[::2], seeds[1::2])]

def run_maps_better(seeds, maps) -> int:
    if len(maps) == 0:
        # Base case. no more maps so just take smallest starting seed value
        return min([seed[0] for seed in seeds])
    mapping = maps.pop(0) # will remove current map from list.
    new_seeds = set()
    for (seed_start, seed_end) in seeds:
        seed_mapped = False
        for (map_start, map_end) in mapping.keys():
            diff = mapping[(map_start, map_end)]
            if has_overlap((seed_start, seed_end), (map_start, map_end)):
                # Do stuff
                # 4 cases:
                #   Seeds starts outside map range and ends inside map range: break into 2 ranges
                #   Seeds starts inside map range and ends outside map range: break into 2 ranges
                #   Seeds starts inside map range and ends inside map range: keep as one range, but move it
                #   Seeds starts outside map range and ends outside map range: break into 3 ranges
                seed_mapped = True
                if seed_start >= map_start and seed_end <= map_end:
                    # Case 3. Just need to move the seed start and end
                    new_seed_start = seed_start + diff
                    new_seed_end = seed_end + diff
                    new_seeds.add((new_seed_start, new_seed_end))
                elif seed_start < map_start and seed_end >= map_start and seed_end <= map_end:
                    # Case 1
                    boundary = map_start
                    new_seed1 = (seed_start, boundary - 1)
                    new_seed2 = (boundary + diff, seed_end + diff)
                    new_seeds.add(new_seed1)
                    new_seeds.add(new_seed2)
                elif seed_start <= map_end and seed_end > map_end and seed_start >= map_start:
                    # Case 2
                    boundary = map_end
                    new_seed1 = (seed_start + diff, boundary + diff)
                    new_seed2 = (boundary + 1, seed_end)
                    new_seeds.add(new_seed1)
                    new_seeds.add(new_seed2)
                elif seed_start < map_start and seed_end > map_end:
                    # Case 4
                    new_seed1 = (seed_start, map_start - 1)
                    new_seed2 = (map_start + diff, map_end + diff)
                    new_seed3 = (map_end + 1, seed_end)
                    new_seeds.add(new_seed1)
                    new_seeds.add(new_seed2)
                    new_seeds.add(new_seed3)
                else:
                    seed_mapped = False
        if seed_mapped == False:
            new_seeds.add((seed_start, seed_end))
    # Done processing all seeds at this step. Recurse to move to next map
    return run_maps_better(new_seeds, maps) # map list had current level popped off.
    
def has_overlap(range1, range2) -> bool:
    start1, end1 = range1
    start2, end2 = range2

    return start1 <= end2 and start2 <= end1

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
    #seeds2 = build_seed_ranges(seeds)
    # Build list of seed ranges
    seeds2 = build_seed_ranges_better(seeds)
    seeds2 = set(seeds2)

    locations1 = run_maps(seeds, maps)
    locations2 = run_maps_better(seeds2, maps)
    #locations2 = run_maps(seeds2, maps)

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