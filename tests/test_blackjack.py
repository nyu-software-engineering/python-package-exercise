import pytest, random
from games_package.blackjack import (CARD_RANKS, CARD_SUITS, create_deck, display_hand, play_blackjack, shuffle_deck, sum_hand)

class TestCreateDeck:
    def test_create_deck_length():
        deck = create_deck()
        assert len(deck) == 52

    def test_each_card_present():
        deck = create_deck()
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                assert f"{rank} of {suit[0]}" in deck

    def test_card_structure():
        card = create_deck()["A of diamonds"]
        assert card == {"rank": "A", "suit": ("diamonds", "♦"), "value": 11}


class TestShuffleDeck:
    def test_shuffled_deck_length():
        shuffled = shuffle_deck(create_deck())
        assert shuffled is not None
        assert len(shuffled) == 52
        for card in shuffled:
            assert card is not None
            assert len(card) == 2
 
    def test_no_lost_cards():
        deck = create_deck()
        shuffled = shuffle_deck(deck)
        assert sorted(card[0] for card in shuffled) == sorted(deck)
 
    def test_shuffle():
        deck = create_deck()
        assert shuffle_deck(deck) != list(deck.items())

    def test_two_shuffled_decks():
        deck = create_deck()
        shuffled1 = shuffle_deck(deck)
        shuffled2 = shuffle_deck(deck)
        assert shuffled1 != shuffled2