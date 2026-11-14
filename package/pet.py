MIN_STAT = 0
MAX_STAT = 100

STATS = ("energy", "hunger", "hygiene", "happiness", "health")

DEFAULT_STATS = {
    "energy": MAX_STAT,
    "hunger": MIN_STAT,
    "hygiene": MAX_STAT,
    "happiness": MAX_STAT,
    "health": MAX_STAT,
}


def create_pet(name):
    """Return a new pet with full stats."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    return {"name": name.strip(), "alive": True, "history": [], **DEFAULT_STATS}


def clamp(value):
    """Keep a stat between MIN_STAT and MAX_STAT."""
    return max(MIN_STAT, min(value, MAX_STAT))


def check_count(value, name):
    """Raise unless value is a non-negative int."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")
    if value < 0:
        raise ValueError(f"{name} can't be negative")


def check_pet(pet, stat):
    """Validate that pet has the given stat with a valid integer value."""
    if not isinstance(pet, dict) or stat not in pet:
        raise TypeError(f"pet must be a dict with a '{stat}' key")

    value = pet[stat]

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{stat} must be an int")

    if value < MIN_STAT or value > MAX_STAT:
        raise ValueError(f"{stat} must be between {MIN_STAT} and {MAX_STAT}")
