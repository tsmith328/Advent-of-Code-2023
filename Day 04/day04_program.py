import os

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 04/day04_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 04/day04_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines

class Card:
    def __init__(self, card_num: int, winning_numbers: list[int], play_numbers: list[int]):
        self.card_num = card_num
        self.winning_numbers = winning_numbers
        self.play_numbers = play_numbers
    
    def score(self):
        wins = self.num_winners()
        score = 2 ** (wins - 1) if wins > 0 else 0        
        return score
    
    def num_winners(self):
        return sum([1 for play in self.play_numbers if play in self.winning_numbers])
    
def parse_cards(input: list[str]) -> list[Card]:
    cards = []
    for line in input:
        card_num, plays = line.split(": ")
        card_num = int(card_num.split()[1]) # Card X
        winning_nums, play_nums = plays.split(" | ")
        winners = [int(x) for x in winning_nums.split()]
        plays = [int(x) for x in play_nums.split()]
        cards.append(Card(card_num, winners, plays))
    
    return cards

def explode_cards(input: list[Card]) -> int:
    # Build initial dictionary
    card_dict = {card.card_num: 1 for card in input}
    for card_num in range(len(card_dict.keys())):
        num_winners = input[card_num].num_winners() # the Card at the ith index in the list is the Card with card_num = i + 1
        for i in range(num_winners):
            card_dict[card_num + i + 2] = card_dict[card_num + i + 2] + card_dict[card_num + 1]
    
    return sum([val for val in card_dict.values()])

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    cards = parse_cards(input_data)

    exploded_cards = explode_cards(cards)

    return f"The total points all cards are worth is: {sum([card.score() for card in cards])}." \
    + f"{os.linesep}\tThe total number of scratchcards we end up with is: {exploded_cards}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()