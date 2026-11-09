from .pet import MAX_STAT, STATS, check_count, check_pet, clamp

HEALTHY_STAT = 60  # baseline health stat level
HEALTHY_HUNGER = 40  # hunger at or below this is healthy
SICK_WELLNESS = 50  # wellness below this starts hurting health
DAMAGE_DIVISOR = 5  # every 5 wellness points below SICK_WELLNESS costs 1 health
REGEN_PER_TICK = 2
DEATH_HEALTH = 10  # pet dies at or below this


def _check_full_pet(pet):
    for stat in STATS:
        check_pet(pet, stat)


def _all_healthy(pet):
    return pet["hunger"] <= HEALTHY_HUNGER and all(
        pet[stat] >= HEALTHY_STAT for stat in ("energy", "hygiene", "happiness")
    )


def wellness(pet):
    """Average of hunger, energy, hygiene and happiness, from 0 to 100."""
    
    _check_full_pet(pet)
    scores = [
        MAX_STAT - pet["hunger"],
        pet["energy"],
        pet["hygiene"],
        pet["happiness"],
    ]
    return sum(scores) / len(scores)


def update_health(pet, ticks=1):
    """Apply `ticks` rounds of health change and return the new health."""
    
    _check_full_pet(pet)
    check_count(ticks, "ticks")

    for _ in range(ticks):
        if not pet.get("alive", True):
            break
        if _all_healthy(pet):
            change = REGEN_PER_TICK
        else:
            change = -int(max(SICK_WELLNESS - wellness(pet), 0) // DAMAGE_DIVISOR)
        pet["health"] = clamp(pet["health"] + change)
        if pet["health"] <= DEATH_HEALTH:
            pet["alive"] = False
    return pet["health"]
