import pytest

from draw_pet import draw_pet
from get_stage import STAGES, get_stage


def test_returns_string_for_every_stage():
    for stage in STAGES:
        art = draw_pet(stage)
        assert isinstance(art, str)
        assert art.strip() != ""


def test_each_stage_has_different_art():
    drawings = [draw_pet(stage) for stage in STAGES]
    assert len(set(drawings)) == len(STAGES)


def test_whole_egg_has_no_eyes():
    art = draw_pet("egg")
    assert "O O" not in art
    assert "( " not in art
    assert "/\\/\\" not in art


def test_eyes_show_once_the_shell_cracks():
    for stage in STAGES[1:]:
        assert "O O" in draw_pet(stage)


def test_tongue_shows_only_when_grown():
    assert "~<" not in draw_pet("egg")
    assert "~<" not in draw_pet("hatchling")
    assert "~<" in draw_pet("young python")
    assert "~<" in draw_pet("full python")


def test_full_python_is_the_biggest():
    sizes = [len(draw_pet(stage)) for stage in STAGES]
    assert max(sizes) == len(draw_pet("full python"))


def test_works_with_get_stage_output():
    for commands_run in (0, 30, 50, 120, 500):
        stage = get_stage(commands_run, 50)
        assert isinstance(draw_pet(stage), str)


def test_unknown_stage_raises_value_error():
    with pytest.raises(ValueError):
        draw_pet("dragon")
    with pytest.raises(ValueError):
        draw_pet("")
    with pytest.raises(ValueError):
        draw_pet("Egg")


def test_non_string_stage_raises_type_error():
    with pytest.raises(TypeError):
        draw_pet(3)
    with pytest.raises(TypeError):
        draw_pet(None)
    with pytest.raises(TypeError):
        draw_pet(["egg"])