test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 01/day01_input_test.txt"
test_file_2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 01/day01_input_test_2.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 01/day01_input.txt"

number_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,"six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines
    
def calculate_calibration_value(input_data: list[str], numerals_only: bool = True) -> int:
    """
    Parses a line of text to find numerals. Takes the first and last numeral to form a 2-digit number.

    These numbers are summed and a total for all input lines is returned.

    Set numerals_only to True to only check for Arabic numeral versions of numbers. Set to False to also check for number 'names' ('one', 'two', etc.).
    """
    cal_values = []
    # Loop through each line
    for line in input_data:
        left_digit = -1
        right_digit = -1
        # Check each character in the line.
        for idx, char in enumerate(line):
            # If we are checking for word numbers, check for those.
            number_found = False
            word_number = 0
            if not numerals_only:
                # Check each number in the dictionary to see if it's in the remaining part of the line.
                for number_word in number_dict.keys():
                    if line.find(number_word, idx, idx + len(number_word)) != -1:
                        number_found = True
                        word_number = number_dict[number_word]
                        break

            # If the character is a numeral, use it.
            if char.isnumeric():
                right_digit = int(char)
            elif number_found:
                right_digit = word_number

            # Only set left_digit if it's not set already.
            if left_digit == -1:
                if char.isnumeric():
                    left_digit = int(char)
                elif number_found:
                    left_digit = word_number
        cal_values.append(left_digit * 10 + right_digit)
    
    return sum(cal_values)
        

def main() -> None:
    # Run the test case for Part 1
    test_data = read_file(test_file)
    cal_value = calculate_calibration_value(test_data)
    print(f"The sum of all calibration values in the test case 1 is {cal_value}.")

    # Run the actual case for Part 1
    input_data = read_file(input_file)
    cal_value = calculate_calibration_value(input_data)
    print(f"The sum of all calibration values in Part 1 is {cal_value}.")

    test_data = read_file(test_file_2)
    cal_value = calculate_calibration_value(test_data, False)
    print(f"The sum of all calibration values in the test case 2 is {cal_value}.")

    # Run the actual case for Part 2
    input_data = read_file(input_file)
    cal_value = calculate_calibration_value(input_data, False)
    print(f"The sum of all calibration values in Part 2 is {cal_value}.")

if __name__ == "__main__":
    main()