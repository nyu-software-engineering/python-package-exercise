[![Test and build](https://github.com/software-students-fall2026/python-package-exercise-Chipotle/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/software-students-fall2026/python-package-exercise-Chipotle/actions/workflows/ci.yml)

# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.


Team Roles:


**Ali — Frontend Integration & Documentation**

**Ownership and Deliverables:** Maintain and improve the RPG Quest Planner frontend, assist with frontend-backend integration and Docker configuration, and develop comprehensive README documentation. Document the project overview, architecture, installation procedures, environment variables, Docker setup, testing commands, and team contributions. Coordinate with backend and infrastructure developers to ensure all setup instructions are accurate and reproducible.

**Test Responsibilities:** Verify frontend functionality, API integration, and error handling. Independently follow the README instructions to confirm that the application can be configured, built, and launched successfully. Validate documentation accuracy and ensure all referenced commands and configuration examples are functional.

## Development setup

Use Python 3.11 or newer. Run these commands from the repository root.
Pipenv is installed in `.tools` and project dependencies in `.venv`.

On macOS/Linux:

```sh
python3 -m venv .tools
.tools/bin/python -m pip install pipenv==2026.11.0
export PIPENV_VENV_IN_PROJECT=1
.tools/bin/pipenv --python "$(command -v python3)"
.tools/bin/pipenv sync --dev
.tools/bin/pipenv run test
```

On Windows PowerShell (`py -3` must select Python 3.11 or newer):

```powershell
py -3 -m venv .tools
.\.tools\Scripts\python.exe -m pip install pipenv==2026.11.0
$env:PIPENV_VENV_IN_PROJECT = "1"
.\.tools\Scripts\pipenv.exe --python (py -3 -c "import sys; print(sys.executable)")
.\.tools\Scripts\pipenv.exe sync --dev
.\.tools\Scripts\pipenv.exe run test
```

`sync --dev` installs the development versions recorded in `Pipfile.lock`.
The `test` script runs the existing pytest tests. `colorama` is explicitly
included so a lock generated on macOS also covers pytest's Windows dependency.
After changing `Pipfile`, run `pipenv lock` and commit both dependency files.

## Build and use the Python package

The working distribution name is `chipotle-quests` (version `0.1.0`). It contains
the `quest_descriptions`, `quest_manager`, `progression`, and `storage` modules. The package has
not been published to PyPI; confirm the distribution name before publishing.

Pipenv now installs the project in editable mode, so source edits are available
immediately. From the repository root on macOS/Linux:

```sh
export PIPENV_VENV_IN_PROJECT=1
.tools/bin/pipenv sync --dev
.tools/bin/pipenv run test
.tools/bin/pipenv run build
.tools/bin/pipenv run python examples/basic_usage.py
```

On Windows PowerShell:

```powershell
$env:PIPENV_VENV_IN_PROJECT = "1"
.\.tools\Scripts\pipenv.exe sync --dev
.\.tools\Scripts\pipenv.exe run test
.\.tools\Scripts\pipenv.exe run build
.\.tools\Scripts\pipenv.exe run python examples/basic_usage.py
```

The build command uses `python -m build` to create
`dist/chipotle_quests-0.1.0.tar.gz` (source distribution) and
`dist/chipotle_quests-0.1.0-py3-none-any.whl` (installable wheel).
`MANIFEST.in` includes the usage example and Pipenv files in the source distribution.

To try the built wheel, replace the editable installation using your platform's
Pipenv executable (`pipenv` below means the executable used above):

```sh
pipenv run python -m pip install --force-reinstall --no-deps dist/chipotle_quests-0.1.0-py3-none-any.whl
pipenv run python -I examples/basic_usage.py
```

Run `pipenv sync --dev` again to return to editable development.

### Public functions

| `quest_validation` | `validate_quest_input(title, duration_minutes)` | Return the trimmed title and validated whole-minute duration. Raise `ValueError` for a blank title or an invalid duration. |
| Import from | Function | Purpose |
| --- | --- | --- |
| `quest_descriptions` | `generate_fantasy_description(title, *, seed=None, custom_templates=None)` | Describe a nonblank title; an integer seed selects a repeatable template, with optional category overrides. |
| `quest_descriptions` | `rename_pending_quest(quest, new_title, *, seed=None, custom_templates=None)` | Return a pending quest copy with its title and description updated. |
| `quest_manager` | `create_quest(quests, title, duration_minutes, *, seed=None, custom_templates=None)` | Return a new list containing a new pending quest with a UUID string ID. |
| `quest_manager` | `list_quests(quests, status=None)` | Return quest copies, optionally filtering by `pending` or `completed`. |
| `quest_manager` | `get_quest(quests, quest_id)` | Return a quest copy by ID; raise `KeyError` if it is missing. |
| `quest_manager` | `delete_quest(quests, quest_id)` | Return a new list with the specified pending quest removed. |
| `quest_manager` | `rename_quest(quests, quest_id, new_title, *, seed=None, custom_templates=None)` | Rename a pending quest by ID and regenerate its description. |
| `quest_manager` | `change_quest_duration(quests, quest_id, duration_minutes)` | Update a pending quest's duration and planned XP reward together. |
| `progression` | `calculate_xp(duration_minutes)` | Return 1 XP per positive integer minute. |
| `progression` | `calculate_level(total_xp)` | Calculate a level from nonnegative integer total XP: `1 + total_xp // 100`. |
| `progression` | `award_xp(total_xp, duration_minutes)` | Calculate total XP and level after one reward. |
| `storage` | `initialize_database(database_path)` | Create SQLite tables and initialize progress without overwriting existing data. |
| `storage` | `insert_quest(database_path, quest)` | Commit one new pending quest without changing earned XP; duplicate IDs raise `sqlite3.IntegrityError`. |
| `storage` | `load_quests(database_path, status=None)` | Read quest dictionaries in insertion order, optionally filtering by `pending` or `completed`. |
| `storage` | `load_progress(database_path)` | Read `{"totalXP": saved_integer}`; derive the level with `calculate_level`. |

For example, `from quest_manager import list_quests` imports the listing function.
The [usage example](examples/basic_usage.py) calls all fifteen public functions:
initialize a temporary database, create/save/reload a quest, read saved progress,
filter/look up/edit/delete quests, generate descriptions, and calculate XP, a
level, and updated progress. After the storage demonstration, edits/deletes and
reward calculations use in-memory helpers. The temporary database is removed
when the storage demonstration finishes. More XP details are in the
[progression notes](docs/progression.md).
Expected output includes `Pending quests: 1` and ends with `Remaining quests: 0`.
Extend the example and module list in `pyproject.toml` as public functions and
modules are added. More title-editing details are in the
[integration notes](docs/quest-description-integration.md).

## Database initialization

After syncing the editable installation with `pipenv sync --dev`, initialize a
local database using Python's standard-library SQLite support:

```python
from storage import initialize_database

initialize_database("quests.db")
```

This creates the file if needed, plus two tables:

- `quests`: `id` (text), `title`, `durationMinutes`, `fantasyDescription`,
  `status`, `xpReward`, and nullable `completedAt`, matching existing quest helpers.
- `progress`: one local-user row (`id = 1`) with `totalXP = 0` initially.
  Use `calculate_level(total_xp)` to derive the level rather than storing it twice.

Repeated initialization preserves existing tasks and XP. Schema creation and
initial progress are committed together, and the connection is closed before
the function returns. Basic schema constraints enforce positive integer minutes,
matching XP rewards, supported statuses, and nonnegative integer total XP.

Pass a string or `pathlib.Path` pointing to a file in an existing directory.
Invalid path types raise `TypeError`; blank names, `:memory:`, and SQLite URIs
raise `ValueError`. File-access and database errors propagate as SQLite errors.
Existing table definitions are not migrated by this initializer.

Local database files and SQLite transaction files are ignored by Git.

### Save and reload a new quest

```python
from progression import calculate_level
from quest_manager import create_quest
from storage import initialize_database, insert_quest, load_progress, load_quests

database_path = "quests.db"
initialize_database(database_path)
quest = create_quest([], "Study math", 60, seed=7)[0]
insert_quest(database_path, quest)

pending = load_quests(database_path, status="pending")
assert any(saved == quest for saved in pending)
progress = load_progress(database_path)
print(progress["totalXP"], calculate_level(progress["totalXP"]))
```

Every helper closes its connection. Committed tasks and XP remain available
after restarting Python and calling the readers again. On a fresh database,
creating a pending quest leaves XP at 0 and the level at 1.

Initialize the database before using these helpers. They open existing files
only, so a misspelled path raises `sqlite3.OperationalError` instead of creating
another empty database. Missing tables and other SQLite errors propagate.
`load_progress` raises `ValueError` if the initial progress row is missing;
it does not reset XP or silently create a row. Readers use read-only connections.

`insert_quest` accepts a dictionary with exactly the seven standard quest fields.
IDs, titles, and descriptions must be nonblank strings. Duration and reward must
be integers (not booleans), duration must be positive and fit SQLite's signed
64-bit range, and reward must equal duration. Only `pending` quests with
`completedAt=None` can be inserted. Invalid field types raise `TypeError`;
missing/extra fields or invalid values raise `ValueError`. Extra metadata is
rejected rather than discarded. Titles and descriptions are stored unchanged.

Insertion returns `None` after committing. It never replaces existing IDs,
clears other tasks, or awards XP. Duplicate IDs raise `sqlite3.IntegrityError`;
a failed insert leaves existing tasks and progress unchanged. `load_quests`
returns independent dictionaries, or `[]` if there are no matches. Its filter
must be `None`, `pending`, or `completed`; other values raise `ValueError`.

Editing/deleting stored quests and completion are later integration work. A
completion operation must check the saved status and commit both the status
change and XP award in one transaction, including retry/concurrency protection.
Do not implement completion using separately committed task and XP writes.

## Automated checks

The [Test and build workflow](.github/workflows/ci.yml) runs on every pull request,
including PRs targeting feature branches, and on pushes to `main` or `master`.
It can also be run manually from GitHub Actions once available on the default branch.
Each job uses Python 3.13 or 3.14 to install locked dependencies, run pytest,
and build the source distribution and wheel. It then reruns pytest and the usage
example from a fresh wheel installation outside the source checkout, catching
missing packaged modules as well as source failures. A failed step fails that job.
The badge at the top shows the latest `main` push result. The instructor's
separate event-logging workflow is unchanged.
