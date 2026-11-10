import pytest

from quest_validation import validate_quest_input


def test_valid_quest_trims_title():
    assert validate_quest_input("  Study math  ", 60) == ("Study math", 60)


@pytest.mark.parametrize("title", ["", "   ", None])
def test_rejects_blank_or_missing_title(title):
    with pytest.raises(ValueError, match="Enter a quest title"):
        validate_quest_input(title, 60)


@pytest.mark.parametrize(
    "minutes", [None, 0, -5, 2.5, "abc", "60", True, 2**53]
)
def test_rejects_invalid_duration(minutes):
    with pytest.raises(ValueError, match="Enter a positive whole number"):
        validate_quest_input("Study math", minutes)