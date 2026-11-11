# Saved quest completion

`storage.complete_quest(database_path, quest_id)` completes a saved quest and
adds its reward to saved progress. It uses `progression.award_xp` and
`calculate_level` for the team's XP and level rules.

```python
from quest_manager import create_quest
from storage import complete_quest, initialize_database, insert_quest

initialize_database("quests.db")
quest = create_quest([], "Study math", 60)[0]
insert_quest("quests.db", quest)

result = complete_quest("quests.db", quest["id"])
assert result["quest"]["status"] == "completed"
assert result["totalXP"] == 60
assert result["level"] == 1
assert result["awardedXP"] == 60

retry = complete_quest("quests.db", quest["id"])
assert retry["totalXP"] == 60
assert retry["awardedXP"] == 0
assert retry["quest"]["completedAt"] == result["quest"]["completedAt"]
```

## Saved behavior

- Completion uses the quest's latest saved duration. Each minute is worth 1 XP.
- The quest's status, UTC completion timestamp, and total XP are saved in one
  transaction. A failed save rolls back all three changes.
- Repeating completion preserves the original timestamp and awards 0 XP,
  including after restarting Python. The returned total XP and level describe
  the current saved progress, which may include other completed quests.
- Concurrent completions use SQLite's write lock. Requests for the same quest
  award one reward; requests for different quests retain both rewards.
- Creating, editing, and deleting pending quests do not add earned XP.
- Completed quests stay protected by the existing pending-only edit/delete helpers.

The returned dictionary has `quest`, `totalXP`, `level`, and `awardedXP` fields.
`quest` is a fresh dictionary with the seven standard quest fields. Level is
calculated from total XP; it is not stored separately.

## Errors

`quest_id` must be a nonblank string. Invalid types raise `TypeError`; a blank
ID raises `ValueError`. IDs are matched exactly. An unknown ID raises `KeyError`.
Missing progress or a resulting XP total above SQLite's signed 64-bit integer
limit raises `ValueError`. SQLite errors propagate to the caller.

The database must already exist and be initialized. Completion does not create
a missing database. Use the same file path accepted by the other storage helpers.

## Example and tests

After installing the package, run the standalone example from the source archive:

```sh
python examples/quest_completion.py
python -m pytest -q tests/test_quest_completion.py
```

The example uses a temporary database. Tests cover retries from another Python
process, concurrent completions, changed durations, level boundaries, failed
saves, integer overflow, and completed-quest protection.

This change supplies the Python storage function. Completion and progress HTTP
routes and their browser controls are separate integration work.
