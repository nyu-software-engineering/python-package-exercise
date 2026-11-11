import json

import pytest

from package.history import get_history, record_event
from package.pet import create_pet
from package.save_load import load_pet, save_pet


def test_save_and_load_round_trip(tmp_path):
    pet = create_pet("Mochi")
    pet["energy"] = 80
    pet["hunger"] = 20
    pet["hygiene"] = 90
    pet["happiness"] = 70
    pet["health"] = 55
    pet["alive"] = True
    path = tmp_path / "pet.json"

    save_pet(pet, path)
    loaded = load_pet(path)

    assert loaded == {
        "name": "Mochi",
        "alive": True,
        "energy": 80,
        "hunger": 20,
        "hygiene": 90,
        "happiness": 70,
        "health": 55,
        "history": [],
    }
    assert json.loads(path.read_text(encoding="utf-8"))["name"] == "Mochi"


def test_history_survives_save_and_load(tmp_path):
    pet = create_pet("Mochi")
    record_event(pet, "play", detail="walk", stat="happiness", before=70, after=75)
    record_event(pet, "feed", stat="hunger", before=40, after=0)
    path = tmp_path / "pet.json"

    save_pet(pet, path)
    loaded = load_pet(path)

    assert get_history(loaded, 5) == get_history(pet, 5)
    assert [event["action"] for event in get_history(loaded, 5)] == ["play", "feed"]
    assert get_history(loaded, 1)[0]["after"] == 0


def test_save_rejects_a_bad_pet(tmp_path):
    path = tmp_path / "pet.json"
    pet = {
        "name": "   ",
        "alive": True,
        "energy": 100,
        "hunger": 0,
        "hygiene": 100,
        "happiness": 100,
        "health": 100,
    }

    with pytest.raises(ValueError):
        save_pet(pet, path)

    assert not path.exists()


def test_save_rejects_bad_history(tmp_path):
    path = tmp_path / "pet.json"
    pet = create_pet("Mochi")
    pet["history"] = ["not an event"]

    with pytest.raises(TypeError):
        save_pet(pet, path)

    assert not path.exists()


def test_load_rejects_invalid_json(tmp_path):
    path = tmp_path / "pet.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_pet(path)


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_pet(tmp_path / "missing.json")