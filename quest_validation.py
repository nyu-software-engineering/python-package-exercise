MAX_SAFE_MINUTES = 2**53 - 1


def validate_quest_input(title, duration_minutes):
    """Return a cleaned quest title and validated duration."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Enter a quest title.")

    if (
        type(duration_minutes) is not int
        or not 1 <= duration_minutes <= MAX_SAFE_MINUTES
    ):
        raise ValueError("Enter a positive whole number of minutes.")

    return title.strip(), duration_minutes