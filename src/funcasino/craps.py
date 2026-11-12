import random
from funcasino.wallet import Wallet

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}


class Craps:
    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()

    def print_dice(self, dice1, dice2):
        for line in range(5):
            print(dice_art[dice1][line] + "  " + dice_art[dice2][line])

    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.print_dice(dice1, dice2)
        return dice1, dice2, dice1 + dice2

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"Balance: ${self.wallet.balance}. Enter bet: $"))

                if 0 < bet <= self.wallet.balance:
                    return bet

                print("Invalid bet amount.")

            except ValueError:
                print("Please enter a valid number.")

    def play_round(self):
        bet = self.place_bet()

        input("Press Enter to roll the dice!")
        dice1, dice2, sum1 = self.roll_dice()
        print(f"Your total is {sum1}")

        #first round, either 2x, 0x, or advances
        if sum1 in (7, 11):
            self.wallet.deposit(bet)
            print(f"Natural {sum1}! You won ${bet}!")
            return
        elif sum1 in (2, 3, 12):
            self.wallet.withdraw(bet)
            print(f"Craps ({sum1})! You lost ${bet}!")
            return

        point = sum1
        print(f"Your point is now: {point}. Try to hit {point} before rolling a 7!")

        #second round
        while True:
            input("Press Enter to roll again!")
            dice1, dice2, sum2 = self.roll_dice()

            if sum2 == point:
                self.wallet.deposit(bet)
                print(f"You rolled {dice1} and {dice2} ({sum2}) , You hit your number! You won ${bet}!")
                return

            if sum2 == 7:
                self.wallet.withdraw(bet)
                print(f"You rolled {dice1} and {dice2} (7) , You sevened out unfortunately. You lost ${bet}!")
                return

            print(f"You rolled {sum2} ({dice1} and {dice2}), not {point} or 7. Rerolling...")

    def play(self):
        while self.wallet.balance > 0:
            print("\n--- CRAPS ---")
            print("1. Play")
            print("2. Quit")

            choice = input("Select an option: ")

            if choice == "1":
                self.play_round()
            elif choice == "2":
                break
            else:
                print("Invalid option.")

        print("Thanks for playing!")


if __name__ == "__main__":
    game = Craps()
    game.play()