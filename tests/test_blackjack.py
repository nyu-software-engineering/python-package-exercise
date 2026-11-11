import pytest, random
from games_package import blackjack 
from games_package.blackjack import (CARD_RANKS, CARD_SUITS, create_deck, display_hand, play_blackjack, shuffle_deck, sum_hand)

# TestCreateDeck
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

def test_desk_consistency():
    deck = create_deck()
    deck2 = create_deck()
    assert deck == deck2

# TestShuffleDeck
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

# TestSumHand
def test_sum_empty_hand():
    hand = []
    assert sum_hand(hand) == 0

@pytest.mark.parametrize(
    "hand", 
    [
        [('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}), 
        ('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}),
        ('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}),
        ('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}),
        ('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10})]
    ]
)
def test_invalid_hand_sum(hand):
    with pytest.raises(ValueError):
        sum_hand(hand)

@pytest.mark.parametrize(
    ("ranks", "suites", "correct"), 
    [
        (["10", "A"], ["hearts", "diamonds"], 21),
        (["10", "A", "A", "2"], ["hearts", "diamonds", "spades", "hearts"], 14),
        (["10", "Q", "5"], ["hearts", "diamonds", "spades"], 25),
        (["10", "A", "9", "A", "A"], ["hearts", "diamonds", "hearts", "spades", "clubs"], 22),
    ],
)
def test_sums(ranks, suites, correct):
    deck = create_deck()
    testing_cards = {}
    for i, rank in enumerate(ranks):
        testing_cards[f"{rank} of {suites[i]}"] = deck[f"{rank} of {suites[i]}"]
    
    hand = list(testing_cards.items())
    assert sum_hand(hand) == correct

# TestDisplayHand
def test_card_length(capsys):
    hand = [('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10})]
    display_hand(hand)
    lines = capsys.readouterr().out.split("\n")
    assert len(lines) == 10
    assert lines[8] == ""

@pytest.mark.parametrize(
    "suit, symbol", 
    [("spades", "♠"), ("clubs", "♣"), ("hearts", "♥"), ("diamonds", "♦")]
)
def test_single_card(capsys, suit, symbol):
    display_hand([(f'10 of {suit}', {'rank': '10', 'suit': (suit, symbol), 'value': 10})])
    lines = capsys.readouterr().out.split("\n")
    assert lines[1] == "|10     |"
    assert lines[4] == f"|   {symbol}   |"
    assert lines[7] == "|_____10|"

def test_multiple_cards(capsys):
    hand = [('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}), ('2 of clubs', {'rank': '2', 'suit': ('clubs', '♣'), 'value': 2})]
    display_hand(hand)
    lines = capsys.readouterr().out.split("\n")
    assert lines[1] == "|10     | | 2     |"
    assert lines[4] == "|   ♣   | |   ♣   |"

def test_hole_card(capsys):
    hand = [('10 of clubs', {'rank': '10', 'suit': ('clubs', '♣'), 'value': 10}), ('2 of clubs', {'rank': '2', 'suit': ('clubs', '♣'), 'value': 2})]
    display_hand(hand, True)
    lines = capsys.readouterr().out.split("\n")
    assert lines[1] == "|/ / / /| | 2     |"
    assert lines[7] == "|/_/_/_/| |_____2 |"

def test_empty_hand():
   with pytest.raises(ValueError):
        display_hand([])

# TestInitalizeGame
def test_blank_init_balance(capsys, monkeypatch):
    inputs = ["1", "s"] 

    def filler(_):
        if inputs:
            return inputs.pop(0)
        if not hasattr(filler, "done"):
            filler.done = True
            return ""
        return "n"

    monkeypatch.setattr('builtins.input', filler)
    play_blackjack()
    printed = capsys.readouterr().out
    assert "Welcome to Blackjack!" in printed
    assert "Balance: $100.00" in printed

@pytest.mark.parametrize("balance", ["abc", 0, -5, 0.5])
def test_invalid_init_balance(balance):
    with pytest.raises(ValueError):
        play_blackjack(balance)

@pytest.mark.parametrize("balance", [100, 200, 500, 4])
def test_valid_init_balance(balance, capsys, monkeypatch):
    inputs = ["1", "s"] 

    def filler(_):
        if inputs:
            return inputs.pop(0)
        if not hasattr(filler, "done"):
            filler.done = True
            return ""
        return "n"

    monkeypatch.setattr('builtins.input', filler)
    play_blackjack(balance)
    printed = capsys.readouterr().out
    assert "Welcome to Blackjack!" in printed
    assert f"Balance: ${balance:.2f}" in printed

# TestGameOutcomes
def test_player_wins_higher(capsys, monkeypatch):
    inputs = ["10", "s"]
    deck = {}
    deck["7 of diamonds"] = {"rank": "7", "suit": ("diamonds", "♦"), "value": 7}
    deck["8 of diamonds"] = {"rank": "8", "suit": ("diamonds", "♦"), "value": 8}
    deck["10 of diamonds"] = {"rank": "10", "suit": ("diamonds", "♦"), "value": 10}
    deck["A of diamonds"] = {"rank": "A", "suit": ("diamonds", "♦"), "value": 11}
    deck_list = list(deck.items())

    def filler(_):
        if inputs:
            return inputs.pop(0)
        if not hasattr(filler, "done"):
            filler.done = True
            return ""
        return "n"

    monkeypatch.setattr('builtins.input', filler)
    monkeypatch.setattr(blackjack, "shuffle_deck", lambda d: deck_list)
    play_blackjack()
    printed = capsys.readouterr().out
    assert "You won! You won $10.00!" in printed
    assert "Walking away with $110.00!" in printed

def test_dealer_wins_higher(capsys, monkeypatch):
    inputs = ["10", "s"]
    deck = {}
    deck["A of diamonds"] = {"rank": "A", "suit": ("diamonds", "♦"), "value": 11}
    deck["10 of diamonds"] = {"rank": "10", "suit": ("diamonds", "♦"), "value": 10}
    deck["8 of diamonds"] = {"rank": "8", "suit": ("diamonds", "♦"), "value": 8}
    deck["7 of diamonds"] = {"rank": "7", "suit": ("diamonds", "♦"), "value": 7}
    deck_list = list(deck.items())

    def filler(_):
        if inputs:
            return inputs.pop(0)
        if not hasattr(filler, "done"):
            filler.done = True
            return ""
        return "n"

    monkeypatch.setattr('builtins.input', filler)
    monkeypatch.setattr(blackjack, "shuffle_deck", lambda d: deck_list)
    play_blackjack()
    printed = capsys.readouterr().out
    assert "Dealer won! You lost $10.00!" in printed
    assert "Walking away with $90.00!" in printed

def test_tie(capsys, monkeypatch):
    inputs = ["10", "s"]
    deck = {}
    deck["7 of diamonds"] = {"rank": "7", "suit": ("diamonds", "♦"), "value": 7}
    deck["8 of diamonds"] = {"rank": "8", "suit": ("diamonds", "♦"), "value": 8}
    deck["10 of diamonds"] = {"rank": "10", "suit": ("diamonds", "♦"), "value": 10}
    deck["9 of diamonds"] = {"rank": "9", "suit": ("diamonds", "♦"), "value": 9}
    deck_list = list(deck.items())

    def filler(_):
        if inputs:
            return inputs.pop(0)
        if not hasattr(filler, "done"):
            filler.done = True
            return ""
        return "n"

    monkeypatch.setattr('builtins.input', filler)
    monkeypatch.setattr(blackjack, "shuffle_deck", lambda d: deck_list)
    play_blackjack()
    printed = capsys.readouterr().out
    assert "Tie! You keep your bet." in printed
    assert "Walking away with $100.00!" in printed