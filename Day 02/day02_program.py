from functools import reduce
import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 02/day02_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 02/day02_input.txt"



class Game:
    def __init__(self, game_num: int):
        self.game_num = game_num
        self.pulls = []
    
    class Pull:
        def __init__(self, num_red: int, num_green: int, num_blue: int):
            self.num_red = num_red
            self.num_green = num_green
            self.num_blue = num_blue
        
        def __str__(self) -> str:
            return f"({self.num_red} red, {self.num_green} green, {self.num_blue} blue)"
        
        def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
            return self.num_red <= max_red and self.num_green <= max_green and self.num_blue <= max_blue
    
    def add_pull(self, num_red: int, num_green: int, num_blue: int) -> None:
        self.pulls.append(Game.Pull(num_red, num_green, num_blue))
    
    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return all([pull.is_possible(max_red, max_green, max_blue) for pull in self.pulls])
    
    def fewest_needed(self):
        return (max([p.num_red for p in self.pulls]), max([p.num_green for p in self.pulls]), max([p.num_blue for p in self.pulls]))
    
    def game_power(self):
        return reduce(lambda x,y: x*y, self.fewest_needed(), 1)

    def __str__(self) -> str:
        return f"Game {self.game_num}: Pulls: [{', '.join([str(p) for p in self.pulls])}]"

def read_file(file_name: str) -> dict[int, list[str]]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        games = {}
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        for line in file_lines:
            game_num = int(line.split(": ")[0].split()[1])
            pull_list = line.split(": ")[1].split("; ")
            games[game_num] = pull_list
        
        return games

def parse_games(games_list: dict[int, list[str]]) -> list[Game]:
    games = []
    for game_num, pulls in games_list.items():
        game = Game(game_num)
        for pull in pulls:
            pull_colors = pull.split(", ")
            num_red = 0
            num_green = 0
            num_blue = 0
            for pull_color in pull_colors:
                num, color = pull_color.split(" ")
                num = int(num)
                if color == "red":
                    num_red = num
                if color == "green":
                    num_green = num
                if color == "blue":
                    num_blue = num
            
            game.add_pull(num_red, num_green, num_blue)
        games.append(game)
    
    return games

def get_valid_games(games: list[Game], max_red: int, max_green: int, max_blue: int) -> int:
    """
    Gets the total of the Game IDs of games that are valid given the max red, green, and blue blocks.
    """

    return sum([g.game_num for g in games if g.is_possible(max_red, max_green, max_blue)])

def get_game_power(games: list[Game]) -> int:
    return sum([g.game_power() for g in games])

def run_case(file_name: str, max_red: int = 12, max_green: int = 13, max_blue: int = 14) -> str:
    games_list = read_file(file_name)
    games = parse_games(games_list)
    valid_game_total = get_valid_games(games, max_red, max_green, max_blue)
    game_power = get_game_power(games)
    return f"The sum of the possible Game #s is {valid_game_total}." + \
    os.linesep + f"\tThe sum of the power of all Games is {game_power}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()