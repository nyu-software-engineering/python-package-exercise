import pytest
from collections import Counter
from funcasino.deck import Card, Deck

def test_default_deck():
    deck = Deck()

    assert deck.num_decks == 1
    assert deck.size() == 52
    assert all(isinstance(card,Card) for card in deck.cards)

@pytest.mark.parametrize("num_decks", [1, 2, 8])
def test_multiple_decks(num_decks):
    deck = Deck(num_decks)

    assert deck.num_decks == num_decks
    assert deck.size() == 52 * num_decks
    assert all(isinstance(card,Card) for card in deck.cards)

@pytest.mark.parametrize("num_decks", [1, 2, 8])
def test_deck_correct_cards(num_decks):
    deck = Deck(num_decks)

    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9",
             "10", "J", "Q", "K", "A")

    expected = Counter({
        (rank, suit): num_decks
        for suit in suits
        for rank in ranks
    })
    actual = Counter((card.rank, card.suit) for card in deck.cards)

    assert actual == expected