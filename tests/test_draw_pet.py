import pytest

from terminal_pet_respin import STAGES, draw_pet, get_stage, pet_says
from terminal_pet_respin.draw_pet import MOODS


def test_returns_string_for_every_stage():
    for stage in STAGES:
        art = draw_pet(stage)
        assert isinstance(art, str)
        assert art.strip() != ""


def test_each_stage_has_different_art():
    drawings = [draw_pet(stage, easter_override=False) for stage in STAGES]
    assert len(set(drawings)) == len(STAGES)


def test_whole_egg_has_no_eyes():
    art = draw_pet("egg", easter_override=False)
    assert "O O" not in art
    assert "( " not in art
    assert "/\\/\\" not in art


def test_eyes_show_once_the_shell_cracks():
    for stage in STAGES[1:]:
        assert "O O" in draw_pet(stage)


def test_tongue_shows_only_when_grown():
    assert "~<" not in draw_pet("egg", easter_override=False)
    assert "~<" not in draw_pet("hatchling")
    assert "~<" in draw_pet("young python")
    assert "~<" in draw_pet("full python")


def test_full_python_is_the_biggest():
    sizes = [len(draw_pet(stage)) for stage in STAGES]
    assert max(sizes) == len(draw_pet("full python"))


def test_works_with_get_stage_output():
    for commands_run in (0, 30, 50, 120, 500):
        stage = get_stage(commands_run, 50)
        assert isinstance(draw_pet(stage, easter_override=False), str)


def test_unknown_stage_raises_value_error():
    with pytest.raises(ValueError):
        draw_pet("dragon")
    with pytest.raises(ValueError):
        draw_pet("", easter_override=False)
    with pytest.raises(ValueError):
        draw_pet("Egg", easter_override=False)


def test_non_string_stage_raises_type_error():
    with pytest.raises(TypeError):
        draw_pet(3)
    with pytest.raises(TypeError):
        draw_pet(None)
    with pytest.raises(TypeError):
        draw_pet(["egg"], easter_override=False)


def test_no_message_means_no_bubble():
    assert draw_pet("egg") == draw_pet("egg", None, easter_override=False)
    assert draw_pet("egg", "") == draw_pet("egg", easter_override=False)
    assert "<" not in draw_pet("egg", easter_override=False)


def test_message_appears_in_bubble_above_art():
    art = draw_pet("hatchling", "I'm out!")
    assert "< I'm out! >" in art
    assert art.endswith(draw_pet("hatchling", easter_override=False))


def test_bubble_width_matches_message():
    lines = draw_pet("egg", "hi", easter_override=False).splitlines()
    assert lines[0] == " " + "_" * 4
    assert lines[1] == "< hi >"
    assert lines[2] == " " + "-" * 4


def test_message_must_be_a_string():
    with pytest.raises(TypeError):
        draw_pet("egg", 42)
    with pytest.raises(TypeError):
        draw_pet("egg", ["hi"], easter_override=False)


def test_every_stage_has_its_own_message():
    messages = [pet_says(stage) for stage in STAGES]
    assert all(isinstance(m, str) and m for m in messages)
    assert len(set(messages)) == len(STAGES)


def test_pet_says_rejects_bad_stage():
    with pytest.raises(ValueError):
        pet_says("dragon")
    with pytest.raises(TypeError):
        pet_says(5)


def test_easter_egg():
    # Test that the easter egg art is returned on Easter
    easter_art = draw_pet("egg", easter_override=True)
    assert "O O" not in easter_art
    assert "/\\/\\/\\/" in easter_art

GROWN_STAGES = STAGES[1:]  # every stage after the plain egg has a face

def test_default_mood_is_surprised():
    for stage in STAGES:
        assert draw_pet(stage, easter_override=False) == draw_pet(stage, easter_override=False, mood="surprised")
        assert draw_pet(stage, "hi") == draw_pet(stage, "hi", mood="surprised")

def test_every_mood_has_three_character_eyes():
    assert "surprised" in MOODS
    for eyes in MOODS.values():
        assert isinstance(eyes, str)
        assert len(eyes) == 3


def test_each_mood_shows_its_own_eyes():
    for stage in GROWN_STAGES:
        for mood, eyes in MOODS.items():
            assert eyes in draw_pet(stage, mood=mood)


def test_each_mood_gives_different_art():
    for stage in GROWN_STAGES:
        drawings = [draw_pet(stage, mood=mood) for mood in MOODS]
        assert len(set(drawings)) == len(MOODS)


def test_other_moods_replace_the_surprised_eyes():
    for stage in GROWN_STAGES:
        for mood in MOODS:
            if mood != "surprised":
                assert "O O" not in draw_pet(stage, mood=mood)


def test_mood_does_not_change_the_egg():
    for mood in MOODS:
        assert draw_pet("egg", easter_override=False, mood=mood) == draw_pet("egg", easter_override=False)
        assert draw_pet("egg", easter_override=True, mood=mood) == draw_pet("egg", easter_override=True)


def test_mood_works_with_speech_bubble():
    art = draw_pet("hatchling", pet_says("hatchling"), mood="happy")
    assert f"< {pet_says('hatchling')} >" in art
    assert "^ ^" in art
    assert art.endswith(draw_pet("hatchling", mood="happy"))


def test_mood_never_changes_the_message():
    art = draw_pet("young python", "O O", mood="sleepy")
    assert "< O O >" in art
    assert "- -" in art


def test_unknown_mood_raises_value_error():
    with pytest.raises(ValueError):
        draw_pet("hatchling", mood="furious")
    with pytest.raises(ValueError):
        draw_pet("hatchling", mood="")
    with pytest.raises(ValueError):
        draw_pet("hatchling", mood="Happy")


def test_non_string_mood_raises_type_error():
    with pytest.raises(TypeError):
        draw_pet("hatchling", mood=1)
    with pytest.raises(TypeError):
        draw_pet("hatchling", mood=None)
    with pytest.raises(TypeError):
        draw_pet("hatchling", mood=["happy"])


def test_bad_stage_still_raises_with_a_mood():
    with pytest.raises(ValueError):
        draw_pet("dragon", mood="happy")
    with pytest.raises(TypeError):
        draw_pet(5, mood="happy")