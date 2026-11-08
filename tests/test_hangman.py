import pytest
from games_package.hangman import choose_word, check_guess, display_word, check_game_status, WORDS

def test_choose_word():
    # Test valid difficulty and category combinations
    word1 = choose_word("easy", "animals")
    assert word1 in WORDS["animals"]["easy"]

    word2 = choose_word("medium", "food")
    assert word2 in WORDS["food"]["medium"]

    word3 = choose_word("hard", "technology")
    assert word3 in WORDS["technology"]["hard"]

    # Test invalid category
    with pytest.raises(ValueError):
        choose_word("easy", "invalid")

    # Test invalid difficulty
    with pytest.raises(ValueError):
        choose_word("invalid", "animals")

def test_check_guess():
    # Correct guess
    guessed = []
    assert check_guess("apple", "a", guessed) == "correct"
    assert "a" in guessed

    # Incorrect guess
    assert check_guess("apple", "z", guessed) == "incorrect"
    assert "z" in guessed

    # Repeated guess
    assert check_guess("apple", "a", guessed) == "already guessed"

    # Invalid guess (more than one letter)
    with pytest.raises(ValueError):
        check_guess("apple", "ab", guessed)

    # Invalid guess (number)
    with pytest.raises(ValueError):
        check_guess("apple", "5", guessed)

def test_display_word():
    # No letters guessed
    assert display_word("cat", []) == "_ _ _"

    # One correct letter guessed
    assert display_word("cat", ["a"]) == "_ a _"

    # All letters guessed
    assert display_word("cat", ["c", "a", "t"]) == "c a t"

    # Incorrect guesses should not reveal letters
    assert display_word("cat", ["z"]) == "_ _ _"

    # Repeated letters should all be revealed
    assert display_word("apple", ["p"]) == "_ p p _ _"

def test_check_game_status():
    # Player is still playing
    assert check_game_status("cat", ["c"]) == "playing"

    # Player has guessed every letter
    assert check_game_status("cat", ["c", "a", "t"]) == "won"

    # Player has made 9 incorrect guesses
    assert check_game_status("cat", ["b", "d", "e", "f", "g", "h", "i", "j", "k"]) == "lost"

    # Incorrect guesses do not prevent winning
    assert check_game_status("cat", ["c", "a", "t", "z"]) == "won"

    # Test a custom maximum of 3 incorrect guesses
    assert check_game_status("cat", ["b", "d", "e"], 3) == "lost"