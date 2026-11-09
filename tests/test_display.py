
import pytest

from package.display import show_pet


def test_show_happy():
    pet = {"happiness": 80, "health": 100, "alive": True}

    result = show_pet(pet)

    assert "( ^.^ )" in result
    assert "> w <" in result
    assert "/\\_/\\" in result


def test_show_neutral():
    pet = {"happiness": 50, "health": 100, "alive": True}

    result = show_pet(pet)

    assert "( o.o )" in result
    assert "> - <" in result
    assert "( ^.^ )" not in result


def test_show_sad():
    pet = {"happiness": 20, "health": 100, "alive": True}

    result = show_pet(pet)

    assert "( ;.; )" in result
    assert "> n <" in result
    assert "( ^.^ )" not in result


def test_show_dead():
    pet = {"happiness": 80, "health": 10, "alive": True}

    result = show_pet(pet)

    assert "( x.x )" in result
    assert "> _ <" in result
    assert "( ^.^ )" not in result


def test_show_not_alive():
    pet = {"happiness": 80, "health": 100, "alive": False}

    result = show_pet(pet)

    assert "( x.x )" in result
    assert "> _ <" in result


def test_happiness_boundaries():
    pet = {"happiness": 70, "health": 100, "alive": True}
    assert "( ^.^ )" in show_pet(pet)

    pet["happiness"] = 69
    assert "( o.o )" in show_pet(pet)

    pet["happiness"] = 35
    assert "( o.o )" in show_pet(pet)

    pet["happiness"] = 34
    assert "( ;.; )" in show_pet(pet)


@pytest.mark.parametrize(
    "happiness",
    [-1, 101]
)
def test_invalid_happiness_range(happiness):
    pet = {"happiness": happiness, "health": 100, "alive": True}

    with pytest.raises(ValueError):
        show_pet(pet)


@pytest.mark.parametrize(
    "health",
    [-1, 101]
)
def test_invalid_health_range(health):
    pet = {"happiness": 80, "health": health, "alive": True}

    with pytest.raises(ValueError):
        show_pet(pet)


@pytest.mark.parametrize(
    "value",
    [None, "80", True, 50.5]
)
def test_invalid_happiness_type(value):
    pet = {"happiness": value, "health": 100, "alive": True}

    with pytest.raises(TypeError):
        show_pet(pet)


def test_missing_stats():
    with pytest.raises(TypeError):
        show_pet({"health": 100, "alive": True})

    with pytest.raises(TypeError):
        show_pet({"happiness": 80, "alive": True})


def test_pet_not_modified():
    pet = {"happiness": 80, "health": 100, "alive": True}
    original = pet.copy()

    show_pet(pet)

    assert pet == original
