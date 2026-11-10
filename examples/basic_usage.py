"""Run every current public function after installing chipotle-quests."""

from quest_descriptions import generate_fantasy_description, rename_pending_quest
from quest_manager import delete_quest, get_quest, list_quests
from progression import award_xp, calculate_level, calculate_xp


def main() -> None:
    title = "Study math"
    duration_minutes = 60

    quests = [
        {
            "id": "q1",
            "title": title,
            "durationMinutes": duration_minutes,
            "fantasyDescription": generate_fantasy_description(title),
            "status": "pending",
            "xpReward": calculate_xp(duration_minutes),
            "completedAt": None,
        }
    ]

    print(f"Original: {title} -> {quests[0]['fantasyDescription']}")
    print("Seeded description:", generate_fantasy_description(title, seed=7))
    print("Quest XP reward:", quests[0]["xpReward"])
    print("Level at 160 total XP:", calculate_level(160))

    progress = award_xp(90, duration_minutes)
    print("Progress after one reward:", progress)

    print("Pending quests:", len(list_quests(quests, status="pending")))

    quest = get_quest(quests, "q1")
    print("Looked up:", quest["id"], quest["title"])

    # Save the returned copy to keep an edit.
    updated = rename_pending_quest(quest, "Clean the kitchen")
    quests = [updated]
    print(f"Renamed: {updated['title']} -> {updated['fantasyDescription']}")
    print("Original copy still says:", quest["title"])

    quests = delete_quest(quests, "q1")
    print("Remaining quests:", len(list_quests(quests)))


if __name__ == "__main__":
    main()