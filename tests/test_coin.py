import pytest

from pyDeciders.coin import flip_coin


# valid inputs

def test_default_is_one_flip():
    result = flip_coin()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] in ("heads", "tails")


def test_times_controls_number_of_flips():
    result = flip_coin(times=10)
    assert len(result) == 10
    assert all(side in ("heads", "tails") for side in result)


def test_same_seed_gives_same_result():
    assert flip_coin(times=20, seed=42) == flip_coin(times=20, seed=42)
    assert flip_coin(times=20, seed=1) != flip_coin(times=20, seed=2)


def test_bias_one_is_always_heads():
    assert flip_coin(times=50, bias=1) == ["heads"] * 50
    assert flip_coin(times=50, bias=1.0, seed=7) == ["heads"] * 50


def test_bias_zero_is_always_tails():
    assert flip_coin(times=50, bias=0) == ["tails"] * 50
    assert flip_coin(times=50, bias=0.0, seed=7) == ["tails"] * 50


def test_bias_shifts_the_odds():
    heads = flip_coin(times=1000, bias=0.9, seed=0).count("heads")
    assert heads > 800
    tails = flip_coin(times=1000, bias=0.1, seed=0).count("tails")
    assert tails > 800


def test_fair_coin_is_roughly_even():
    heads = flip_coin(times=1000, seed=123).count("heads")
    assert 400 < heads < 600


#invalid inputs

@pytest.mark.parametrize("bad_times", [0, -1, -100])
def test_times_below_one_raises_value_error(bad_times):
    with pytest.raises(ValueError):
        flip_coin(times=bad_times)


@pytest.mark.parametrize("bad_times", [2.5, "3", None, True])
def test_times_wrong_type_raises_type_error(bad_times):
    with pytest.raises(TypeError):
        flip_coin(times=bad_times)


@pytest.mark.parametrize("bad_bias", [-0.1, 1.1, 5])
def test_bias_out_of_range_raises_value_error(bad_bias):
    with pytest.raises(ValueError):
        flip_coin(bias=bad_bias)


@pytest.mark.parametrize("bad_bias", ["0.5", None, True])
def test_bias_wrong_type_raises_type_error(bad_bias):
    with pytest.raises(TypeError):
        flip_coin(bias=bad_bias)