import pytest
from realesagent.excuses import (
    generate_excuse,
    grade_beg,
    apology_multiplier,
    absence_excuse
)


class Tests:

    # Test generate_excuse()

    def test_generate_excuse(self):
        actual = generate_excuse("Math Homework")

        assert isinstance(actual, str)
        assert len(actual) > 0
        assert "Math Homework" in actual

    # Test grade_beg()

    def test_grade_beg(self):
        actual = grade_beg(69, 70, "Smith")

        assert isinstance(actual, str)
        assert "69" in actual
        assert "70" in actual
        assert "Smith" in actual

    # Test apology_multiplier()

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

    # Test absence_excuse()

    def test_absence_excuse(self):
        result = absence_excuse("English")

        assert isinstance(result, str)
        assert "English" in result
        assert len(result) > 0
