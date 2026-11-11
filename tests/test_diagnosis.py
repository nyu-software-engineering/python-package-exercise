
import pytest

from package.diagnosis import diagnose_pet, recommend_action
from package.pet import STATS


def make_pet():
    return {
        "hunger": 20,
        "energy": 80,
        "hygiene": 80,
        "happiness": 80,
        "health": 100,
        "alive": True,
    }


def test_diagnose_healthy_pet():
    pet = make_pet()

    assert diagnose_pet(pet) == [
        "Your pet is healthy and happy!"
    ]


def test_diagnose_multiple_issues():
    pet = make_pet()
    pet.update({
        "hunger": 80,
        "energy": 20,
        "hygiene": 30,
        "happiness": 40,
        "health": 25,
    })

    issues = diagnose_pet(pet)

    assert len(issues) == 5
    assert "Your pet is hungry. Feed it!" in issues
    assert "Your pet is tired. Let it rest!" in issues
    assert "Your pet is dirty. Give it a bath!" in issues
    assert "Your pet is sad. Play with it!" in issues
    assert "Your pet is critically unhealthy!" in issues


def test_diagnose_healthy_boundaries():
    pet = make_pet()
    pet.update({
        "hunger": 40,
        "energy": 60,
        "hygiene": 60,
        "happiness": 60,
    })

    assert diagnose_pet(pet) == [
        "Your pet is healthy and happy!"
    ]


def test_diagnose_dead_pet():
    pet = make_pet()
    pet["alive"] = False

    assert diagnose_pet(pet) == [
        "Your pet has passed away."
    ]

    pet["alive"] = True
    pet["health"] = 10

    assert diagnose_pet(pet) == [
        "Your pet has passed away."
    ]


@pytest.mark.parametrize(
    ("stat", "value", "error"),
    [
        ("hunger", -1, ValueError),
        ("energy", 101, ValueError),
        ("hygiene", None, TypeError),
        ("happiness", "80", TypeError),
        ("health", True, TypeError),
    ],
)
def test_diagnose_invalid_stats(stat, value, error):
    pet = make_pet()
    pet[stat] = value

    with pytest.raises(error):
        diagnose_pet(pet)


@pytest.mark.parametrize("stat", STATS)
def test_diagnose_missing_stats(stat):
    pet = make_pet()
    del pet[stat]

    with pytest.raises(TypeError):
        diagnose_pet(pet)


def test_recommend_healthy_pet():
    pet = make_pet()

    assert "healthy" in recommend_action(pet)


@pytest.mark.parametrize(
    ("stat", "value", "expected"),
    [
        ("hunger", 90, "Feed"),
        ("energy", 10, "rest"),
        ("hygiene", 10, "bath"),
        ("happiness", 10, "Play"),
    ],
)
def test_recommend_single_issue(stat, value, expected):
    pet = make_pet()
    pet[stat] = value

    assert expected in recommend_action(pet)


def test_recommend_most_urgent():
    pet = make_pet()
    pet.update({
        "hunger": 60,
        "energy": 10,
        "hygiene": 40,
    })

    assert "rest" in recommend_action(pet)


def test_recommend_priority_tie():
    pet = make_pet()
    pet.update({
        "hunger": 80,
        "energy": 20,
    })

    assert "Feed" in recommend_action(pet)


def test_recommend_dead_pet():
    pet = make_pet()
    pet["alive"] = False

    assert recommend_action(pet) == (
        "Your pet has passed away."
    )


def test_diagnosis_does_not_modify_pet():
    pet = make_pet()
    original = pet.copy()

    diagnose_pet(pet)
    recommend_action(pet)

    assert pet == original


@pytest.mark.parametrize("value", [None, "yes", 1])
def test_invalid_alive(value):
    pet = make_pet()
    pet["alive"] = value

    with pytest.raises(TypeError):
        diagnose_pet(pet)

    with pytest.raises(TypeError):
        recommend_action(pet)


def test_missing_alive():
    pet = make_pet()
    del pet["alive"]

    with pytest.raises(TypeError):
        diagnose_pet(pet)

    with pytest.raises(TypeError):
        recommend_action(pet)


def test_invalid_recommend_pet():
    pet = make_pet()
    pet["energy"] = -1

    with pytest.raises(ValueError):
        recommend_action(pet)

    with pytest.raises(TypeError):
        recommend_action(None)
