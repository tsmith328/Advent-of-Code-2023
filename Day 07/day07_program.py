import os
from math import floor
from math import ceil
from enum import Enum
from itertools import product

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
    JOKER = 1


class Hand:
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"Bet {self.bet} on {self.cards} which is a {self.type}."

    def __init__(self, cards, bet, has_jokers):
        self.bet = bet
        self.has_jokers = has_jokers
        self.cards = Hand.get_cards(cards, has_jokers)
        self.type = Hand.get_type(self.cards, has_jokers)

    def get_type(cards: list[Card], has_joker: bool) -> HandType:
        if has_joker and any([True for x in cards if x == Card.JOKER]):
            # Only need to run this if we actually have a joker.
            best_type = HandType.HIGH_CARD
            non_joker_cards = [card for card in Card if card != Card.JOKER and card != Card.JACK]
            all_hands = product(non_joker_cards, repeat = 5) # get all possible hands.
            try_hands = []
            for hand in list(all_hands):
                ok = True
                # Check to see if all cards line up except Js.
                for i, card in enumerate(hand):
                    if cards[i] != Card.JOKER: # If original card is a Joker, don't need to check anything.
                        if cards[i] != card:
                            ok = False
                            break
                if ok:
                    try_hands.append(hand)
            
            for hand in try_hands:
                # Try each possible hand and get highest type
                try_type = Hand.get_type(hand, False)
                if try_type > best_type:
                    best_type = try_type
            
            return best_type

        # Do something with Jokers. Recursive?
        card_dict = {card: len(list(filter(lambda c: c == card, cards))) for card in set(cards)}
        # 5 of a kind?
        if len(set(cards)) == 1:
            return HandType.FIVE_OF_A_KIND
        
        most_cards = max(card_dict.values())
        least_cards = min(card_dict.values())
        if most_cards == 4:
            return HandType.FOUR_OF_A_KIND
        if most_cards == 3 and least_cards == 2:
            return HandType.FULL_HOUSE
        if most_cards == 3 and least_cards < 2:
            return HandType.THREE_OF_A_KIND
        if most_cards == 1:
            return HandType.HIGH_CARD
        # Need to distinguish between one pair or two pair.
        pairs = [k for k,v in card_dict.items() if v == 2]
        if len(pairs) == 1:
            return HandType.ONE_PAIR
        
        return HandType.TWO_PAIR

    def get_cards(cards: str, has_joker: bool) -> list[Card]:
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
                if has_joker:
                    my_card = Card.JOKER
                else:
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
        for i in range(len(self.cards)):
            my_card = self.cards[i]
            their_card = other.cards[i]
            if my_card > their_card:
                return True
            if my_card < their_card:
                return False
        
        return False
    
    def __eq__(self, other):
        return self.type == other.type and self.cards == other.cards
    
    def __lt__(self, other):
        return not self.is_stronger(other)
    
    def __gt__(self, other):
        return self.is_stronger(other)
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        return self == other or self > other
        
def build_hands(input_str: list[str], with_jokers: bool) -> list[Hand]:
    return [Hand(hand.split()[0], int(hand.split()[1]), with_jokers) for hand in input_str]

def get_winnings(input_data, with_jokers) -> int:
    hands = build_hands(input_data, with_jokers)
    hands = sorted(hands)
    total_winnings = sum([(i + 1) * hand.bet for i, hand in enumerate(hands)])

    return total_winnings


def run_case(file_name: str) -> str:
    input_data = read_file(file_name)
    
    total_winnings = get_winnings(input_data, False)

    total_winnings_with_jokers = get_winnings(input_data, True)

    return f"The total winnings of my hands is: {total_winnings}." \
    + f"{os.linesep}\tThe total winnings of my hand when playing with Jokers is: {total_winnings_with_jokers}."

def main() -> None:
    # Run test case
    print("Test Case:")
    print("\t" + run_case(test_file))

    # Run Full Problem Set
    print("Problem:")
    print("\t" + run_case(input_file))
    

if __name__ == "__main__":
    main()