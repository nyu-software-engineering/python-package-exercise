# Saved quest page

Start the Flask demo from the repository:

```sh
pipenv sync --dev
pipenv run python app.py
```

Open `http://127.0.0.1:8000/`. The page includes the original creation form and
adds the saved quest list, details, and current XP and level.

## Viewing saved data

- The page loads all saved quests and progress on opening.
- Use **Show quests** to select all, pending, or completed quests.
- **View details** fetches the selected quest's latest saved data. It shows
  the original title, fantasy description, duration, status, planned reward,
  completion time, and ID. Completion time is shown in the browser's local time.
- **Refresh quests** reloads the current filter and progress. Failed refreshes
  keep previously displayed data with an error message; refresh again to retry.
  Detail buttons wait until the list refresh finishes, then become available
  again even if the refresh failed.
- Creating a quest refreshes the saved list without changing the selected
  filter. A new pending quest will not appear in the completed filter.
- Progress is read from the saved total XP; viewing or filtering awards no XP.

The existing `quest_form.html` and `quest_form.js` still handle creation and
its validation. `planner.html` includes that form; `quest_list.js` listens for
the form's existing `quest:created` event. The new script uses only GET requests.
Editing, deletion, and completion controls will be added in the next UI step.

## Loading and errors

Lists and details have loading, empty, and retry messages. If a quest has been
deleted, its detail request reports that it was not found. Older responses do
not replace a newer filter, detail selection, or progress total. Task titles
and descriptions are inserted as text, so saved markup is not executed.

The layout stacks on narrow screens. Controls have visible labels and focus
indicators; dynamic feedback uses live regions. Opening details moves keyboard
focus to the detail heading. No external fonts or JavaScript packages are
required by the page.

## Tests

```sh
pipenv run python -m pytest tests/test_quest_planner.py -q
pipenv run python -m playwright install chromium
pipenv run python -m pytest tests/test_quest_list_ui.py tests/test_quest_form.py -q
```

Template tests check the rendered page, assets, and the original creation token.
The new browser tests check list/filter/detail behavior, empty/error/retry states,
creation refresh, untrusted text, and narrow layout. Browser tests use mocked
HTTP responses; the API suites test real SQLite persistence separately.
The Flask demo is source-only, so CI runs these tests in the source phase and
excludes them from its installed-library phase.
