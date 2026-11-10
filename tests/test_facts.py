import pytest

from pyfakefacts.facts import generate_fact

def test_generate_fact_returns_string():
    result = generate_fact("cats", "animals")

    assert isinstance(result, str)


def test_generate_fact_is_not_empty():
    result = generate_fact("cats", "animals")

    assert len(result.strip()) > 0


def test_generate_fact_contains_inputs():
    result = generate_fact("cats", "animals")

    assert "cats" in result
    assert "animals" in result

@pytest.mark.parametrize(
    "topic",
    [None, 123, 1.5, True, [], {}],
)
def test_invalid_topic_type(topic):
    with pytest.raises(TypeError, match="topic must be a string"):
        generate_fact(topic, "animals")


@pytest.mark.parametrize(
    "category",
    [None, 123, 1.5, True, [], {}],
)
def test_invalid_category_type(category):
    with pytest.raises(TypeError, match="category must be a string"):
        generate_fact("cats", category)


@pytest.mark.parametrize(
    "topic",
    ["", " ", "   ", "\t", "\n", " \t\n "],
)
def test_empty_topic(topic):
    with pytest.raises(ValueError, match="topic must not be empty"):
        generate_fact(topic, "animals")


@pytest.mark.parametrize(
    "category",
    ["", " ", "   ", "\t", "\n", " \t\n "],
)
def test_empty_category(category):
    with pytest.raises(ValueError, match="category must not be empty"):
        generate_fact("cats", category)


def test_topic_whitespace_is_trimmed():
    result = generate_fact("\t cats \n", "animals")

    assert "cats" in result
    assert "\t" not in result
    assert "\n" not in result
    assert "  " not in result


def test_category_whitespace_is_trimmed():
    result = generate_fact("cats", "\t animals \n")

    assert "animals" in result
    assert "\t" not in result
    assert "\n" not in result
    assert "  " not in result


def test_internal_spaces_are_preserved():
    result = generate_fact("New York students", "campus life")

    assert "New York students" in result
    assert "campus life" in result


def test_capitalization_is_preserved():
    result = generate_fact("NYU Students", "Campus Life")

    assert "NYU Students" in result
    assert "Campus Life" in result


def test_unicode_inputs():
    result = generate_fact("café owners", "文化")

    assert "café owners" in result
    assert "文化" in result