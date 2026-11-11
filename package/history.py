"""Record what happened to a pet and read those events back."""

from .pet import MAX_STAT, MIN_STAT, STATS, check_count

ACTIONS = ("feed", "play", "clean", "stat")


def _check_bound(value, name):
    """Raise unless value is an int stat, or None."""
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")
    if value < MIN_STAT or value > MAX_STAT:
        raise ValueError(f"{name} must be between {MIN_STAT} and {MAX_STAT}")


def record_event(pet, action, detail=None, stat=None, before=None, after=None):
    """Append one event and return a copy of it."""
    if not isinstance(pet, dict):
        raise TypeError("pet must be a dict")
    if action not in ACTIONS:
        raise ValueError("action must be feed, play, clean, or stat")
    if detail is not None and not isinstance(detail, str):
        raise TypeError("detail must be a string")
    if stat is not None and stat not in STATS:
        raise ValueError("stat must be energy, hunger, hygiene, happiness, or health")
    if action == "stat" and stat is None:
        raise ValueError("stat is required when action is 'stat'")
    _check_bound(before, "before")
    _check_bound(after, "after")
    if (before is None) != (after is None):
        raise ValueError("before and after must both be set or both be omitted")

    event = {
        "action": action,
        "detail": detail,
        "stat": stat,
        "before": before,
        "after": after,
    }
    history = pet.setdefault("history", [])
    if not isinstance(history, list):
        raise TypeError("history must be a list")
    history.append(event)
    return dict(event)


def get_history(pet, limit):
    """Return the most recent events, oldest of that slice first."""
    if not isinstance(pet, dict):
        raise TypeError("pet must be a dict")
    check_count(limit, "limit")

    history = pet.get("history", [])
    if not isinstance(history, list):
        raise TypeError("history must be a list")
    if limit == 0:
        return []
    return [dict(event) for event in history[-limit:]]