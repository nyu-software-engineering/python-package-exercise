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
