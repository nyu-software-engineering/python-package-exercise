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
the `quest_descriptions`, `quest_manager`, and `progression` modules. The package has
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

| Import from | Function | Purpose |
| --- | --- | --- |
| `quest_descriptions` | `generate_fantasy_description(title, *, seed=None)` | Describe a nonblank title; an integer seed selects a repeatable template. |
| `quest_descriptions` | `rename_pending_quest(quest, new_title, *, seed=None)` | Return a pending quest copy with its title and description updated. |
| `quest_manager` | `list_quests(quests, status=None)` | Return quest copies, optionally filtering by `pending` or `completed`. |
| `quest_manager` | `get_quest(quests, quest_id)` | Return a quest copy by ID; raise `KeyError` if it is missing. |
| `quest_manager` | `delete_quest(quests, quest_id)` | Return a new list with the specified pending quest removed. |
| `progression` | `calculate_xp(duration_minutes)` | Return 1 XP per positive integer minute. |
| `progression` | `calculate_level(total_xp)` | Calculate a level from nonnegative integer total XP: `1 + total_xp // 100`. |

For example, `from quest_manager import list_quests` imports the listing function.
The [usage example](examples/basic_usage.py) calls all seven functions: generate a
description, calculate XP and a level, filter and look up a quest, rename it, and
delete it. It keeps data in memory; persistence and awarding XP on completion
are separate integration work. More XP details are in the
[progression notes](docs/progression.md).
Expected output includes `Pending quests: 1` and ends with `Remaining quests: 0`.
Extend the example and module list in `pyproject.toml` as public functions and
modules are added. More title-editing details are in the
[integration notes](docs/quest-description-integration.md).
