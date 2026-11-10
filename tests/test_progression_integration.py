import pytest

from progression import award_xp
from quest_manager import change_quest_duration, create_quest, get_quest


@pytest.mark.parametrize(
    "new_duration, starting_xp, expected",
    [
        (10, 90, {"totalXP": 100, "level": 2}),
        (90, 0, {"totalXP": 90, "level": 1}),
        (250, 90, {"totalXP": 340, "level": 4}),
    ],
)
def test_award_uses_edited_duration(new_duration, starting_xp, expected):
    quests = create_quest([], "Study math", 60)
    quest_id = quests[0]["id"]

    updated = change_quest_duration(quests, quest_id, new_duration)
    quest = get_quest(updated, quest_id)
    progress = award_xp(starting_xp, quest["durationMinutes"])

    assert progress == expected
    assert progress["totalXP"] - starting_xp == quest["xpReward"]
    assert quests[0]["durationMinutes"] == 60