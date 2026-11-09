import random

import pytest

from project.random_response import RESPONSES, get_response, normalize_category


@pytest.mark.parametrize("category", ["positive", "non-committal", "negative"])
def test_response_comes_from_its_category(category):
    for _ in range(50):
        assert get_response(category) in RESPONSES[category]


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Positive", "positive"),
        ("Non-Committal", "non-committal"),
        ("Negative", "negative"),
        ("  NEGATIVE ", "negative"),
        ("non committal", "non-committal"),
        ("noncommittal", "non-committal"),
    ],
)
def test_accepts_category_selector_output_and_variants(raw, expected):
    assert normalize_category(raw) == expected
    assert get_response(raw) in RESPONSES[expected]


def test_category_counts_match_spec():
    assert len(RESPONSES["positive"]) == 10
    assert len(RESPONSES["non-committal"]) == 5
    assert len(RESPONSES["negative"]) == 5


def test_custom_answers_are_used():
    custom = {"positive": ["Heck yes"], "non-committal": [], "negative": []}
    seen = {get_response("positive", custom) for _ in range(500)}
    assert "Heck yes" in seen
    assert seen <= set(RESPONSES["positive"]) | {"Heck yes"}


def test_custom_answers_stay_in_their_category():
    custom = {"negative": ["Absolutely not"]}
    for _ in range(200):
        assert get_response("positive", custom) != "Absolutely not"


def test_empty_custom_dict_is_fine():
    assert get_response("negative", {}) in RESPONSES["negative"]


def test_seeded_rng_is_repeatable():
    a = get_response("positive", rng=random.Random(42))
    b = get_response("positive", rng=random.Random(42))
    assert a == b


@pytest.mark.parametrize("bad", ["Invalid number", "maybe", ""])
def test_invalid_category_raises_value_error(bad):
    with pytest.raises(ValueError):
        get_response(bad)


@pytest.mark.parametrize("bad", [None, 3, ["positive"]])
def test_non_string_category_raises_type_error(bad):
    with pytest.raises(TypeError):
        get_response(bad)


def test_custom_answers_must_be_dict():
    with pytest.raises(TypeError):
        get_response("positive", custom_answers=["Heck yes"])


def test_custom_answers_with_bad_key_raises():
    with pytest.raises(ValueError):
        get_response("positive", custom_answers={"sorta": ["eh"]})
