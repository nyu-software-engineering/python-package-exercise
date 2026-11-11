import pytest
from realesagent import extension_request, subject_line


def test_subject_line_invalid_situation():
    for situation in ("", "   ", None, 123):
        with pytest.raises(ValueError):
            subject_line(situation, 3)


def test_subject_line_levels():
    prefixes = [
        "Quick Question About",
        "A Humble Request Regarding",
        "URGENT: My Academic Future Depends on",
        "FINAL PLEA: I Am Fighting for My Life Over",
        "PLEASE READ BEFORE I BECOME A CAMPUS URBAN LEGEND:",
    ]
    for urgency in range(1, 6):
        prefix = prefixes[urgency - 1]
        result = subject_line("Homework", urgency)
        assert result == f"{prefix} Homework"
        assert result.endswith("Homework")
        assert subject_line("Exam", urgency) == f"{prefix} Exam"


def test_subject_line_invalid_levels():
    for urgency in [0, 6, -1, "3", None]:
        assert subject_line("Homework", urgency) == "Invalid urgency level"


def test_extension_request_tiers():
    cases = [
        (0, "a little extra time"),
        (1, "another 24 hours"),
        (2, "another 24 hours"),
        (3, "reflecting on my choices"),
        (5, "reflecting on my choices"),
        (6, "more of a suggestion"),
        (10, "more of a suggestion"),
        (11, "a fresh start"),
    ]
    for days, phrase in cases:
        result = extension_request(days, "Rivera")
        assert result.startswith("Dear Professor Rivera,\n\n")
        assert phrase in result
        assert result.endswith("Best,\nA Student With Excellent Intentions")


def test_extension_request_invalid_values():
    cases = [
        (-1, "Rivera", ValueError),
        (0, "   ", ValueError),
        ("one", "Rivera", TypeError),
        (0, None, AttributeError),
    ]
    for days, name, expected_error in cases:
        try:
            extension_request(days, name)
        except expected_error:
            pass
        else:
            assert False, "Expected an error for invalid extension input"

def test_subject_line_invalid_situation():
    for situation in ("", "   ", None, 123):
        with pytest.raises(ValueError):
            subject_line(situation, 3)
