
"""Display the Tamagotchi as an ASCII cat."""

HAPPY_LEVEL = 70
NEUTRAL_LEVEL = 35
DEATH_HEALTH = 10


def show_pet(pet):
    """Return the Tamagotchi's appearance based on its stats."""

    if not isinstance(pet, dict):
        raise TypeError("pet must be a dictionary")

    for stat in ("happiness", "health", "alive"):
        if stat not in pet:
            raise TypeError(f"pet must have a '{stat}' key")

    happiness = pet["happiness"]
    health = pet["health"]
    alive = pet["alive"]

    if type(happiness) is not int:
        raise TypeError("happiness must be an int")
    if happiness < 0 or happiness > 100:
        raise ValueError("happiness must be between 0 and 100")

    if type(health) is not int:
        raise TypeError("health must be an int")
    if health < 0 or health > 100:
        raise ValueError("health must be between 0 and 100")

    if not isinstance(alive, bool):
        raise TypeError("alive must be a bool")

    if not alive or health <= DEATH_HEALTH:
        face = "( x.x )"
        mouth = "> _ <"
    elif happiness >= HAPPY_LEVEL:
        face = "( ^.^ )"
        mouth = "> w <"
    elif happiness >= NEUTRAL_LEVEL:
        face = "( o.o )"
        mouth = "> - <"
    else:
        face = "( ;.; )"
        mouth = "> n <"

    cat = (
        "     /\\_/\\\n"
        f"    {face}\n"
        f"     {mouth}"
    )

    return cat

