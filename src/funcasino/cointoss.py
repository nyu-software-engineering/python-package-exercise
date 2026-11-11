import random
import sys
import time

class CoinToss:
    def __init__(self, balance=100):
        self.balance = balance
        self.wins = 0
        self.losses = 0
        self.history = []

    def animate_flip(self, result, num_frames=12):
        print("Flipping coin...")

        frames = ["HEADS", "TAILS"]
        start = frames.index(result.upper()) - (num_frames - 1)

        for i in range(num_frames):
            frame = frames[(start + i) % 2]
            sys.stdout.write(f"\r🪙 {frame}   ")
            sys.stdout.flush()
            time.sleep(0.1 + i * 0.025)

        print()

    def flip_coin(self):
        return random.choice(["heads", "tails"])

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"Balance: ${self.balance}. Enter bet: $"))

                if 0 < bet <= self.balance:
                    return bet

                print("Invalid bet amount.")

            except ValueError:
                print("Please enter a valid number.")

    def play_round(self):
        bet = self.place_bet()

        choice = input("Heads or tails: ").lower()

        while choice not in ["heads", "tails"]:
            choice = input("Please enter heads or tails: ").lower()

        result = self.flip_coin()
        self.animate_flip(result)

        print(f"The coin landed on {result.upper()}!")

        if choice == result:
            self.balance += bet
            self.wins += 1
            print(f"You won ${bet}!")
        else:
            self.balance -= bet
            self.losses += 1
            print(f"You lost ${bet}!")

        self.history.append({
            "bet": bet,
            "choice": choice,
            "result": result,
            "balance": self.balance
        })

    def show_stats(self):
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total else 0

        print(f"\nWins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Balance: ${self.balance}")

    def play(self):
        while self.balance > 0:
            print("\n--- COIN TOSS ---")
            print("1. Play")
            print("2. View Stats")
            print("3. Quit")

            choice = input("Select an option: ")

            if choice == "1":
                self.play_round()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                break
            else:
                print("Invalid option.")

        print("Thanks for playing!")

    
if __name__ == "__main__":
    game = CoinToss()
    game.play()
