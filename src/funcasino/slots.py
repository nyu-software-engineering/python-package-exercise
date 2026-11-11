import random

class Slots:
    SYMBOLS = ["CHERRY", "LEMON", "BELL", "STAR", "SEVEN"]
    PAYOUTS = {"CHERRY": 2, "LEMON": 3, "BELL": 5, "STAR": 10, "SEVEN": 50}

    def __init__(self, balance=100):
            self.balance = balance

    def spin(self):        
        return [random.choice(self.SYMBOLS) for _ in range(3)]


    def payout(self, result, bet):
        if bet <= 0:
            raise ValueError("bet must be positive")
        
        if len(set(result)) == 1:
            return bet * self.PAYOUTS[result[0]]
        
        return 0


    def play(self):
        while self.balance > 0:
            bet = input(f"Balance: ${self.balance}. Enter bet (or q to quit): $")
            if bet == "q":
                break
            if not bet.isdigit() or not 0 < int(bet) <= self.balance:
                print("Invalid bet.")
                continue

            bet = int(bet)
            result = self.spin()
            winnings = self.payout(result, bet)
            self.balance += winnings - bet

            print(" | ".join(result))
            print(f"You won ${winnings}!" if winnings else f"You lost ${bet}.")

        print("Thank you for your donation!")


if __name__ == "__main__":
    Slots().play()
