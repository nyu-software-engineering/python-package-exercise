import random
import pytest
from games_package import wordle


def scripted_input(*guesses):
    answers = iter(guesses)
    return lambda prompt: next(answers)


class TestWordValidation:
    def test_valid_words(self):
        assert wordle._is_valid_word("apple") is True
        assert wordle._is_valid_word("APPLE") is True
        assert wordle._is_valid_word("CrAnE") is True
        
    def test_invalid_words(self):
        assert wordle._is_valid_word("cat") is False
        assert wordle._is_valid_word("apples") is False
        assert wordle._is_valid_word("a2ple") is False
        assert wordle._is_valid_word("a ple") is False
        assert wordle._is_valid_word("ápple") is False
        assert wordle._is_valid_word(None) is False


def test_invalid_english_word():
    guesses = iter(["prynt", "crypt"])
    messages = []
    result = wordle.play_wordle(
        secret="crypt",
        input_fn=lambda _: next(guesses),
        output_fn=messages.append
    )

    assert result["won"] is True
    assert result["attempts"] == 1
    assert result["guesses"] == ("crypt",)
    assert "Invalid guess: not a recognized English word." in messages


class TestChooseWord:
    def test_word_is_chosen_from_supplied_list(self):
        assert wordle._choose_word(["apple"]) == "apple"
        assert wordle._choose_word(["GRAPE"]) == "grape"
        assert wordle._choose_word(["apple", "grape"]) in {"apple", "grape"}

    def test_random_choice_is_repeatable_with_seed(self):
        words = ["apple", "grape", "peach", "lemon"]
        actual = wordle._choose_word(words, random.Random(42))
        expected = wordle._choose_word(words, random.Random(42))
        assert actual == expected, "Equal random seeds should select the same word"
        assert actual in words, "The answer should come from the word bank"

    def test_empty_word_list_raises_value_error(self):
        with pytest.raises(ValueError):
            wordle._choose_word([])


class TestScoreGuess:
    def test_all_letters_correct(self):
        actual = wordle._score_guess("apple", "apple")
        assert actual == ("correct",) * 5
        assert len(actual) == 5
        assert wordle._score_guess("APPLE", "apple") == ("correct",) * 5

    def test_all_letters_absent(self):
        actual = wordle._score_guess("apple", "zzzzz")
        assert actual == ("absent",) * 5

    def test_mixed_correct_present_and_absent(self):
        actual = wordle._score_guess("apple", "grape")
        assert actual == ("absent", "absent", "present", "present", "correct")
        assert wordle._score_guess("crane", "crown") == ("correct", "correct", "absent", "absent", "present")

    def test_repeated_letters_are_not_counted_twice(self):
        assert wordle._score_guess("apple", "allee") == ("correct", "present", "absent", "absent", "correct")
        assert wordle._score_guess("apple", "ppppp") == ("absent", "correct", "correct", "absent", "absent")

    @pytest.mark.parametrize("secret, guess",
                            [("cat", "apple"), ("apple", "hi"), ("apple", "a2ple")])
    def test_invalid_words_raise_value_error(self, secret, guess):
        with pytest.raises(ValueError):
            wordle._score_guess(secret, guess)


class TestFormatFeedback:
    def test_colored_squares(self):
        assert wordle._format_feedback("apple", ("correct",) * 5) == ("APPLE  🟩🟩🟩🟩🟩")
        assert wordle._format_feedback("grape", ("absent",) * 5) == ("GRAPE  ⬛⬛⬛⬛⬛")
        assert wordle._format_feedback("allee", ("correct", "present", "absent", "absent", "correct")) == "ALLEE  🟩🟨⬛⬛🟩"

    def test_unknown_status_raises_key_error(self):
        with pytest.raises(KeyError):
            wordle._format_feedback("apple", ("unknown",) * 5)
            

class TestPlayWordle:
    def test_winning_game(self):
        messages = []
        actual = wordle.play_wordle(
            secret="apple",
            input_fn=scripted_input("grape", "APPLE"),
            output_fn=messages.append,
        )
        assert actual["won"] is True
        assert actual["attempts"] == 2
        assert actual["guesses"] == ("grape", "apple")
        assert actual["secret"] == "apple"
        assert actual["cancelled"] is False
        assert "APPLE  🟩🟩🟩🟩🟩" in messages
        assert any("You won" in message for message in messages)

    def test_losing_game_respects_max_attempts(self):
        messages = []
        actual = wordle.play_wordle(
            max_attempts=2,
            secret="apple",
            input_fn=scripted_input("grape", "melon"),
            output_fn=messages.append,
        )
        assert actual["won"] is False
        assert actual["attempts"] == 2
        assert actual["guesses"] == ("grape", "melon")
        assert actual["cancelled"] is False
        assert any("Game over" in message for message in messages)

    def test_invalid_guesses_do_not_use_attempts(self):
        messages = []
        actual = wordle.play_wordle(
            max_attempts=1,
            secret="apple",
            input_fn=scripted_input("cat", "a2ple", "apple"),
            output_fn=messages.append,
        )
        assert actual["won"] is True
        assert actual["attempts"] == 1
        assert actual["guesses"] == ("apple",)
        assert sum("Invalid guess" in message for message in messages) == 2

    def test_custom_word_bank_is_used(self):
        actual = wordle.play_wordle(
            words=["grape"],
            input_fn=scripted_input("grape"),
            output_fn=lambda message: None,
        )
        assert actual["secret"] == "grape"
        assert actual["won"] is True
        assert actual["attempts"] == 1

    def test_whitespace_and_uppercase_input(self):
        actual = wordle.play_wordle(
            secret="APPLE",
            input_fn=scripted_input("  APPLE  "),
            output_fn=lambda message: None,
        )
        assert actual["won"] is True
        assert actual["secret"] == "apple"
        assert actual["guesses"] == ("apple",)

    @pytest.mark.parametrize("error_type", [EOFError, KeyboardInterrupt])
    def test_cancelled_game(self, error_type):
        def interrupted_input(prompt):
            raise error_type
        actual = wordle.play_wordle(
            secret="apple",
            input_fn=interrupted_input,
            output_fn=lambda message: None,
        )
        assert actual["cancelled"] is True
        assert actual["won"] is False
        assert actual["attempts"] == 0

    @pytest.mark.parametrize("max_attempts", [0, -1, 1.5, True, "six"])
    def test_invalid_attempt_limits_raise_value_error(self, max_attempts):
        with pytest.raises(ValueError):
            wordle.play_wordle(max_attempts=max_attempts, secret="apple")

    @pytest.mark.parametrize("secret", ["cat", "apple1", "a2ple"])
    def test_invalid_secret_raises_value_error(self, secret):
        with pytest.raises(ValueError):
            wordle.play_wordle(secret=secret)

    def test_empty_custom_word_bank_raises_value_error(self):
        with pytest.raises(ValueError):
            wordle.play_wordle(words=[])

