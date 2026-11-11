import pytest
from realesagent.excuses import (
    generate_excuse,
    grade_beg,
    apology_multiplier,
    absence_excuse,
)


class Tests:

    def test_generate_excuse(self):
        actual = generate_excuse("Math Homework")

        assert isinstance(actual, str)
        assert len(actual) > 0
        assert "Math Homework" in actual

    def test_grade_beg(self):
        actual = grade_beg(69, 70, "Smith")

        assert isinstance(actual, str)
        assert "69" in actual
        assert "70" in actual
        assert "Smith" in actual

    def test_apology_multiplier(self):
        email = "Dear Professor Smith, I need an extension."

        actual = apology_multiplier(email, 9)

        assert isinstance(actual, str)
        assert email in actual
        assert "forgiveness" in actual.lower()

    def test_apology_multiplier_low_desperation(self):
        email = "Dear Professor Smith."

        actual = apology_multiplier(email, 1)

        assert email in actual
        assert "apologize" in actual.lower()

    def test_absence_excuse(self):
        result = absence_excuse("English")

        assert isinstance(result, str)
        assert "English" in result
        assert len(result) > 0


def test_generate_excuse_empty_assignment():
    with pytest.raises(ValueError):
        generate_excuse("")

    with pytest.raises(ValueError):
        generate_excuse("   ")


def test_generate_excuse_invalid_type():
    with pytest.raises(TypeError):
        generate_excuse(None)

    with pytest.raises(TypeError):
        generate_excuse(123)

    with pytest.raises(TypeError):
        generate_excuse(True)


def test_generate_excuse_whitespace():
    result = generate_excuse("  Math Homework  ")

    assert isinstance(result, str)
    assert "Math Homework" in result
    assert "  Math Homework  " not in result
