
from .health import HEALTHY_HUNGER, HEALTHY_STAT, DEATH_HEALTH
from .pet import STATS, check_pet


def _validate_pet(pet):
    """Validate all pet stats and the alive flag."""
    for stat in STATS:
        check_pet(pet, stat)

    if not isinstance(pet.get("alive"), bool):
        raise TypeError("alive must be a bool")


def diagnose_pet(pet):
    """Return a list of health issues affecting the pet."""
    _validate_pet(pet)

    if not pet["alive"] or pet["health"] <= DEATH_HEALTH:
        return ["Your pet has passed away."]

    issues = []

    if pet["hunger"] > HEALTHY_HUNGER:
        issues.append("Your pet is hungry. Feed it!")

    if pet["energy"] < HEALTHY_STAT:
        issues.append("Your pet is tired. Let it rest!")

    if pet["hygiene"] < HEALTHY_STAT:
        issues.append("Your pet is dirty. Give it a bath!")

    if pet["happiness"] < HEALTHY_STAT:
        issues.append("Your pet is sad. Play with it!")

    if pet["health"] <= 30:
        issues.append("Your pet is critically unhealthy!")

    if not issues:
        return ["Your pet is healthy and happy!"]

    return issues


def recommend_action(pet):
    """Recommend care for the pet's most urgent need."""
    _validate_pet(pet)

    if not pet["alive"] or pet["health"] <= DEATH_HEALTH:
        return "Your pet has passed away."

    needs = {
        "feed": max(pet["hunger"] - HEALTHY_HUNGER, 0),
        "rest": max(HEALTHY_STAT - pet["energy"], 0),
        "clean": max(HEALTHY_STAT - pet["hygiene"], 0),
        "play": max(HEALTHY_STAT - pet["happiness"], 0),
    }

    most_urgent = max(needs, key=needs.get)

    if needs[most_urgent] == 0:
        return "Your pet is healthy! Keep taking good care of it."

    recommendations = {
        "feed": "Feed your pet to reduce its hunger.",
        "rest": "Let your pet rest to restore energy.",
        "clean": "Give your pet a bath to improve hygiene.",
        "play": "Play with your pet to improve happiness.",
    }

    return recommendations[most_urgent]
