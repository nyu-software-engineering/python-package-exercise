def calculate_xp(duration_minutes: int) -> int:
    """Earn 1 XP per planned minute. Duration must be a positive integer."""
    if isinstance(duration_minutes, bool) or not isinstance(duration_minutes, int):
        raise TypeError("duration_minutes must be an integer")
    if duration_minutes <= 0:
        raise ValueError("duration_minutes must be greater than zero")
    return duration_minutes


def calculate_level(total_xp: int) -> int:
    """Start at level 1 and gain a level every 100 XP."""
    if isinstance(total_xp, bool) or not isinstance(total_xp, int):
        raise TypeError("total_xp must be an integer")
    if total_xp < 0:
        raise ValueError("total_xp must not be negative")
    return 1 + total_xp // 100
