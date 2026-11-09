# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

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
