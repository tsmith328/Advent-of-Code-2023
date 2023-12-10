import os
from math import ceil


test_file1 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test1.txt"
test_file2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test2.txt"
test_file3 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test3.txt"
test_file4 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test4.txt"
test_file5 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test5.txt"
test_file6 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input_test6.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 10/day10_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines
    
def build_pipes(data_lines: list[str]) -> list[list[str]]:
    maze = []
    for line in data_lines:
        maze_line = [x for x in line]
        maze.append(maze_line)
    return maze

def find_start(maze: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "S":
                return (x, y)

def get_next_position(curr_x: int, curr_y: int, prev_x: int, prev_y: int, maze: list[list[str]]) -> tuple[int, int]:
    if curr_y == 0:
        neighbor_up = ''
    else:
        neighbor_up = maze[curr_y - 1][curr_x]

    if curr_x == 0:
        neighbor_left = ''
    else:
        neighbor_left = maze[curr_y][curr_x - 1]

    if curr_x >= len(maze[curr_y]) - 1:
        neighbor_right = ''
    else:
        neighbor_right = maze[curr_y][curr_x + 1]

    if curr_y >= len(maze) - 1:
        neighbor_down = ''
    else:
        neighbor_down = maze[curr_y + 1][curr_x]

    curr_char = maze[curr_y][curr_x]
    next_valid = False

    if curr_char == "|":
        next_x = curr_x
        next_y = curr_y - 1
        if next_y == prev_y and next_x == prev_x:
            next_y = curr_y + 1
    if curr_char == "-":
        next_x = curr_x - 1
        next_y = curr_y
        if next_y == prev_y and next_x == prev_x:
            next_x = curr_x + 1
    if curr_char == "L":
        next_x = curr_x + 1
        next_y = curr_y
        if next_y == prev_y and next_x == prev_x:
            next_x = curr_x
            next_y = curr_y - 1
    if curr_char == "J":
        next_x = curr_x - 1
        next_y = curr_y
        if next_y == prev_y and next_x == prev_x:
            next_x = curr_x
            next_y = curr_y - 1
    if curr_char == "7":
        next_x = curr_x - 1
        next_y = curr_y
        if next_y == prev_y and next_x == prev_x:
            next_x = curr_x
            next_y = curr_y + 1
    if curr_char == "F":
        next_x = curr_x + 1
        next_y = curr_y
        if next_y == prev_y and next_x == prev_x:
            next_x = curr_x
            next_y = curr_y + 1
    if curr_char == "S": # Special case for starting position
        if neighbor_up == "|" :
            next_x = curr_x
            next_y = curr_y - 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_up == "F" and not next_valid:
            next_x = curr_x + 1
            next_y = curr_y - 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_up == "7"  and not next_valid:
            next_x = curr_x - 1
            next_y = curr_y - 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_left == "F" and not next_valid:
            next_x = curr_x - 1
            next_y = curr_y + 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_left == "-"  and not next_valid:
            next_x = curr_x - 1
            next_y = curr_y
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_left == "L" and not next_valid:
            next_x = curr_x - 1
            next_y = curr_y - 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_right == "-" and not next_valid:
            next_x = curr_x + 1
            next_y = curr_y
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_right == "J" and not next_valid:
            next_x = curr_x + 1
            next_y = curr_y - 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_right == "7" and not next_valid:
            next_x = curr_x + 1
            next_y = curr_y + 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_down == "J" and not next_valid:
            next_x = curr_x - 1
            next_y = curr_y + 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_down == "|" and not next_valid:
            next_x = curr_x
            next_y = curr_y + 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
        if neighbor_down == "L" and not next_valid:
            next_x = curr_x + 1
            next_y = curr_y + 1
            # Make sure we aren't backtracking
            next_valid = next_x != prev_x or next_y != prev_y
    
    return (next_x, next_y)

def traverse_maze(maze: list[list[str]], start: tuple[int,int]) -> dict[tuple[int,int], tuple[int,int]]:
    pipe_dict = {}
    curr_x = start[0]
    curr_y = start[1]
    prev_x = curr_x
    prev_y = curr_y

    # Need a special case if we're on the S: find a neighbor that points to the S
    next_x, next_y = get_next_position(curr_x, curr_y, prev_x, prev_y, maze)
    
    pipe_dict[(curr_x, curr_y)] = (next_x, next_y)
    curr_x = next_x
    curr_y = next_y

    while True:
        # Get next x and y based on character at this location.
        # Also need to make sure we're traversing one way...don't want to accidentally turn around mid-pipe
        next_x, next_y = get_next_position(curr_x, curr_y, prev_x, prev_y, maze)
        next_char = maze[next_y][next_x]
        pipe_dict[(curr_x, curr_y)] = (next_x, next_y)
        prev_x, prev_y = curr_x, curr_y
        curr_x, curr_y = next_x, next_y
        if next_char == "S":
            # Completed the loop
            return pipe_dict
        
def find_vertices(points: list[tuple[int,int]]) -> list[tuple[int,int]]:
    vertices = []
    for i in range(len(points)):
        # If x of next and y of next changes, we are at a vertex
        prev_x, prev_y = points[i - 1]
        next_x, next_y = points[(i + 1) % len(points)]
        if prev_x != next_x and prev_y != next_y:
            vertices.append(points[i])
    
    return vertices

def get_edges(verts):
    edges = []
    for vert1, vert2 in zip(verts, verts[1:] + [verts[0]]):
        edge_x, edge_y = vert2[0] - vert1[0], vert2[1] - vert1[1]
        edges.append((edge_x, edge_y))
    
    return edges
        
def scale_vertices(verts: list[tuple[int, int]]) -> list[tuple[int,int]]:
    # Adds 1 to the length of each edge on this polygon so area math works correctly.
    edges = get_edges(verts)
    # Scale edges
    edges = list(map(lambda point: (0 if point[0] == 0 else point[0] + 1 if point[0] > 0 else point[0] - 1, 0 if point[1] == 0 else point[1] + 1 if point[1] > 0 else point[1] - 1), edges))

    new_verts = [verts[0]]
    for i, edge in enumerate(edges):
        next_vert = tuple((sum(x) for x in zip(new_verts[-1], edge)))
        if not next_vert in new_verts:
            new_verts.append(next_vert)
    # Remove duplicates
   
    return new_verts

def get_area(verts):
    area = 0
    for i in range(len(verts)):
        j = (i + 1) % len(verts)
        area += (verts[i][0] * verts[j][1])
        area -= (verts[i][1] * verts[j][0])
    
    return area / 2

def is_inside(point, pipe, max_x, max_y, maze) -> bool:
    # If we are on the line, we don't count it.
    if point in pipe:
        return False
    
    point_x, point_y = point
    # Test by moving in +x from point to "infinity" (end of maze)
    crossings = 0
    for dx in range(1, max_x - point_x):
        if (point_x + dx, point_y) in pipe:
            if maze[point_y][point_x + dx] == '-':
                crossings += 0
            elif maze[point_y][point_x + dx] in ('L', '7'):
                crossings += 0.5
            elif maze[point_y][point_x + dx] in ('J', 'F'):
                crossings -= 0.5
            else:
                crossings += 1

    return crossings % 2 == 1


def points_inside(maze, pipe) -> int:
    area = 0
    max_y = len(maze)
    for y in range(max_y):
        max_x = len(maze[y])
        for x in range(max_x):
            area += 1 if is_inside((x, y), pipe, max_x, max_y, maze) else 0
            #area += 1 if is_point_in_path(x, y, pipe) else 0
    
    return area

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    maze = build_pipes(input_data)

    start_x, start_y = find_start(maze)

    pipe = traverse_maze(maze, (start_x, start_y))
    vertices = find_vertices(list(pipe.keys()))
    area = points_inside(maze, pipe)
    """ 
    vertices = scale_vertices(vertices)
    area1 = get_area(vertices)"""
    
    return f"The furthest point is this many steps away from the start: {ceil(len(pipe.keys()) / 2)}." \
    + f"{os.linesep}\tThe total area of this pipe is: {area}."

def main() -> None:
    # Run test case
    print("Test Case 1 (Should be 1):")
    print("\t" + run_case(test_file1))

    print("Test Case 2 (Should be 1):")
    print("\t" + run_case(test_file2))

    print("Test Case 3 (Should be 4):")
    print("\t" + run_case(test_file3))

    print("Test Case 4 (Should be 4):")
    print("\t" + run_case(test_file4))

    print("Test Case 5 (Should be 8):")
    print("\t" + run_case(test_file5))

    print("Test Case 6 (Should be 10):")
    print("\t" + run_case(test_file6))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()
