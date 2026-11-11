# XP and leveling

Each planned minute is worth 1 XP. Users start at level 1 with 0 XP.
Every 100 total XP increases the level by 1.

## Usage

```python
from progression import calculate_xp, calculate_level

reward = calculate_xp(60)  # 60 XP
level = calculate_level(160)  # Level 2
```

## Applying a reward

Use `award_xp(total_xp, duration_minutes)` to calculate the updated XP total
and level after one reward.

```python
from progression import award_xp

progress = award_xp(90, 60)
assert progress == {"totalXP": 150, "level": 2}
```

For the next reward, pass the updated `totalXP` as the starting total.

## Input rules

- Duration must be a positive integer.
- Total XP must be a nonnegative integer.
- Booleans, floats, strings, and `None` raise `TypeError`.
- Zero or negative durations raise `ValueError`.
- Negative total XP raises `ValueError`.

## Completion integration

Store the calculated reward as the quest's `xpReward`.
Persist `totalXP` and calculate the level from that total.

Creating or editing a pending quest changes its planned reward without
adding earned XP. Completion must use the quest's latest stored duration.

`award_xp` only calculates values. It does not receive a quest ID or check
quest status, and each call adds another reward. The completion code must
check whether the quest is already completed before awarding XP.

Save the completed status, completion timestamp, and updated total XP in
one transaction. If saving fails, all of those changes must roll back.
Concurrent requests for the same quest must award XP only once.

`storage.complete_quest(database_path, quest_id)` now handles this saved
completion flow using `award_xp` and `calculate_level`. It returns the completed
quest, current `totalXP` and `level`, and `awardedXP` (0 on a retry).
See [saved quest completion](quest-completion.md) for usage and error rules.

## Completion acceptance checks

These storage acceptance checks are covered by `tests/test_quest_completion.py`.
They are not implemented by the calculation helper alone. Completion and
progress HTTP routes are covered by `tests/test_quest_completion_api.py`;
browser controls still need separate integration checks.

Start each independent scenario with 90 total XP and a pending quest
worth 60 XP, with `completedAt` set to `None`.

| Scenario | Expected saved result |
| --- | --- |
| Complete the quest once | Status is `completed`, a completion timestamp is saved, and total XP is 150 at level 2. |
| Retry completion of the same quest | Total XP stays at 150 and the original completion timestamp is preserved. |
| Reload and retry the completed quest | The saved status still prevents another reward; total XP stays at 150. |
| Send two completion requests concurrently | Only one 60 XP reward is saved; total XP is 150. |
| Fail while saving completion | The quest stays pending, its timestamp stays `None`, and total XP stays at 90. |
| Retry after the failed save | A successful retry completes the quest and saves total XP of 150. |
| After the first quest, complete a different quest worth 50 XP | Total XP becomes 200 at level 3. |

Check saved values through a new database connection after each operation.
A successful response alone does not prove that progress was persisted.

## Testing

From the repository root:

```sh
pipenv install --dev
pipenv run python -m pytest -q
```

