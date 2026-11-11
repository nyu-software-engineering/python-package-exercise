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

class TestSumHand:
    def test_sum_empty_hand():
        hand = []
        assert sum_hand(hand) == 0
 
    @pytest.mark.parametrize(
        ("ranks, correct"), 
        [
            (["10", "A"], 21),
            (["10", "A", "A", "2"], 14),
            (["10", "Q", "5"], 25),
            (["10", "A", "9", "A", "A"], 22),
        ],
    )
    def test_sums(ranks, correct):
        hand = []
        deck = create_deck()
        for rank in ranks:
            hand.append(deck[f"{rank} of hearts"])
        assert sum_hand(hand) == correct

class TestSetup:
    @pytest.mark.parametrize("balance", ["abc", 0, -5, 0.5])
    def test_invalid_init_balance(balance):
        with pytest.raises(ValueError):
            play_blackjack(balance)
 
    @pytest.mark.parametrize("balance", [100, 200, 500, 4])
    def test_valid_init_balance(balance):
        play_blackjack(balance)
        printed = capsys.readouterr().out
        assert "Welcome to Blackjack!" in printed
        assert f"Balance: ${balance:.2f}" in printed
    
    def test_blank_init_balance():
        play_blackjack()
        printed = capsys.readouterr().out
        assert "Welcome to Blackjack!" in printed
        assert "Balance: $100.00" in printed