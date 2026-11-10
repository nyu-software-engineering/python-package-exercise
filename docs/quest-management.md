# Creating and editing quests

The `quest_manager` module now connects quest creation and editing to the
team's fantasy descriptions and XP calculations. These functions work on an
in-memory list and return a new list. Assign the returned value to keep a change.

```python
from quest_manager import (
    change_quest_duration,
    create_quest,
    get_quest,
    rename_quest,
)

quests = create_quest([], "Study math", 30)
quest_id = quests[-1]["id"]
assert get_quest(quests, quest_id)["xpReward"] == 30

quests = rename_quest(quests, quest_id, "Do laundry")
quests = change_quest_duration(quests, quest_id, 45)
quest = get_quest(quests, quest_id)
assert quest["fantasyDescription"] == "Restore Order to the Kingdom"
assert quest["durationMinutes"] == 45
assert quest["xpReward"] == 45
```

## Public functions

| Function | Behavior |
| --- | --- |
| `create_quest(quests, title, duration_minutes, *, seed=None)` | Append a new pending quest to a copied list, generating a UUID string ID. |
| `rename_quest(quests, quest_id, new_title, *, seed=None)` | Find one pending quest and update its title and fantasy description together. |
| `change_quest_duration(quests, quest_id, duration_minutes)` | Find one pending quest and update its duration and planned XP reward together. |

Creation produces `id`, `title`, `durationMinutes`, `fantasyDescription`,
`status`, `xpReward`, and `completedAt`. It sets `status` to `pending` and
`completedAt` to `None`. The original title formatting is preserved. Each call
creates a separate quest, even when the same title and duration are supplied;
this API does not identify retried submissions.

Creation and title edits call `generate_fantasy_description` and
`rename_pending_quest` from `quest_descriptions`. Pass `seed=7`, for example,
to select a repeatable template. Seeds are not saved in quest records; pass
one again when renaming if repeatable selection is wanted. No seed uses the
default template. Duration validation and reward calculation use
`progression.calculate_xp`, following the 1 planned minute = 1 XP rule.

Only pending quests can be edited. Completed quests are read-only. Edits keep
the ID, status, completion time, unrelated fields, and list order. New lists
contain shallow copies of task dictionaries, consistent with the existing
list/get/delete helpers. Nested custom metadata remains shared; these functions
do not modify it. Input lists are left unchanged on success and failure.

## Errors

- `TypeError`: a collection is not a list, an entry is not a dictionary, a
  title is not a string, a duration is not an integer, or an ID/seed has an
  invalid type. Booleans are not accepted as durations, IDs, or seeds.
- `ValueError`: a title or string ID is blank, a duration is zero/negative,
  the target is not pending, or an edited ID matches multiple records.
- `KeyError`: the requested ID is absent, including when editing an empty list.

IDs supplied for editing can be nonblank strings or integers, matching
`get_quest`. String IDs are matched exactly, without trimming whitespace.
The new UUID is checked against IDs already present in the supplied list.
Creation/storage remain responsible for the overall record schema and existing
data quality.

## Limits and packaging

Creating or changing a planned reward does not award XP, update total XP,
mark a quest complete, or write a database. Completion must later save status
and its XP award atomically through the persistence layer.

The installed package must include the `progression` module. This is supplied
by the teammate's package fix in PR #19; source-only imports are not enough to
validate the installed wheel.

After installing the project with the team's Pipenv setup, run:

```sh
pipenv run python -I examples/quest_management.py
pipenv run python -m pytest -q
```

The example calls all ten current public functions across `quest_manager`,
`quest_descriptions`, and `progression`. Expected output includes
`Updated planned XP: 45` and ends with `Remaining quests: 0`.
