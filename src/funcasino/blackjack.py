from wallet import Wallet
from deck import Deck

class Blackjack:
    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0