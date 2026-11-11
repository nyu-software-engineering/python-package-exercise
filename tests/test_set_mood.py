import pytest
from desktop_cat import Cat, MOODS

def test_set_mood_changes_mood():
    cat = Cat()
    cat.set_mood("sad")

    assert cat.mood == "sad"

@pytest.mark.parametrize("mood", MOODS)
def test_set_mood_valid_moods(mood):
    cat = Cat()
    cat.set_mood(mood)

    assert cat.mood == mood

def test_set_mood_case_insensitive():
    cat = Cat()
    cat.set_mood("ANGRY")

    assert cat.mood == "angry"


def test_set_mood_removes_whitespace():
    cat = Cat()
    cat.set_mood("  tired  ")

    assert cat.mood == "tired"


@pytest.mark.parametrize("mood", [123, None, True, [], 3.5])
def test_set_mood_invalid_type(mood):
    cat = Cat()

    with pytest.raises(TypeError):
        cat.set_mood(mood)


@pytest.mark.parametrize("mood", ["excited", "scared", "", "sleepy"])
def test_set_mood_invalid_mood(mood):
    cat = Cat()

    with pytest.raises(ValueError):
        cat.set_mood(mood)


def test_set_mood_invalid_input_keeps_original_mood():
    cat = Cat()
    original_mood = cat.mood

    with pytest.raises(ValueError):
        cat.set_mood("excited")

    assert cat.mood == original_mood


def test_set_mood_resets_last_action():
    cat = Cat()
    cat.last_action = "eating"

    cat.set_mood("angry")

    assert cat.last_action == "idle"
    assert cat.visual_state() == "angry"


def test_set_mood_updates_render():
    cat = Cat()
    cat.set_mood("angry")

    assert "( >.< )" in cat.render()
