
import random


def make_stat_card(activity, level):
    """
    Create a fictional stat card for an everyday activity.
    Scores depend on the selected level from 1 to 10.
    """

    if not isinstance(activity, str):
        raise TypeError("Activity must be a string.")

    if activity.strip() == "":
        raise ValueError("Activity cannot be empty.")

    if type(level) is not int:
        raise TypeError("Level must be an integer.")

    if level < 1 or level > 10:
        raise ValueError("Level must be between 1 and 10.")

    if activity.lower().strip() == "studying":
        labels = ["Focus", "Studymaxxing", "Exam Aura"]
    elif activity.lower().strip() == "gym":
        labels = ["Strength", "Gymmaxxing", "Physique Aura"]
    else:
        labels = ["Effort", "Maxxing", "Aura"]

    minimum_score = (level - 1) * 10 + 1
    maximum_score = level * 10

    card = "ASCEND STAT CARD\n"
    card += "Activity: " + activity.strip() + "\n"
    card += "Level: " + str(level) + "\n\n"

    for label in labels:
        score = random.randint(minimum_score, maximum_score)
        card += label + ": " + str(score) + "\n"

    return card
