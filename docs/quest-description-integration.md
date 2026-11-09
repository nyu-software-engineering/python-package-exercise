# Updating quest titles and fantasy descriptions

For a new quest, call `generate_fantasy_description(title, seed=7)` and store
its return value as `fantasyDescription` alongside the original `title`.

For edits, call `rename_pending_quest` so the title and description change
together. This helper accepts a quest dictionary; the caller is responsible
for looking up the quest and persisting the returned copy.

```python
from quest_descriptions import rename_pending_quest

original = {
    "id": "q1",
    "title": "Study math",
    "fantasyDescription": "Decipher an Ancient Scroll",
    "status": "pending",
    "durationMinutes": 30,
    "xpReward": 30,
    "completedAt": None,
}
updated = rename_pending_quest(original, "Go swimming")
assert updated["fantasyDescription"] == "Train for the Royal Tournament"
assert original["title"] == "Study math"  # Input is unchanged.

# Optional seeds produce repeatable template selection for all three categories.
seeded = rename_pending_quest(original, "Do laundry", seed=7)
assert seeded == rename_pending_quest(original, "Do laundry", seed=7)
```

- Only quests whose `status` is exactly `pending` can be renamed.
- The title must be a nonblank string. Its original formatting is preserved.
- `seed` accepts an integer or `None`; booleans are rejected. Pass the seed on
  each edit; it is not stored automatically. No seed means the default template.
- Other fields, including ID, XP, duration, and completion time, are preserved.
- The result is a **shallow copy**, matching `list_quests`. Nested custom metadata
  is shared; this helper does not modify it.
- Invalid input raises `TypeError` or `ValueError` before any data changes. Only
  persist the returned dictionary after a successful call. This helper itself
  does not perform database writes or handle concurrent updates.
- Matching priority remains study, exercise, then chores. Unknown titles use
  the generic fallback. English keywords match whole words, ignoring case.

Run the tests from the repository root with `python -m pytest -q` in an
environment with pytest installed.
