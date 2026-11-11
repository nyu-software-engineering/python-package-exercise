import random

SYMBOLS = ["CHERRY", "LEMON", "BELL", "STAR", "SEVEN"]
PAYOUTS = {"CHERRY": 2, "LEMON": 3, "BELL": 5, "STAR": 10, "SEVEN": 50}


def spin(reels=3):
    if reels < 2:
        raise ValueError("reels must be at least 2")
    
    return [random.choice(SYMBOLS) for _ in range(reels)]


def payout(result, bet):
    if bet <= 0:
        raise ValueError("bet must be positive")
    
    if len(set(result)) == 1:
        return bet * PAYOUTS[result[0]]
    
    return 0


def play(bet, balance, reels=3):
    if bet > balance:
        raise ValueError("bet cannot be more than balance")
    
    result = spin(reels)
    winnings = payout(result, bet)

    return result, balance - bet + winnings


if __name__ == "__main__":
    balance = 100
    
    for _ in range(5):
        result, balance = play(10, balance)
        print(" | ".join(result), "-> balance:", balance)