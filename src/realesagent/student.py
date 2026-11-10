import math


def desperation_level(grade, hours_until_deadline, missing_assignments):
    for name, value in (("grade", grade),
                        ("hours_until_deadline", hours_until_deadline)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

    if not 0 <= grade <= 100:
        raise ValueError("grade must be between 0 and 100")
    if type(missing_assignments) is not int:
        raise TypeError("missing_assignments must be an integer")
    if missing_assignments < 0:
        raise ValueError("missing_assignments cannot be negative")

    grade_points = math.ceil((100 - grade) / 20)
    if hours_until_deadline > 48:
        deadline_points = 0
    elif hours_until_deadline > 24:
        deadline_points = 1
    elif hours_until_deadline > 0:
        deadline_points = 2
    else:
        deadline_points = 3

    total = 1 + grade_points + deadline_points

    if missing_assignments > 3:
        total += 3
    else:
        total += missing_assignments

    if total > 10:
        total = 10
    
    return total

def professionalize(truth):
    if not isinstance(truth, str):
        raise TypeError("truth must be a string")
    truth = " ".join(truth.split())
    if not truth:
        raise ValueError("truth cannot be empty")

    explanations = (
        (("overslept", "slept in"),
         "I experienced an unforeseen disruption to my circadian scheduling."),
        (("forgot",),
         "I encountered a temporary interruption in my task retention system."),
        (("procrastinated", "procrastinating"),
         "I extended the preliminary planning phase beyond its intended duration."),
        (("internet", "wifi", "wi-fi"),
         "I experienced an unexpected interruption to my digital connectivity."),
        (("dog ate",),
         "My academic materials underwent an unauthorized canine review."),
    )
    normalized = truth.lower()
    for phrases, explanation in explanations:
        for phrase in phrases:
            if phrase in normalized:
                return explanation

    return (
        f'I wish to formally report the following circumstance: "{truth}". '
        "I respectfully request your consideration while I address this matter."
    )
