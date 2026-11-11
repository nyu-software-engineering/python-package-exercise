"""Save a pet to JSON and load it back."""

import json
from pathlib import Path

from .pet import MAX_STAT, MIN_STAT, STATS

PET_FIELDS = ("name", "alive", *STATS)


def _check_pet_record(pet):
    """Raise unless pet has a name, alive flag, and every stat."""
    if not isinstance(pet, dict):
        raise TypeError("pet must be a dict")

    for field in PET_FIELDS:
        if field not in pet:
            raise TypeError(f"pet must be a dict with a '{field}' key")

    if not isinstance(pet["name"], str) or not pet["name"].strip():
        raise ValueError("name must be a non-empty string")

    if not isinstance(pet["alive"], bool):
        raise TypeError("alive must be a bool")

    for stat in STATS:
        value = pet[stat]
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{stat} must be an int")
        if value < MIN_STAT or value > MAX_STAT:
            raise ValueError(f"{stat} must be between {MIN_STAT} and {MAX_STAT}")

    if "history" in pet:
        history = pet["history"]
        if not isinstance(history, list) or not all(isinstance(event, dict) for event in history):
            raise TypeError("history must be a list of dicts")

    if "last_seen" in pet:
        last_seen = pet["last_seen"]
        if isinstance(last_seen, bool) or not isinstance(last_seen, int):
            raise TypeError("last_seen must be an int")
        if last_seen < 0:
            raise ValueError("last_seen can't be negative")


def _record(pet):
    """Copy only the fields that get stored."""
    data = {"name": pet["name"].strip(), "alive": pet["alive"]}
    data.update({stat: pet[stat] for stat in STATS})
    if "history" in pet:
        data["history"] = [dict(event) for event in pet["history"]]
    if "last_seen" in pet:
        data["last_seen"] = pet["last_seen"]
    return data


def save_pet(pet, path):
    """Write the pet's name, current stats, history, and last_seen to a JSON file."""
    _check_pet_record(pet)
    destination = Path(path)
    destination.write_text(
        json.dumps(_record(pet), indent=2) + "\n",
        encoding="utf-8",
    )
    return destination


def load_pet(path):
    """Read a pet back from a JSON file."""
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("save file is not valid JSON") from error

    _check_pet_record(raw)
    return _record(raw)