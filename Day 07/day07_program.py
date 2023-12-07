import os
from math import floor
from math import ceil
from enum import Enum

test_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 07/day07_input_test.txt"
input_file = "E:/Documents/Advent of Code/Advent-of-Code-2023/Day 07/day07_input.txt"

def read_file(file_name: str) -> list[str]:
    """
    Reads a file and returns a list of the lines in the file, 
    removing any lines that are purely whitespace or are empty.

    The file is closed when this function returns.
    """
    with open(file_name) as file:
        file_lines = [l.strip() for l in file.readlines() if len(l.strip()) > 0]
        return file_lines

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
class HandType(OrderedEnum):
    
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

class Card(OrderedEnum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2


class Hand:
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"Bet {self.bet} on {self.cards} which is a {self.type}."

    def __init__(self, cards, bet):
        self.bet = bet
        self.cards = Hand.get_cards(cards)
        self.type = Hand.get_type(self.cards)

    def get_type(cards: list[Card]) -> HandType:
        return HandType.FOUR_OF_A_KIND

    def get_cards(cards: str) -> list[Card]:
        my_cards = []
        my_card = None
        for card in cards:
            if card == "A":
                my_card = Card.ACE
            elif card == "K":
                my_card = Card.KING
            elif card == "Q":
                my_card = Card.QUEEN
            elif card == "J":
                my_card = Card.JACK
            elif card == "T":
                my_card = Card.TEN
            elif card == "9":
                my_card = Card.NINE
            elif card == "8":
                my_card = Card.EIGHT
            elif card == "7":
                my_card = Card.SEVEN
            elif card == "6":
                my_card = Card.SIX
            elif card == "5":
                my_card = Card.FIVE
            elif card == "4":
                my_card = Card.FOUR
            elif card == "3":
                my_card = Card.THREE
            elif card == "2":
                my_card = Card.TWO

            my_cards.append(my_card)
        return my_cards

    def is_stronger(self, other):
        if self.type > other.type:
            return True
        if self.type < other.type:
            return False
        for i in range(self.cards):
            my_card = self.cards[i]
            their_card = self.cards[i]
            if my_card > their_card:
                return True
            if my_card < their_card:
                return False
        
        return False
        
def build_hands(input_str: list[str]) -> list[Hand]:
    return [Hand(hand.split()[0], int(hand.split()[1])) for hand in input_str]

def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    hands = build_hands(input_data)

 

    return f"The product of number of ways to win is: {''}." \
    + f"{os.linesep}\tThe number of ways to win the single race is: {''}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()