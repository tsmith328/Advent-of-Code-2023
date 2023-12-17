import os
from enum import Enum
import math

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input_test.txt"
test_file = "C:/Users/Kory/Documents/Tyler Programs/Advent-of-Code-2023/Day 17/day17_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input.txt"
input_file = "C:/Users/Kory/Documents/Tyler Programs/Advent-of-Code-2023/Day 17/day17_input.txt"

def read_file(file_name: str) -> list[list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        return [l.strip() for l in file.readlines() if len(l.strip()) > 0]

class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

def build_field(file_data: list[list[str]]) -> dict[tuple[int,int],int]:
    field = dict()
    for y, line in enumerate(file_data):
        for x, char in enumerate(line):
            field[(x, y)] = int(char)
    
    return field

def get_diag_weight(field: dict[tuple[int,int],int]) -> int:
    """Gets weight of diagonal path as a baseline for comparing weights of other paths."""
    max_x = max([point[0] for point in field.keys()])
    max_y = max([point[1] for point in field.keys()])
    curr_x = 0
    curr_y = 0
    total_weight = 0
    while curr_x < max_x and curr_y < max_y:
        # Move right
        curr_x += 1
        weight = field[(curr_x, curr_y)]
        total_weight += weight
        # Move down
        curr_y += 1
        weight = field[(curr_x, curr_y)]
        total_weight += weight
    
    return total_weight

def get_unvisited_neighbors(field: dict[tuple[int,int], int], 
                            position: tuple[int,int], 
                            visited: list[tuple[int,int]],
                            dir_from: Direction,
                            need_to_turn: bool) -> list[tuple[int,int]]:
    neighbor_up = (position[0], position[1] - 1)
    neighbor_down = (position[0], position[1] + 1)
    neighbor_left = (position[0] - 1, position[1])
    neighbor_right = (position[0] + 1, position[1])
    neighbors = []
    if neighbor_up in field.keys() and neighbor_up not in visited and dir_from != Direction.NORTH and (dir_from != Direction.SOUTH or not need_to_turn):
        neighbors.append(neighbor_up)
    if neighbor_right in field.keys() and neighbor_right not in visited and dir_from != Direction.EAST and (dir_from != Direction.WEST or not need_to_turn):
        neighbors.append(neighbor_right)
    if neighbor_down in field.keys() and neighbor_down not in visited and dir_from != Direction.SOUTH and (dir_from != Direction.NORTH or not need_to_turn):
        neighbors.append(neighbor_down)
    if neighbor_left in field.keys() and neighbor_left not in visited and dir_from != Direction.WEST and (dir_from != Direction.EAST or not need_to_turn):
        neighbors.append(neighbor_left)
    
    return neighbors
    
def get_direction(point_from: tuple[int,int], point_to: tuple[int,int]) -> Direction:
    from_x, from_y = point_from
    to_x, to_y = point_to
    if from_x == to_x:
        if from_y > to_y:
            return Direction.SOUTH
        if from_y < to_y:
            return Direction.NORTH
        else:
            return None
    if from_y == to_y:
        if from_x > to_x:
            return Direction.EAST
        if from_x < to_x:
            return Direction.WEST
        else:
            return None
    return None

def find_best_path(field: dict[tuple[int,int],int], start: tuple[int,int], dest: tuple[int,int], best: int) -> list[tuple[int,int]]:
    visited = [start]
    steps_since_turn = 0
    best_weights = dict()
    frontier = []
    current = start
    dir_from = None
    curr_weight = 0
    prev = dict() # Stores nodes that gave min weight. Allows back-tracking.
    # initialized known weights from start to this node
    for point in field.keys():
        best_weights[point] = 0 if point == start else math.inf
    
    # Populate frontier with first neighbors and get best possible weight to each.
    neighbors = get_unvisited_neighbors(field, current, visited, dir_from, steps_since_turn >= 3)
    for item in neighbors:
        frontier.append(item)
        best_weights[item] = curr_weight + field[item]
        prev[item] = current

    while current != dest and frontier:
        # Sort the frontier
        frontier = sorted(frontier, key=lambda i: best_weights[i])

        # Get next-lowest spot and add to visited and path
        next = frontier.pop(0)
        if next == dest:
            current = dest
            break
        movement_dir = get_direction(prev[next], next)
        if movement_dir == dir_from:
            steps_since_turn += 1
        else:
            steps_since_turn = 0
            dir_from = movement_dir
        curr_weight = best_weights[current]
        current = next
        
        visited.append(current)

        # Update current path weight
        curr_weight += field[current]

        # Get available neighbors, add to our frontier, and update seen distances if lower
        neighbors = get_unvisited_neighbors(field, current, visited, dir_from, steps_since_turn >= 3)
        for neighbor in neighbors:
            if neighbor not in frontier:
                frontier.append(neighbor)
            possible_weight = curr_weight + field[neighbor]
            if best_weights[neighbor] is None or possible_weight < best_weights[neighbor]:
                best_weights[neighbor] = curr_weight + field[neighbor]
                prev[neighbor] = current
    
    # Should be at destination.
    if current == dest:
        path = [dest]
        node = prev[dest]
        while node != start:
            path.append(node)
            node = prev[node]
        return reversed(path)

    else:
        return []


def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    field = build_field(input_data)
    field_width = max([x[0] for x in field.keys()])
    field_height = max([x[1] for x in field.keys()])

    diag_weight = get_diag_weight(field)
    path = find_best_path(field, (0,0), (field_width, field_height), diag_weight)
    heat_loss = sum([field[point] for point in path])

    return f"The minimum heat lost is: {heat_loss}." \
          + f"{os.linesep}\tThe highest possible energy level is: {''}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()