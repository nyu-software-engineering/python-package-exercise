from funcasino.wallet import Wallet
from funcasino.slots import Slots
from funcasino.cointoss import CoinToss
from funcasino.craps import play_craps

def main():
    wallet = Wallet(100)
    games = {
        "1": lambda : Slots(wallet).play(),
        "2": lambda: CoinToss(wallet).play(),
        "3": lambda: play_craps(wallet)
    }

    while wallet.balance > 0:
        choice = input(f"\nBalance ${wallet.balance} - 1) Slots 2) Coin Toss 3) Craps q) Quit: ")
        if choice == "q" or choice == "Q":
            break
        if choice in games:
            games[choice]()
        else:
            print("Please enter valid input\n")

if __name__ == "__main__":
    main()