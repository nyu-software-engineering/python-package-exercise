import random


def make_title(activity, outcome):
    """Return a random edit title, or None for invalid inputs."""
    if not isinstance(activity, str) or not isinstance(outcome, str):
        return None

    activity = activity.strip().lower()
    phrases = {
        "win": [
            "ascension confirmed",
            "brutal mog",
            "halo activated",
            "psl went up",
            "chadlite unlocked",
            "mog streak started",
        ],
        "loss": [
            "its over",
            "pure cope",
            "never began",
            "got mogged",
            "brutal failo",
            "psl dropped",
        ],
        "grind": [
            "ascension pending",
            "mogging in progress",
            "softmaxxing arc",
            "halo under construction",
            "psl gains pending",
            "mewing streak",
        ],
    }

    if not activity or outcome not in phrases:
        return None

    phrase = random.choice(phrases[outcome])
    subject = f"{activity}maxxing"
    frames = [
        f"pov {subject} {phrase}",
        f"{subject} update {phrase}",
        f"{phrase} after {subject}",
    ]
    return random.choice(frames)
