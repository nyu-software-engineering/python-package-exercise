import pytest

from progression import calculate_xp, calculate_level


def test_calculate_xp():
    assert calculate_xp(1) == 1
    assert calculate_xp(30) == 30
    assert calculate_xp(60) == 60


def test_calculate_level():
    assert calculate_level(0) == 1
    assert calculate_level(99) == 1
    assert calculate_level(100) == 2
    assert calculate_level(101) == 2
    assert calculate_level(199) == 2
    assert calculate_level(200) == 3


def test_gain_multiple_levels():
    total_xp = 90
    reward = calculate_xp(250)

    assert calculate_level(total_xp) == 1
    assert total_xp + reward == 340
    assert calculate_level(total_xp + reward) == 4


@pytest.mark.parametrize("duration", [0, -1, -30])
def test_invalid_duration(duration):
    with pytest.raises(ValueError):
        calculate_xp(duration)


@pytest.mark.parametrize("total_xp", [-1, -100])
def test_negative_xp(total_xp):
    with pytest.raises(ValueError):
        calculate_level(total_xp)


@pytest.mark.parametrize("value", [None, "30", 30.0, 1.5, True, False])
def test_invalid_input_types(value):
    with pytest.raises(TypeError):
        calculate_xp(value)

    with pytest.raises(TypeError):
        calculate_level(value)
