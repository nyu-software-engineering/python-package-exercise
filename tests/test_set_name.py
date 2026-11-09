import pytest
from desktop_cat import Cat


def test_set_name_changes_name():
    cat = Cat()
    cat.set_name("Mochi")
    assert cat.name == "Mochi"


def test_set_name_strips_whitespace():
    cat = Cat()
    cat.set_name("   Luna  ")
    assert cat.name == "Luna"


def test_set_name_keeps_capitalization():
    cat = Cat()
    cat.set_name("Mr. Biscuits")
    assert cat.name == "Mr. Biscuits"


def test_set_name_returns_message():
    cat = Cat(name="Whiskers")
    result = cat.set_name("Mochi")
    assert result == "Whiskers is now called Mochi!"


def test_set_name_shows_in_status():
    cat = Cat()
    cat.set_name("Mochi")
    assert cat.status().startswith("Mochi")


def test_set_name_empty_raises():
    cat = Cat()
    with pytest.raises(ValueError):
        cat.set_name("   ")


def test_set_name_too_long_raises():
    cat = Cat()
    with pytest.raises(ValueError):
        cat.set_name("a" * 21)


def test_set_name_non_string_raises():
    cat = Cat()
    with pytest.raises(TypeError):
        cat.set_name(123)


def test_set_name_invalid_keeps_old_name():
    cat = Cat(name="Whiskers")
    with pytest.raises(ValueError):
        cat.set_name("")
    assert cat.name == "Whiskers"