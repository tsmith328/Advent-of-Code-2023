import os
from itertools import combinations
from functools import cache

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 13/day13_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 13/day13_input.txt"

def read_file(file_name: str) -> list[list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        groups = [grp.strip() for grp in file.read().split('\n' * 2)]
        new_groups = []
        for group in groups:
            new_groups.append([l.strip() for l in group.splitlines() if len(l.strip()) > 0])
        return new_groups
    
def build_field(input_data: list[str]) -> tuple[list[str], list[str]]:
    field = []
    for line in input_data:
        field.append([x for x in line])
    
    # Transposes a 2d array
    field_t = list(map(list, zip(*field)))

    field = [''.join([x for x in line]) for line in field]
    field_t = [''.join([x for x in line]) for line in field_t]

    return field, field_t

def find_reflection_row(field: list[list[str]]) -> set[int]:
    found_rows = [field[0]] # Start with first row added
    reflections = set()
    for i in range(1, len(field)):
        before = field[:i]
        after = field[i:]
        compare = list(zip(reversed(before), after))
        ok = all([x[0] == x[1] for x in compare])
        if ok:
            reflections.add(i)
    return reflections

def build_smudges(field: list[list[str]]) -> list[list[str]]:
    options = []
    total_vals = len(field) * len(field[0])
    for i in range(total_vals):
        new_field = []
        i_row = int(i / len(field[0]))
        i_col = i % len(field[0])
        for j, line in enumerate(field):
            new_line = []
            for k, char in enumerate(line):
                if j == i_row and k == i_col:
                    new_line.append('#' if char == '.' else '.')
                else:
                    new_line.append(char)
            new_field.append(''.join(new_line))
        options.append(new_field)
    return options

def run_case(file_name: str) -> str:
    input_groups = read_file(file_name)
    total_val = 0
    total_val_smudged = 0
    for input_data in input_groups:

        field, field_t = build_field(input_data)
        
        reflection_row = find_reflection_row(field)
        reflection_col = find_reflection_row(field_t)

        if len(reflection_row) == 0:
            reflection_val = list(reflection_col)[0]
        else:
            reflection_val = 100 * list(reflection_row)[0]

        field_smudged = build_smudges(field)
        field_t_smudged = build_smudges(field_t)

        for i in range(len(field_smudged)):
            smudged_reflection_row = find_reflection_row(field_smudged[i])
            smudged_reflection_col = find_reflection_row(field_t_smudged[i])
            ref_row = smudged_reflection_row.difference(reflection_row)
            ref_col = smudged_reflection_col.difference(reflection_col)
            smudged_val = 0
            if len(ref_row) > 0:
                smudged_val = 100 * list(ref_row)[0]
            elif len(ref_col) > 0:
                smudged_val = list(ref_col)[0]
            total_val_smudged += smudged_val
            if smudged_val > 0:
                break

        total_val += reflection_val

    return f"The total reflection value is: {total_val}." \
          + f"{os.linesep}\tThe total smudged reflection value is: {total_val_smudged}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()