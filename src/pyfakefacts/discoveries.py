"""Generate fictional scientific discoveries."""

import random

#types of discoveries and their corresponding absurdity levels
DISCOVERIES = {
    "physics": {
        "subjects": ["electrons", "photons", "magnetic fields"],
        "low": [
            "respond to unusual sound frequencies",
            "behave differently under colored lights",
        ],
        "medium": [
            "change direction when people sneeze",
            "become stronger around electronic devices",
        ],
        "high": [
            "take a lunch break every Thursday",
            "secretly communicate using interpretive dance",
        ],
    },
    "biology": {
        "subjects": ["mushrooms", "jellyfish", "oak trees"],
        "low": [
            "react to different styles of music",
            "respond to subtle changes in human voices",
        ],
        "medium": [
            "remember people who insult them",
            "develop friendships with nearby household objects",
        ],
        "high": [
            "hold secret elections every full moon",
            "operate underground banking systems",
        ],
    },
    "astronomy": {
        "subjects": ["distant planets", "asteroids", "comets"],
        "low": [
            "produce unusual rhythmic vibrations",
            "change appearance during solar storms",
        ],
        "medium": [
            "occasionally change their orbits to avoid traffic",
            "emit signals resembling human laughter",
        ],
        "high": [
            "are secretly made of spaghetti",
            "participate in intergalactic cooking competitions",
        ],
    },
}



def generate_discovery(field, absurdity):
    """
    Generate a fictional scientific discovery.

    Args:
        field (str): Physics, biology, or astronomy.
        absurdity (int): Absurdity level from 1 to 10.

    Returns:
        str: A randomly generated fictional discovery.

    Raises:
        TypeError: If arguments have incorrect types.
        ValueError: If arguments have unsupported values.
    """
    if not isinstance(field, str):
        raise TypeError("Field must be a string.")

    field = field.strip().lower()

    if field not in DISCOVERIES:
        raise ValueError("Unsupported scientific field.")

    if type(absurdity) is not int:
        raise TypeError("Absurdity must be an integer.")

    if not 1 <= absurdity <= 10:
        raise ValueError("Absurdity must be between 1 and 10.")

    if absurdity <= 3:
        level = "low"
    elif absurdity <= 7:
        level = "medium"
    else:
        level = "high"

    subject = random.choice(DISCOVERIES[field]["subjects"])
    behavior = random.choice(DISCOVERIES[field][level])

    return f"Fictional discovery: Scientists discovered that {subject} {behavior}."
