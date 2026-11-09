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


def get_quest(quests, quest_id):
    """Return a quest copy by ID, or raise KeyError if it does not exist."""
    if isinstance(quest_id, bool) or not isinstance(quest_id, (str, int)):
        raise TypeError("quest_id must be a string or an integer")

    if isinstance(quest_id, str) and not quest_id.strip():
        raise ValueError("quest_id must not be blank")

    for quest in list_quests(quests):
        if quest.get("id") == quest_id:
            return quest

    raise KeyError(f"quest not found: {quest_id}")
