import random

RESPONSES = {
    "positive": [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
    ],
    "non-committal": [
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
    ],
    "negative": [
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful",
    ],
}


def normalize_category(category):
    """Turn 'Positive', 'Non-Committal', 'non committal', etc. into a RESPONSES key."""
    if not isinstance(category, str):
        raise TypeError("category must be a string")
    key = category.strip().lower().replace("_", "-").replace(" ", "-")
    if key == "noncommittal":
        key = "non-committal"
    if key not in RESPONSES:
        raise ValueError(
            f"Unknown category '{category}'. Use positive, non-committal, or negative."
        )
    return key


def get_response(category, custom_answers=None, rng=None):
    """
    Return a random Magic 8 Ball answer from the given category.

    category: "positive", "non-committal", or "negative" (any capitalization,
              so the output of select_category() works directly).
    custom_answers: optional dict like the one custom_answer() returns,
              e.g. {"positive": ["Heck yes"]}. Its answers are added to the pool.
    rng: optional random.Random instance, mainly so tests can be repeatable.
    """
    key = normalize_category(category)
    pool = list(RESPONSES[key])

    if custom_answers is not None:
        if not isinstance(custom_answers, dict):
            raise TypeError("custom_answers must be a dict")
        for custom_key, answers in custom_answers.items():
            if normalize_category(custom_key) == key:
                pool.extend(answers)

    return (rng or random).choice(pool)


if __name__ == "__main__":
    for cat in RESPONSES:
        print(f"{cat}: {get_response(cat)}")
