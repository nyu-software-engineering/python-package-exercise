"""Complete a saved quest without awarding the same reward twice."""

from pathlib import Path
from tempfile import TemporaryDirectory

from quest_manager import create_quest
from storage import complete_quest, initialize_database, insert_quest, load_progress


def main():
    with TemporaryDirectory() as folder:
        database = Path(folder) / "quests.db"
        initialize_database(database)
        quest = create_quest([], "Study math", 60)[0]
        insert_quest(database, quest)

        first = complete_quest(database, quest["id"])
        retry = complete_quest(database, quest["id"])

        assert first["awardedXP"] == 60
        assert retry["awardedXP"] == 0
        assert retry["quest"]["completedAt"] == first["quest"]["completedAt"]
        assert load_progress(database) == {"totalXP": 60}
        print("Status:", first["quest"]["status"])
        print("First reward:", first["awardedXP"])
        print("Reward on retry:", retry["awardedXP"])
        print("Saved XP:", retry["totalXP"])
        print("Level:", retry["level"])


if __name__ == "__main__":
    main()
