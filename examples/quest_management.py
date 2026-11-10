"""Use the creation and editing functions with the team's other modules."""

from progression import calculate_level, calculate_xp
from quest_descriptions import generate_fantasy_description, rename_pending_quest
from quest_manager import (
    change_quest_duration,
    create_quest,
    delete_quest,
    get_quest,
    list_quests,
    rename_quest,
)


def main():
    title = "Study math"
    quests = create_quest([], title, 30)
    quest_id = quests[0]["id"]
    original = get_quest(quests, quest_id)

    print("Description:", generate_fantasy_description(title))
    print("Planned XP:", calculate_xp(30))
    print("Level before completion:", calculate_level(0))
    print("Pending quests:", len(list_quests(quests, "pending")))

    preview = rename_pending_quest(original, "Go swimming", seed=7)
    print("Rename preview:", preview["fantasyDescription"])
    print("Original title:", original["title"])

    quests = rename_quest(quests, quest_id, "Do laundry")
    quests = change_quest_duration(quests, quest_id, 45)
    updated = get_quest(quests, quest_id)
    print("Updated title:", updated["title"])
    print("Updated description:", updated["fantasyDescription"])
    print("Updated planned XP:", updated["xpReward"])

    quests = delete_quest(quests, quest_id)
    print("Remaining quests:", len(list_quests(quests)))


if __name__ == "__main__":
    main()
