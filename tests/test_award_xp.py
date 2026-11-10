import pytest

from progression import award_xp


def test_award_xp():
    assert award_xp(0, 60) == {"totalXP": 60, "level": 1}
    assert award_xp(40, 60) == {"totalXP": 100, "level": 2}
    assert award_xp(90, 250) == {"totalXP": 340, "level": 4}


def test_rewards_add_to_previous_total():
    first = award_xp(0, 45)
    second = award_xp(first["totalXP"], 60)

    assert first == {"totalXP": 45, "level": 1}
    assert second == {"totalXP": 105, "level": 2}


@pytest.mark.parametrize("total_xp", [-1, -100])
def test_negative_total_xp(total_xp):
    with pytest.raises(ValueError):
        award_xp(total_xp, 250)


@pytest.mark.parametrize("duration", [0, -1])
def test_invalid_duration(duration):
    with pytest.raises(ValueError):
        award_xp(100, duration)


@pytest.mark.parametrize("total_xp", [None, "90", 90.0, True, False])
def test_invalid_total_xp_type(total_xp):
    with pytest.raises(TypeError):
        award_xp(total_xp, 60)


@pytest.mark.parametrize("duration", [None, "60", 60.0, True, False])
def test_invalid_duration_type(duration):
    with pytest.raises(TypeError):
        award_xp(100, duration)