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
the form's existing `quest:created` event. The creation success message also
shows the saved description and planned XP, following Ali's latest form update.

## Editing, deleting, and completing

Open a pending quest's details to use these controls:

- **Edit quest** opens the saved title and duration in an inline form. Save
  changes after entering a nonblank title and positive whole minutes. Only
  changed fields are sent; an unchanged form makes no request. Cancel edit
  closes the form. Failed saves keep the entered values for retry.
- **Delete quest** opens a confirmation. Confirm delete removes the pending
  quest, clears its detail, and refreshes the list. Cancel delete makes no change.
- **Complete quest** saves completion and awards the stored planned XP once.
  Save or cancel an open edit first. The detail becomes read-only and shows
  the saved completion time; current XP and level refresh from the server.
  Under the pending filter, the completed task leaves the list while its
  completed detail remains visible.

Completed quests have no editing, deletion, or completion controls. Mutations
use the existing session token; the server still enforces status and validates
input. Viewing, editing, and deleting do not award XP. Completion displays the
server's awardedXP; it does not add a reward in browser code. If a completion
response is lost, retrying can confirm the saved result with no extra XP.

While a change is saving, other page controls wait and repeated clicks do not
send another write. If creation is already saving, wait for it before changing
another quest. A conflict asks you to refresh before writing again. An expired
session asks you to reload the page; a missing quest asks you to refresh the
list. A failed refresh after a confirmed write has its own read-error message
and does not turn a successful save into a reported write failure.

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
creation refresh, editing/deletion/completion, conflicts, retry and duplicate
submission behavior, untrusted text, and narrow layout. Browser tests use mocked
HTTP responses; the API suites test real SQLite persistence separately.
The Flask demo is source-only, so CI runs these tests in the source phase and
excludes them from its installed-library phase.

