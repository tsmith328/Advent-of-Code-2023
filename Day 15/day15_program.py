import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 15/day15_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 15/day15_input.txt"

def read_file(file_name: str) -> list[list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        return [l.strip() for l in file.readlines() if len(l.strip()) > 0]

def hash(data: str) -> int:
    hash_val = 0
    for char in data:
        hash_val += ord(char)
        hash_val *= 17
        hash_val = hash_val % 256
    
    return hash_val

def hash_steps(steps: list[str]) -> int:
    return sum(map(hash, steps))

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    hash_val = hash_steps(input_data.split(','))

    # Part 2:
    # 1. Create a hashmap/dictionary using hash function as key
    # 2. dict should be int -> list[Lens] or list[str]
    # 3. Look up which list to use. Then follow directions from step
    # 4. Traverse dict.items() to calculate focusing power.

    return f"The total hash value is: {hash_val}." \
          + f"{os.linesep}\tThe total weight after the spin cycle is: {''}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()