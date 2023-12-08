import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 08/day08_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 08/day08_input.txt"

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
    
    
    return f"The total steps to reach the end is: {''}." \
    + f"{os.linesep}\tThe total winnings of my hand when playing with Jokers is: {''}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()
