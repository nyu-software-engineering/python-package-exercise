import json

import pytest

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
    }
    assert json.loads(path.read_text(encoding="utf-8"))["name"] == "Mochi"


def test_save_rejects_a_bad_pet(tmp_path):
    path = tmp_path / "pet.json"

    with pytest.raises(ValueError):
        save_pet({"name": "   "}, path)

    assert not path.exists()


def test_load_rejects_invalid_json(tmp_path):
    path = tmp_path / "pet.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_pet(path)


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_pet(tmp_path / "missing.json")