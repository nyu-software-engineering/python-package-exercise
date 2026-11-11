import random
import sys
import time
from funcasino.wallet import Wallet

class Slots:
    SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎"]
    PAYOUTS = {"🍒": 2, "🍋": 3, "🔔": 5, "⭐": 10, "💎": 50}

    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()

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


    def play(self):
        while self.wallet.balance > 0:
            bet = input(f"Balance: ${self.wallet.balance}. Enter bet (or q to quit): $")
            if bet == "q":
                break
            if not bet.isdigit() or not self.wallet.can_afford(int(bet)):
                print("Invalid bet.")
                continue

            bet = int(bet)
            self.wallet.withdraw(bet)
            result = self.spin()
            winnings = self.payout(result, bet)
            self.wallet.deposit(winnings)

            self.animate_spin(result)
            print(f"You won ${winnings}!" if winnings else f"You lost ${bet}.")

        print("Thank you for your generous donation to the house!")


if __name__ == "__main__":
    Slots().play()
