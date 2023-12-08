import os
from math import lcm

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 08/day08_input_test.txt"
test_file_2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 08/day08_input_test2.txt"
test_file_2 = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 08/day08_input_test_part2.txt"
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
    

def build_graph(nodes: list[str]) -> dict[str, tuple[str, str]]:
    graph = {}
    for node in nodes:
        node_name, children = node.split(" = ")
        children = tuple(children.strip("()").split(", "))
        graph[node_name] = children
    return graph

def follow_graph(graph: dict[str, tuple[str, str]], directions: str, starting_node: str = "AAA", ghostly: bool = False) -> int:
    num_steps = 0
    curr_nodes = [starting_node]
    end_nodes = ["ZZZ"] if not ghostly else [n for n in graph.keys() if n[-1] == "Z"]
    num_at_z = 0
    while num_at_z < len(curr_nodes):
        #print(f"Step #{num_steps}. Nodes at Z: {num_at_z}. CurrentNodes: {curr_nodes}.")
        for i, curr_node in enumerate(curr_nodes):
            curr_step = directions[num_steps % len(directions)]
            
            if curr_step == "L":
                curr_nodes[i] = graph[curr_node][0]
            else:
                curr_nodes[i] = graph[curr_node][1]
        num_at_z = sum([1 for n in curr_nodes if n in end_nodes])
        num_steps += 1
    
    return num_steps

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    directions, *nodes = input_data[:]

    graph = build_graph(nodes)

    num_steps = follow_graph(graph, directions)
    a_nodes = [node for node in graph.keys() if node[-1] == "A"]
    steps = []
    for node in a_nodes:
        steps.append(follow_graph(graph, directions, node, True))
    
    least_common = lcm(*steps)

    
    return f"The total steps to reach the end is: {num_steps}." \
    + f"{os.linesep}\tThe total steps to reach the end in a ghostly manner is: {least_common}."

def main() -> None:
    # Run test case
    print("Test Case 1:")
    #print("\t" + run_case(test_file))

    print("Test Case 2:")
    #print("\t" + run_case(test_file_2))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()
