import random

card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
card_suits = [("spades", "♠"), ("clubs", "♣"), ("hearts", "♥"), ("diamonds", "♦")]


def create_deck():
    deck = {}
    for suit in card_suits:
        for rank in card_ranks:
            deck[f"{rank} of {suit[0]}"] = {"rank": rank, "suit": suit}
            if rank in ["J", "Q", "K"]:
                deck[f"{rank} of {suit[0]}"]["value"] = 10
            elif rank == "A":
                deck[f"{rank} of {suit[0]}"]["value"] = 1
            else:
                deck[f"{rank} of {suit[0]}"]["value"] = int(rank)
    return deck

def display_card(card_rank, card_suit):
    print(" _______")
    print(f"|{card_rank}      |")
    print(f"|       |")
    print(f"|       |")
    print(f"|   {card_suit}   |")
    print(f"|       |")
    print(f"|       |")
    print(f"|______{card_rank}|")

def display_hand(hand):
    for card in hand:
        print(" _______", end = " ")
    for card, details in hand.items():
        print(f"|{details['rank']}      |")
    for card in hand:
        print(f"|       |")
    for card in hand:
        print(f"|       |")
    for card, details in hand.items():
        print(f"|   {details['suit'][1]}   |")
    for card in hand:
        print(f"|       |")
    for card in hand:
        print(f"|       |")
    for card, details in hand.items():
        print(f"|______{details['rank']}|")

def play_blackjack(init_balance = 100):
    try:
        balance = int(init_balance)
        if balance <= 0:
            raise ValueError("Initial balance must be above $0")
    except ValueError:
        raise("Initial balance must be a whole number")

    print("Welcome to Blackjack!")
    play_again = "y"

    def new_game():
        deck = create_deck()
        nonlocal balance
        print(f"Deck has {len(deck)} cards")
        print(f"Balance: ${balance:.2f}")
        while True:
            try:
                bet = int(input("Place your inital bet: $"))
                if 0 < bet <= init_balance:
                    break
                else:
                    print("Invalid bet! Please enter a positive bet within your balance.")
            except ValueError:
                print("Invalid bet! Please enter a whole number.")
        
        balance += bet

    while play_again == "y":
        new_game()
        while True:
            play_again = input("Would you like to play again (y/n)? ").lower()
            if play_again == "y" or  play_again == "n":
                break    
    
    print(f"Walking away with ${balance:.2f}!")
    
        

if __name__ == "__main__":
    play_blackjack()