import pytest
from desktop_cat import Cat, MOODS

def test_render_returns_string():
    cat = Cat()
    result = cat.render()

    assert isinstance(result, str)
    assert result != ""

def test_render_not_empty():
    cat = Cat()
    result = cat.render()
    assert result != ""

def test_render_strips_whitesspace():
    cat = Cat()
    result = cat.render()
    assert result.strip() != ""
    assert "\n\n" not in result

def test_render_changes_with_mood():
    cat = Cat(mood="happy")
    happy_cat = cat.render()

    cat.mood = "sad"
    sad_cat = cat.render()

    assert happy_cat != sad_cat


@pytest.mark.parametrize("mood", MOODS)
def test_render_valid_moods(mood):
    cat = Cat(mood=mood)
    result = cat.render()

    assert isinstance(result,str)
    assert result != ""

@pytest.mark.parametrize(
        "action", ["eating", "petted", "sleeping", "speaking"]
)
def test_render_action_changes_art(action):
    cat = Cat(mood="happy")
    normal_cat = cat.render()

    cat.last_action = action
    action_cat = cat.render()

    assert action_cat != normal_cat

def test_render_action_overrides_mood():
    cat = Cat(mood = "happy")
    cat.last_action = "eating"
    first = cat.render()

    cat.mood = "sad"
    second = cat.render()

    assert first == second

def test_render_high_hunger_shows_hungry():
    cat = Cat(mood = "happy")
    cat.hunger = 9
    hungry_cat = cat.render()

    cat.hunger = 5
    cat.mood = "hungry"

    assert cat.render() == hungry_cat

def test_render_high_sleepiness_shows_tired():
    cat = Cat(mood="happy")
    cat.sleepiness = 8
    tired_cat = cat.render()
    
    cat.sleepiness = 5
    cat.mood = "tired"
    
    assert cat.render() == tired_cat

def test_render_action_overrides_hunger():
    cat = Cat(mood="happy")
    cat.hunger = 9
    hungry_cat = cat.render()

    cat.last_action = "eating"
    eating_cat = cat.render()

    assert eating_cat != hungry_cat


def test_render_does_not_print(capsys):
    cat = Cat()
    cat.render()

    captured = capsys.readouterr()
    assert captured.out == ""

def test_render_does_not_change_mood():
    cat = Cat(mood = "happy")
    cat.render()
    assert cat.mood == "happy"


def test_render_does_not_change_last_action():
    cat = Cat()
    cat.last_action = "eating"
    cat.render()
    assert cat.last_action == "eating"
