from uuid import uuid4

from progression import calculate_xp
from quest_descriptions import generate_fantasy_description, rename_pending_quest


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


def delete_quest(quests, quest_id):
    """Return a new list without the pending quest, leaving the input unchanged."""
    quest = get_quest(quests, quest_id)
    if quest.get("status") != "pending":
        raise ValueError("only pending quests can be deleted")

    result = []
    for item in list_quests(quests):
        if item.get("id") != quest_id:
            result.append(item)

    if len(result) != len(quests) - 1:
        raise ValueError("quest IDs must be unique")

    return result


def create_quest(quests, title, duration_minutes, *, seed=None, custom_templates=None):
    """Return a new pending quest list; optional templates customize its description.

    No XP is awarded. Templates and seed are forwarded to the description
    generator, validated there, and not stored in the quest.
    """
    result = list_quests(quests)
    description = generate_fantasy_description(
        title, seed=seed, custom_templates=custom_templates
    )
    reward = calculate_xp(duration_minutes)

    quest_id = uuid4().hex
    while any(quest.get("id") == quest_id for quest in result):
        quest_id = uuid4().hex

    result.append({
        "id": quest_id,
        "title": title,
        "durationMinutes": duration_minutes,
        "fantasyDescription": description,
        "status": "pending",
        "xpReward": reward,
        "completedAt": None,
    })
    return result


def rename_quest(quests, quest_id, new_title, *, seed=None, custom_templates=None):
    """Rename one pending quest and regenerate its description.

    Pass custom_templates again to retain a custom theme; omitted categories
    use defaults. Validation failures leave the input collection unchanged.
    """
    quest = get_quest(quests, quest_id)
    updated = rename_pending_quest(
        quest, new_title, seed=seed, custom_templates=custom_templates
    )
    return _replace_quest(quests, quest_id, updated)


def change_quest_duration(quests, quest_id, duration_minutes):
    """Update one pending quest's duration and planned XP reward together."""
    quest = get_quest(quests, quest_id)
    if quest.get("status") != "pending":
        raise ValueError("only pending quests can be edited")

    reward = calculate_xp(duration_minutes)
    quest["durationMinutes"] = duration_minutes
    quest["xpReward"] = reward
    return _replace_quest(quests, quest_id, quest)


def _replace_quest(quests, quest_id, updated):
    result = list_quests(quests)
    matches = [
        index for index, quest in enumerate(result) if quest.get("id") == quest_id
    ]
    if len(matches) != 1:
        raise ValueError("quest IDs must be unique")

    result[matches[0]] = updated
    return result
