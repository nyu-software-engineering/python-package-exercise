import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @property
    def blackjack_value(self):
        if self.rank == "A":
            return 11
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ("Hearts", "Diamonds", "Clubs", "Spades")
        ranks = ("2", "3", "4", "5", "6", "7", "8", "9",
                 "9", "10", "J", "Q", "K", "A")
        
        self.cards = []
        for suit in suits:
            for rank in ranks:
                cards.append(Card(rank, suit))
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError("The deck is empty.")
        return self.cards.pop()
    
    def size(self):
        return len(self.cards)