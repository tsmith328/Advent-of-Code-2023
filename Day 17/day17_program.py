import os
from enum import Enum
import math

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 17/day17_input.txt"

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

def get_unvisited_neighbors(field: dict[tuple[int,int], int], 
                            position: tuple[int,int], 
                            visited: list[tuple[int,int]],
                            dir_from: Direction,
                            need_to_turn: bool) -> list[tuple[int,int]]:
    neighbor_up = ((position[0][0], position[0][1] - 1), Direction.SOUTH)
    neighbor_down = ((position[0][0], position[0][1] + 1), Direction.NORTH)
    neighbor_left = ((position[0][0] - 1, position[0][1]), Direction.EAST)
    neighbor_right = ((position[0][0] + 1, position[0][1]), Direction.WEST)
    neighbors = []
    if neighbor_up[0] in field.keys() and neighbor_up not in visited and dir_from != Direction.NORTH and (dir_from != Direction.SOUTH or not need_to_turn):
        neighbors.append(neighbor_up)
    if neighbor_right[0] in field.keys() and neighbor_right not in visited and dir_from != Direction.EAST and (dir_from != Direction.WEST or not need_to_turn):
        neighbors.append(neighbor_right)
    if neighbor_down[0] in field.keys() and neighbor_down not in visited and dir_from != Direction.SOUTH and (dir_from != Direction.NORTH or not need_to_turn):
        neighbors.append(neighbor_down)
    if neighbor_left[0] in field.keys() and neighbor_left not in visited and dir_from != Direction.WEST and (dir_from != Direction.EAST or not need_to_turn):
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

def get_smallest(from_list: list[tuple[int,int]], weights: dict[tuple[int,int], int]) -> tuple[int,int]:
    min_point = from_list[0]
    min_val = math.inf
    for item in from_list:
        if weights[item] < min_val:
            min_point = item
            min_val = weights[item]
    
    return min_point

def find_path(field: dict[tuple[int,int],int], start: tuple[int,int], dest: tuple[int,int]) -> list[tuple[int,int]]:
    # Prepare Dijkstra's Alg.
    unvisited = list(zip(list(field.keys()) * 4, [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST] * len(field.keys())))
    weights = {point: 0 if point[0] == start else math.inf for point in unvisited}
    prev = {point: None for point in unvisited}
    runs = {point: 0 for point in unvisited}
    dirs = {point: None for point in unvisited}

    # Continue until list of unvisited nodes is empty
    while unvisited:
        # Sort queue by weight and get first item (min weight)
        next_point = get_smallest(unvisited, weights)
        unvisited.remove(next_point)
        current = next_point
        if current == dest: # Break early if we are at the destination node.
            break
        
        neighbors = get_unvisited_neighbors(field, current, [], dirs[current], runs[current] >= 3)

        for neighbor in neighbors:
            if neighbor in unvisited:
                new_weight = weights[current] + field[neighbor[0]]
                if new_weight < weights[neighbor]:
                    weights[neighbor] = new_weight
                    prev[neighbor] = current
                    new_dir = neighbor[1]
                    dirs[neighbor] = new_dir
                    # Check if we need to reset our run count.
                    if new_dir == dirs[current]:
                        runs[neighbor] = 1 + runs[current]
                    else:
                        runs[neighbor] = 1
    
    # Build path back to start
    path_first = [x for x, v in prev.items() if v is not None and x[0] == dest][0]
    path = [path_first]
    curr = path_first
    while True:
        next_node = prev[curr]
        if next_node[0] == start:
            break
        path.append(next_node)
        curr = next_node
    return list(reversed(path))

def find_best_path(field: dict[tuple[int,int],int], start: tuple[int,int], dest: tuple[int,int]) -> list[tuple[int,int]]:
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
            steps_since_turn = 1
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

    #path = find_best_path(field, (0,0), (field_width, field_height))
    path = find_path(field, (0, 0), (field_width, field_height))
    heat_loss = sum([field[point[0]] for point in path])

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