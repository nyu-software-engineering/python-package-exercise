import pytest
from terminal_pet_respin import get_stage

@pytest.mark.parametrize("commands_run, expected", [
    (0, "egg"),
    (24, "egg"),
    (25, "cracking"),
    (49, "cracking"),
    (50, "hatchling"),
    (99, "hatchling"),
    (100, "young python"),
    (199, "young python"),
    (200, "full python"),
    (10_000, "full python"),
])
def test_stage_boundaries_default_threshold(commands_run, expected):
    assert get_stage(commands_run, 50) == expected


def test_stage_scales_with_custom_threshold():
    assert get_stage(4, 10) == "egg"
    assert get_stage(5, 10) == "cracking"
    assert get_stage(10, 10) == "hatchling"
    assert get_stage(20, 10) == "young python"
    assert get_stage(40, 10) == "full python"


def test_odd_threshold_has_no_rounding_gap():
    assert get_stage(1, 3) == "egg"
    assert get_stage(2, 3) == "cracking"
    assert get_stage(3, 3) == "hatchling"


def test_threshold_of_one():
    assert get_stage(0, 1) == "egg"
    assert get_stage(1, 1) == "hatchling"
    assert get_stage(4, 1) == "full python"


@pytest.mark.parametrize("commands_run, hatch_at", [(-1, 50), (0, 0), (10, -5)])
def test_invalid_values_raise_value_error(commands_run, hatch_at):
    with pytest.raises(ValueError):
        get_stage(commands_run, hatch_at)


@pytest.mark.parametrize("commands_run, hatch_at", [
    ("5", 50), (5.0, 50), (5, 50.0), (True, 50), (5, None),
])
def test_non_integer_inputs_raise_type_error(commands_run, hatch_at):
    with pytest.raises(TypeError):
        get_stage(commands_run, hatch_at)
