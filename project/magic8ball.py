"""
Magic 8 Ball: ask a question, pick a number, get your fate.

Functions, in order:
1. get_question     - validate the user's question
2. select_category  - turn a number 0-8 into Positive / Non-Committal / Negative
3. get_response     - pick a random answer from that category
4. custom_answer    - let the user add their own answer to a category
"""

import random


# 1. Get question
def get_question(question):
    """
    Accept and validate a user's Magic 8 Ball question.
    """
    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    return question


# 2. Get random category (pick a number 0-8)
def select_category(number):
    numbers = list(range(9))
    random.shuffle(numbers)

    positive = numbers[0:3]
    non_committal = numbers[3:6]
    negative = numbers[6:9]

    if type(number) != int or number < 0 or number > 8:
        return "Invalid number"

    if number in positive:
        return "Positive"
    elif number in non_committal:
        return "Non-Committal"
    elif number in negative:
        return "Negative"
    else:
        return "Invalid number"


# 3. Get random response in the category / give response
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


# 4. Take in custom answer (dictionary)
def custom_answer(answer, category):
    responses = {
        "positive": [],
        "non-committal": [],
        "negative": []
    }
    
    category = category.lower()
    if category in responses:
        responses[category].append(answer)
        print("Answer added!")
    else:
        print("Invalid category")
    return responses
