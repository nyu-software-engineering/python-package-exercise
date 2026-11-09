"""Run every current public function after installing chipotle-quests."""

from quest_descriptions import generate_fantasy_description, rename_pending_quest
from quest_manager import delete_quest, get_quest, list_quests


def main() -> None:
    title = "Study math"
    quests = [
        {
            "id": "q1",
            "title": title,
            "durationMinutes": 60,
            "fantasyDescription": generate_fantasy_description(title),
            "status": "pending",
            "xpReward": 60,
            "completedAt": None,
        }
    ]
    print(f"Original: {title} -> {quests[0]['fantasyDescription']}")
    print("Seeded description:", generate_fantasy_description(title, seed=7))
    print("Pending quests:", len(list_quests(quests, status="pending")))

    quest = get_quest(quests, "q1")
    print("Looked up:", quest["id"], quest["title"])

    # These helpers return copies; save the returned value to keep an edit.
    updated = rename_pending_quest(quest, "Clean the kitchen")
    quests = [updated]
    print(f"Renamed: {updated['title']} -> {updated['fantasyDescription']}")
    print("Original copy still says:", quest["title"])

    quests = delete_quest(quests, "q1")
    print("Remaining quests:", len(list_quests(quests)))


if __name__ == "__main__":
    main()
