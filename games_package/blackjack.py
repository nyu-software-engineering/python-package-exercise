import random

CARD_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = [("spades", "♠"), ("clubs", "♣"), ("hearts", "♥"), ("diamonds", "♦")]


def create_deck():
    deck = {}
    for suit in CARD_SUITS:
        for rank in CARD_RANKS:
            deck[f"{rank} of {suit[0]}"] = {"rank": rank, "suit": suit}
            if rank in ["J", "Q", "K"]:
                deck[f"{rank} of {suit[0]}"]["value"] = 10
            elif rank == "A":
                deck[f"{rank} of {suit[0]}"]["value"] = 11
            else:
                deck[f"{rank} of {suit[0]}"]["value"] = int(rank)
    return deck

def shuffle_deck(deck):
    shuffled = list(deck.items())
    random.shuffle(shuffled)
    return shuffled

def sum_hand(hand):
    sum = 0
    aces = 0

    for card in hand:
        sum += card[1]['value']
        if card[1]['rank'] == "A":
            aces += 1

    for i in range(aces):
        if sum <= 21:
            break
        sum -= 10
    
    return sum

def display_hand(hand, hole=False):
    row1, row2, row3, row4, row5, row6, row7, row8 = [], [], [], [], [], [], [], []
    rows = [row1, row2, row3, row4, row5, row6, row7, row8]

    for i, card in enumerate(hand):
        row1.append(" _______ ")
        if hole and i == 0:
            row2.append("|/ / / /|")
            row3.append("| / / / |")
            row4.append("|/ / / /|")
            row5.append("| / / / |")
            row6.append("|/ / / /|")
            row7.append("| / / / |")
            row8.append("|/_/_/_/|")
        else:
            row2.append(f"|{card[1]['rank']:>2}     |")
            row3.append("|       |")
            row4.append("|       |")
            row5.append(f"|   {card[1]['suit'][1]}   |")
            row6.append("|       |")
            row7.append("|       |")
            row8.append(f"|_____{card[1]['rank']:<2}|")

    for i in range(8):
        print(" ".join(rows[i]))
    print()

def play_blackjack(init_balance=100):
    try:
        balance = int(init_balance)
        if balance <= 0:
            raise ValueError("Initial balance must be above $0")
    except ValueError:
        raise ValueError("Initial balance must be a whole number")

    print("Welcome to Blackjack!")
    play_again = "y"

    def new_game():
        deck = shuffle_deck(create_deck())
        nonlocal balance
        hit = "h"
        print(f"Balance: ${balance:.2f}")
        while True:
            try:
                bet = int(input("Place your inital bet: $"))
                if 0 < bet <= balance:
                    break
                else:
                    print("Invalid bet! Please enter a positive bet within your balance.")
            except ValueError:
                print("Invalid bet! Please enter a whole number.")
        
        player_hand = []
        dealer_hand = []

        def init_round():
            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop())
            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop())
            print("Player:")
            display_hand(player_hand)
            print("Dealer:")
            display_hand(dealer_hand, True)

        def draw_card(hand, hole = False):
            hand.append(deck.pop())
            print("Player:")
            display_hand(player_hand)
            print("Dealer:")
            display_hand(dealer_hand, hole)

        while hit == "h":
            if len(player_hand) == 0:
                init_round()
            else:
                draw_card(player_hand, True)
            if sum_hand(player_hand) >= 21:
                hit = "s"
            else:
                while True:
                    hit = input("Would you like to hit or stay (h/s)? ").lower()
                    if hit == "h" or hit == "s":
                        break

        if sum_hand(player_hand) > 21:
            print(f"You busted! You lost ${bet:.2f}!")
            balance -= bet
        else:
            print("Player:")
            display_hand(player_hand)
            print("Dealer:")
            display_hand(dealer_hand)
            while sum_hand(dealer_hand) < 17:
                input("Press enter to continue!")
                draw_card(dealer_hand, False)
            player_sum = sum_hand(player_hand)
            dealer_sum = sum_hand(dealer_hand)
            if dealer_sum > 21:
                print(f"Dealer busted! You won ${bet:.2f}!")
                balance += bet
            elif dealer_sum > player_sum:
                print(f"Dealer won! You lost ${bet:.2f}!")
                balance -= bet
            elif player_sum > dealer_sum:
                print(f"You won! You won ${bet:.2f}!")
                balance += bet
            else:
                print("Tie! You keep your bet.")
            
    while play_again == "y":
        new_game()
        if balance == 0:
            print("You're broke! No more blackjack!")
            play_again = "n"
        else:
            while True:
                play_again = input("Would you like to play again (y/n)? ").lower()
                if play_again == "y" or  play_again == "n":
                    break    
    
    print(f"Walking away with ${balance:.2f}!")

if __name__ == "__main__":
    play_blackjack()