import os
from enum import Enum

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 16/day16_input_test.txt"

input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 16/day16_input.txt"

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

class Beam:
    direction: Direction
    position: tuple[int,int]
    history: set[tuple[int,int]]

    def __init__(self, direction: Direction, position: tuple[int,int]):
        self.direction = direction
        self.position = position
        self.history = set()
    
    def move(self, field: list[list[str]]) -> list["Beam"]:
        """Moves the endpoint of this Beam based on its direction and current location"""
        spawn = None
        curr_x, curr_y = self.position
        max_y = len(field) - 1
        max_x = len(field[0]) - 1
        if self.direction == Direction.NORTH:
            if curr_y == 0:
                # At the top of the map and cannot move up anymore.
                # Return empty list to indicate we're done.
                return []
            # move up
            new_y = curr_y - 1
            self.position = (curr_x, new_y)

            # Determine next move
            next_char = field[new_y][curr_x]
            if next_char == '\\':
                # reflected west
                self.direction = Direction.WEST
            if next_char == '/':
                # reflected east
                self.direction = Direction.EAST
            if next_char == '-':
                # split. this beam goes west and the spawn goes east
                self.direction = Direction.WEST
                spawn = Beam(Direction.EAST, self.position)
            # Do nothing on | or .
                
        elif self.direction == Direction.WEST:
            if curr_x == 0:
                # At the far left of the map and cannot move.
                # Return empty list to indicate we're done.
                return []
            # Move left
            new_x = curr_x - 1
            self.position = (new_x, curr_y)

            # Determine next move
            next_char = field[curr_y][new_x]
            if next_char == '\\':
                # reflected north
                self.direction = Direction.NORTH
            if next_char == '/':
                # reflected south
                self.direction = Direction.SOUTH
            if next_char == '|':
                # split. go north and create new beam going south.
                self.direction = Direction.NORTH
                spawn = Beam(Direction.SOUTH, self.position)
            # Nothing on - or .

        elif self.direction == Direction.SOUTH:
            if curr_y == max_y:
                # At the bottom of the map and cannot move.
                # Return empty list to indicate we're done.
                return []
            # Move down
            new_y = curr_y + 1
            self.position = (curr_x, new_y)

            # Next move
            next_char = field[new_y][curr_x]
            if next_char == '\\':
                # reflected east
                self.direction = Direction.EAST
            if next_char == '/':
                # reflected west
                self.direction = Direction.WEST
            if next_char == '-':
                # split. go west and create new beam going east.
                self.direction = Direction.WEST
                spawn = Beam(Direction.EAST, self.position)
            # Nothing on | or .
                
        elif self.direction == Direction.EAST:
            if curr_x == max_x:
                # At the far right of the map and cannot move.
                # Return empty list to indicate we're done.
                return []
            # Move right
            new_x = curr_x + 1
            self.position = (new_x, curr_y)

            # Determine next move
            next_char = field[curr_y][new_x]
            if next_char == '\\':
                # reflected souuth
                self.direction = Direction.SOUTH
            if next_char == '/':
                # reflected north
                self.direction = Direction.NORTH
            if next_char == '|':
                # split. go north and create new beam going south.
                self.direction = Direction.NORTH
                spawn = Beam(Direction.SOUTH, self.position)
            # Nothing on - or .
        
        # After we move, we need to capture the current position in our history
        self.history.add(self.position)

        # Return the list of Beams that are active after this step. This might include a Beam split off from us.
        return [self] if spawn is None else [self, spawn]

    def state(self):
        return (self.position, self.direction)

def move_beams(field: list[list[str]], initial_position: tuple[int,int], initial_direction: Direction) -> set[tuple[int,int]]:
    beam = Beam(initial_direction, initial_position)
    beams = [beam] # Working list of beams that have to move
    beam_states = set() # history of beam states for tracking cycles.
    visited_locations = set()

    # Always work while we have a Beam we can move
    while beams:
        beam = beams.pop() # get the next Beam to move
        # capture the locations visited by this beam so far.
        visited_locations = visited_locations.union(beam.history)

        new_beams = beam.move(field) # Move it
        
        for new_beam in new_beams: # Will return a list of Beams after the move. Might be empty if the Beam hit the edge
            beam_state = new_beam.state() # Get the immutable state
            if beam_state not in beam_states: # If this is a new state
                beam_states.add(beam_state) # Save the state
                beams.append(new_beam) # return this beam to our work queue.
    
    return visited_locations

def build_field(data: list[str]) -> list[list[str]]:
    lines = []
    for line in data:
        new_line = [x for x in line]
        lines.append(new_line)
    return lines

def find_most_energy(field: list[list[str]]) -> int:
    max_x = len(field[0])
    max_y = len(field)
    from_north = [(p[0],p[1] - 1) for p in zip(range(max_x), [0] * max_x)]
    from_west = [(p[0] - 1,p[1]) for p in zip([0] * max_y, range(max_y))]
    from_south = [(p[0],p[1] ) for p in zip(range(max_x), [max_y] * max_x)]
    from_east = [(p[0] ,p[1]) for p in zip([max_x] * max_y, range(max_y))]

    max_energy = 0
   
    for point in from_north:
        print(f"Running from {point} going South.")
        energy = len(move_beams(field, point, Direction.SOUTH))
        if energy > max_energy:
            max_energy = energy
    
    for point in from_south:
        print(f"Running from {point} going North.")
        energy = len(move_beams(field, point, Direction.NORTH))
        if energy > max_energy:
            max_energy = energy
    
    for point in from_east:
        print(f"Running from {point} going West.")
        energy = len(move_beams(field, point, Direction.WEST))
        if energy > max_energy:
            max_energy = energy
    
    for point in from_west:
        print(f"Running from {point} going East.")
        energy = len(move_beams(field, point, Direction.EAST))
        if energy > max_energy:
            max_energy = energy
    
    return max_energy


def run_case(file_name: str) -> str:
    input_data = read_file(file_name)

    field = build_field(input_data)

    visited_locations = move_beams(field, (-1,0), Direction.EAST)

    best_energized_level = find_most_energy(field)

    return f"The number of spots energized is: {len(visited_locations)}." \
          + f"{os.linesep}\tThe highest possible energy level is: {best_energized_level}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))


if __name__ == "__main__":
    main()