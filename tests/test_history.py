import pytest

from package.history import get_history, record_event
from package.hunger import feed
from package.hygiene import clean
from package.pet import create_pet


def test_get_history_returns_recent_events_in_order():
    pet = create_pet("Mochi")
    record_event(pet, "feed", stat="hunger", before=40, after=0)
    record_event(pet, "play", detail="catch", stat="happiness", before=70, after=80)
    record_event(pet, "clean", stat="hygiene", before=50, after=100)
    record_event(pet, "stat", stat="energy", before=100, after=90)

    recent = get_history(pet, 2)
    everything = get_history(pet, 10)
    nothing = get_history(pet, 0)

    assert [event["action"] for event in recent] == ["clean", "stat"]
    assert recent[0]["before"] == 50 and recent[0]["after"] == 100
    assert [event["action"] for event in everything] == ["feed", "play", "clean", "stat"]
    assert everything[1]["detail"] == "catch"
    assert nothing == []


def test_get_history_returns_copies():
    pet = create_pet("Mochi")
    record_event(pet, "play", detail="walk", stat="happiness", before=70, after=75)

    recent = get_history(pet, 1)
    recent.clear()
    recent_again = get_history(pet, 1)
    recent_again[0]["detail"] = "changed"

    assert len(pet["history"]) == 1
    assert pet["history"][0]["detail"] == "walk"
    assert get_history(pet, 1)[0]["detail"] == "walk"


def test_missing_history_is_empty():
    assert get_history({}, 3) == []


def test_feed_and_clean_record_events():
    pet = create_pet("Mochi")
    pet["hunger"] = 40
    pet["hygiene"] = 50

    assert feed(pet) == 0
    assert clean(pet) == 100

    recent = get_history(pet, 2)
    assert [event["action"] for event in recent] == ["feed", "clean"]
    assert recent[0]["before"] == 40 and recent[0]["after"] == 0
    assert recent[1]["stat"] == "hygiene" and recent[1]["after"] == 100


def test_record_event_rejects_bad_input():
    pet = create_pet("Mochi")

    with pytest.raises(ValueError):
        record_event(pet, "nap")
    with pytest.raises(ValueError):
        record_event(pet, "stat")
    with pytest.raises(TypeError):
        record_event("Mochi", "feed")

    assert get_history(pet, 5) == []


@pytest.mark.parametrize(
    ("limit", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (-1, ValueError),
    ],
)
def test_get_history_rejects_bad_limit(limit, error):
    pet = create_pet("Mochi")

    with pytest.raises(error):
        get_history(pet, limit)