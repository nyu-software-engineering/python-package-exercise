import re

import pytest

from pyfakefacts.statistic import generate_statistic


def test_generate_statistic_returns_nonempty_string():
    result = generate_statistic("students", "campus life")

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_generate_statistic_contains_inputs():
    result = generate_statistic("students", "campus life")

    assert "students" in result
    assert "campus life" in result


def test_generate_statistic_contains_valid_percentage():
    result = generate_statistic("students", "campus life")
    percentage_match = re.search(r"(\d+)%", result)

    assert percentage_match is not None
    assert 1 <= int(percentage_match.group(1)) <= 99


@pytest.mark.parametrize(
    "topic",
    [None, 123, 1.5, True, [], {}],
)
def test_invalid_topic_type(topic):
    with pytest.raises(TypeError, match="topic must be a string"):
        generate_statistic(topic, "campus life")


@pytest.mark.parametrize(
    "category",
    [None, 123, 1.5, True, [], {}],
)
def test_invalid_category_type(category):
    with pytest.raises(TypeError, match="category must be a string"):
        generate_statistic("students", category)


@pytest.mark.parametrize(
    "topic",
    ["", " ", "   ", "\t", "\n"],
)
def test_empty_topic(topic):
    with pytest.raises(ValueError):
        generate_statistic(topic, "campus life")


@pytest.mark.parametrize(
    "category",
    ["", " ", "   ", "\t", "\n"],
)
def test_empty_category(category):
    with pytest.raises(ValueError):
        generate_statistic("students", category)


def test_topic_whitespace_is_trimmed():
    result = generate_statistic("\t students \n", "campus life")

    assert "students" in result
    assert "\t" not in result
    assert "\n" not in result


def test_category_whitespace_is_trimmed():
    result = generate_statistic("students", "\t campus life \n")

    assert "campus life" in result
    assert "\t" not in result
    assert "\n" not in result


def test_internal_spaces_are_preserved():
    result = generate_statistic("New York students", "campus life")

    assert "New York students" in result
    assert "campus life" in result


def test_capitalization_is_preserved():
    result = generate_statistic("NYU Students", "Campus Life")

    assert "NYU Students" in result
    assert "Campus Life" in result


def test_unicode_inputs_are_preserved():
    result = generate_statistic("café owners", "文化")

    assert "café owners" in result
    assert "文化" in result


@pytest.mark.parametrize("percentage", [1, 99])
def test_percentage_boundaries(monkeypatch, percentage):
    monkeypatch.setattr(
        "pyfakefacts.statistic.random.randint",
        lambda lower, upper: percentage,
    )

    result = generate_statistic("students", "campus life")

    assert f"{percentage}%" in result


@pytest.mark.parametrize(
    ("template_index", "expected_phrase"),
    [
        (0, "secretly controlled by pigeons"),
        (1, "communicate with aliens"),
        (2, "time-traveling hamsters"),
        (3, "works better when nobody is watching"),
        (4, "government conspiracy"),
    ],
)
def test_each_statistic_template(
    monkeypatch, template_index, expected_phrase
):
    monkeypatch.setattr(
        "pyfakefacts.statistic.random.choice",
        lambda templates: templates[template_index],
    )
    monkeypatch.setattr(
        "pyfakefacts.statistic.random.randint",
        lambda lower, upper: 42,
    )

    result = generate_statistic("students", "campus life")

    assert expected_phrase in result
    assert "42%" in result
    assert "students" in result
    assert "campus life" in result
