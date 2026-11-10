"""Run every current public function after installing chipotle-quests."""

from pathlib import Path
from tempfile import TemporaryDirectory
from quest_validation import validate_quest_input
from quest_descriptions import generate_fantasy_description, rename_pending_quest
from quest_manager import (
    change_quest_duration, create_quest, delete_quest, get_quest, list_quests,
    rename_quest,
)
from progression import award_xp, calculate_level, calculate_xp
from storage import initialize_database


def main() -> None:
    # Use a temporary file so this demonstration leaves no local database behind.
    with TemporaryDirectory() as directory:
        initialize_database(Path(directory) / "quests.db")
        print("Database initialized.")

    title, duration_minutes = validate_quest_input("  Study math  ", 60)
    quests = create_quest([], title, duration_minutes)
    quest_id = quests[0]["id"]

    print(f"Original: {title} -> {quests[0]['fantasyDescription']}")
    print("Seeded description:", generate_fantasy_description(title, seed=7))
    print("Quest XP reward:", calculate_xp(duration_minutes))
    print("Level at 160 total XP:", calculate_level(160))

    progress = award_xp(90, duration_minutes)
    print("Progress after one reward:", progress)

    print("Pending quests:", len(list_quests(quests, status="pending")))

    quest = get_quest(quests, quest_id)
    print("Looked up:", quest["id"], quest["title"])

    # Save the returned copy to keep an edit.
    updated = rename_pending_quest(quest, "Clean the kitchen")
    quests = [updated]
    print(f"Renamed: {updated['title']} -> {updated['fantasyDescription']}")
    print("Original copy still says:", quest["title"])

    quests = rename_quest(quests, quest_id, "Go swimming")
    quests = change_quest_duration(quests, quest_id, 45)
    print("Updated planned XP:", get_quest(quests, quest_id)["xpReward"])

    quests = delete_quest(quests, quest_id)
    print("Remaining quests:", len(list_quests(quests)))


if __name__ == "__main__":
    main()
