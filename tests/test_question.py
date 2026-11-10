import pytest

from project.magic8ball import get_question


def test_valid_question():
    assert get_question("Will I pass?") == "Will I pass?"
    assert get_question("Am I lucky?") == "Am I lucky?"
    assert get_question("Will it rain?") == "Will it rain?"


def test_question_with_spaces():
    assert get_question("  Will I pass?  ") == "Will I pass?"
    assert get_question("\nAm I lucky?\n") == "Am I lucky?"


def test_empty_question():
    with pytest.raises(ValueError):
        get_question("")

    with pytest.raises(ValueError):
        get_question("   ")


def test_invalid_type():
    with pytest.raises(TypeError):
        get_question(123)

    with pytest.raises(TypeError):
        get_question(None)

    with pytest.raises(TypeError):
        get_question(["Hello"])
