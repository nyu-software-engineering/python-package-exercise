from datetime import datetime, timedelta, timezone

from .pet import check_pet
from .health import DEATH_HEALTH

INACTIVE_DAYS = 7


def check_death(pet, last_opened=None, now=None):
    #Check if the pet has died from low health or inactivity.

    check_pet(pet, "health")

    if "alive" not in pet or not isinstance(pet["alive"], bool):
        raise TypeError("alive must be a bool")

    
    if not pet["alive"]:
        return True

    
    if pet["health"] <= DEATH_HEALTH:
        pet["alive"] = False
        return True

    
    if last_opened is not None:
        if not isinstance(last_opened, str):
            raise TypeError("last_opened must be a string")

        try:
            last_date = datetime.fromisoformat(last_opened)
        except ValueError:
            raise ValueError("last_opened must be a valid date")

        if now is None:
            now = datetime.now(timezone.utc)

        if not isinstance(now, datetime):
            raise TypeError("now must be a datetime")

        if last_date.tzinfo is None or now.tzinfo is None:
            raise ValueError("dates must include a timezone")

        if last_date > now:
            raise ValueError("last_opened cannot be in the future")

        if now - last_date >= timedelta(days=INACTIVE_DAYS):
            pet["alive"] = False
            return True

    return False
