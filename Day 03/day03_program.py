import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 03/day03_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 03/day03_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines

class PartNumber:
    def __init__(self, x_pos, y_pos, number, length):
        self.x_pos = x_pos - length
        self.y_pos = y_pos
        self.number = number
        self.length = length
        self.valid_part = False

    def __str__(self):
        return f"{self.number} @ ({self.x_pos}, {self.y_pos}) with length {self.length}."
    
    def __repr__(self):
        return str(self)
    
    def is_within_area(self, x, y):
        return self.x_pos - 1 <= x and self.x_pos + self.length >= x and self.y_pos - 1 <= y and self.y_pos + 1 >= y

    def is_valid_part(self, data_array):
        max_y = len(data_array)
        max_x = len(data_array[0])
        # Check if any character in the box surrounding this number is a symbol.
        x_range = range(max(0, self.x_pos - 1), min(self.x_pos + self.length + 1, max_x))
        y_range = range(max(0, self.y_pos - 1), min(self.y_pos + 2, max_y))
        for x in x_range:
            for y in y_range:
                test_char = data_array[y][x]
                if not test_char.isnumeric() and test_char != '.':
                    return True
        
        return False

def parse_schematic(data: list[str]) -> list[list[str]]:
    return [[c for c in line] for line in data]

def find_part_numbers(data_array):
    max_y = len(data_array)
    max_x = len(data_array[0])
    part_numbers = []
    current_number = ''
    for y in range(max_y):
        # Starting on a new line, reset the currrent number
        current_number = ''
        for x in range(max_x):
            curr_digit = data_array[y][x]
            # If this digit is numeric, add it to our current_number we're tracking.
            if curr_digit.isnumeric():
                current_number = current_number + curr_digit
                # If we're at the end of the line, we need to immediately add this part number
                if x == max_x - 1:
                    part_num = PartNumber(x, y, int(current_number), len(current_number))
                    part_numbers.append(part_num)
                    current_number = ''
            else:
                # Found the end of the number. Need to convert to int and add to our list.
                if len(current_number) > 0:
                    part_num = PartNumber(x, y, int(current_number), len(current_number))
                    part_numbers.append(part_num)
                    current_number = ''
    
    return part_numbers

def find_gears(input, part_numbers):
    gears: list[tuple[int,int]] = []
    gear_ratios = []
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == '*':
                gears.append((x, y))
    
    # have a list of possible gears. Now compare each position in gears with the positions in each part.
    for gear in gears:
        gear_parts = []
        for part in part_numbers:
            if part.is_within_area(gear[0], gear[1]):
                gear_parts.append(part.number)
        if len(gear_parts) == 2:
            gear_ratios.append(gear_parts[0] * gear_parts[1])
    
    return gear_ratios

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    input_array = parse_schematic(input_data)
    part_numbers = find_part_numbers(input_array)
    valid_parts = [pn.number for pn in part_numbers if pn.is_valid_part(input_array)]
    gears = find_gears(input_array, part_numbers)
    return f"The total sum of all part numbers is: {sum(valid_parts)}." \
    + f"{os.linesep}\tThe total sum of all gear ratios is: {sum(gears)}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()