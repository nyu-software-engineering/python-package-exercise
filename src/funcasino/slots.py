import random
import sys
import time
from funcasino.wallet import Wallet

class Slots:
    SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎"]
    PAYOUTS = {"🍒": 5, "🍋": 10, "🔔": 15, "⭐": 25, "💎": 64}

    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0

    def spin(self):        
        return [random.choice(self.SYMBOLS) for _ in range(3)]

    def animate_spin(self, result, frames=12):
        for i in range(frames):
            sys.stdout.write("\r🎰 " + " | ".join(self.spin()))
            sys.stdout.flush()
            time.sleep(0.05 + i * 0.02)

        sys.stdout.write("\r🎰 " + " | ".join(result) + "\n")

    def payout(self, result, bet):
        if bet <= 0:
            raise ValueError("bet must be positive")
        
        if len(set(result)) == 1:
            return bet * self.PAYOUTS[result[0]]
        
        return 0


    def play_round(self):
        while self.wallet.balance > 0:
            bet = input(f"Balance: ${self.wallet.balance}. Enter bet (q to go back): $")
            if bet == "q":
                return
            if not bet.isdigit() or not self.wallet.can_afford(int(bet)):
                print("Invalid bet.")
                continue

            bet = int(bet)
            self.wallet.withdraw(bet)
            result = self.spin()
            self.animate_spin(result)
            winnings = self.payout(result, bet)
            self.wallet.deposit(winnings)

            if winnings:
                self.wins += 1
                print(f"You won ${winnings}!")
            else:
                self.losses += 1
                print(f"You lost ${bet}.")

    def show_stats(self):
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total else 0
        print(f"\nWins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Balance: ${self.wallet.balance}")
        input("Press q to go back: ")

    def play(self):
        while self.wallet.balance > 0:
            print("\n--- SLOTS ---")
            print("1. Spin")
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


if __name__ == "__main__":
    Slots().play()
