def list_quests(quests, status=None):
    """Return quest copies, optionally filtered by pending or completed status."""
    if not isinstance(quests, list):
        raise TypeError("quests must be a list")

    if status not in (None, "pending", "completed"):
        raise ValueError("status must be pending, completed, or None")

    result = []

    for quest in quests:
        if not isinstance(quest, dict):
            raise TypeError("each quest must be a dictionary")

        if status is None or quest.get("status") == status:
            result.append(quest.copy())

    return result
