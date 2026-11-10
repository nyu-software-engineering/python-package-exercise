# terminal-pet-respin

[![build-test](https://github.com/software-students-fall2026/python-package-exercise-respin/actions/workflows/build-test.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-respin/actions/workflows/build-test.yml)


A tiny pet python that lives in your terminal. It starts as an egg, and every
terminal command you run helps it grow: from egg, to cracking egg, to hatchling,
to young python, and finally to a full coiled python.



**PyPI:** [terminal-pet-respin](https://pypi.org/project/terminal-pet-respin/)

## Installation

Install the package from PyPI with pip:

```bash
pip install terminal-pet-respin
```

Then import the functions in your own code:

```python
from terminal_pet_respin import create_egg, add_commands, get_stage, draw_pet

pet = create_egg("Monty", hatch_at=10)
add_commands(pet, 12)
print(draw_pet(pet["stage"]))
```

## Functions


### `create_egg(name, hatch_at=50)`

Creates a new pet egg.

- `name`: the pet's name. Leading and trailing spaces are removed.
- `hatch_at`: how many commands it takes to hatch. Must be a positive integer.

```python
from terminal_pet_respin import create_egg

create_egg("Monty")
# {"name": "Monty", "hatch_at": 50, "commands_run": 0, "stage": "egg"}
```

Raises `TypeError` if `name` isn't a string or `hatch_at` isn't an integer, and
`ValueError` if `name` is empty or `hatch_at` is zero or negative.

### `get_stage(commands_run, hatch_at)`

Works out the growth stage from the numbers alone.

| `commands_run` (with `hatch_at=50`) | Stage |
|---|---|
| 0–24 | `"egg"` |
| 25–49 | `"cracking"` |
| 50–99 | `"hatchling"` |
| 100–199 | `"young python"` |
| 200+ | `"full python"` |

```python
from terminal_pet_respin import get_stage

get_stage(0, 50)     # "egg"
get_stage(60, 50)    # "hatchling"
```

Raises `TypeError` for non-integer arguments, and `ValueError` if
`commands_run` is negative or `hatch_at` is zero or negative.

### `draw_pet(stage)`

Returns ASCII art of the pet at the given stage, as a string.

```python
from terminal_pet_respin import draw_pet

print(draw_pet("hatchling"))
```

```
     .---.
    ( O O )
     \   /~
  \/\/   \/\/
   \        /
    '------'
```

Raises `TypeError` if `stage` isn't a string, and `ValueError` if it isn't one
of the five stage names.

### `add_commands(pet, count=1)`

Records that `count` more terminal commands were run, then updates the pet's
stage. The pet is changed in place and also returned.

- `pet`: a pet dictionary made by `create_egg`.
- `count`: how many commands to add. Must be a positive integer.

```python
from terminal_pet_respin import add_commands, create_egg

pet = create_egg("Monty", hatch_at=10)
add_commands(pet)       # commands_run 1, stage "egg"
add_commands(pet, 4)    # commands_run 5, stage "cracking"
```

Raises `TypeError` if `pet` isn't a dictionary or `count` isn't an integer
(`True` and `False` are rejected), and `ValueError` if `pet` is missing a key
or `count` is zero or negative.


## Contributing

### 1. Get the code and set up the virtual environment

You need Python 3.11 or newer and git.

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-respin.git
cd python-package-exercise-respin
pip install pipenv
pipenv install --dev
```

The `Pipfile` targets Python 3.12. If you have a different version installed
(3.11 or newer), tell pipenv which one to use:

```bash
pipenv install --dev --python 3.11
```

### 2. Run the tests

```bash
pipenv run pytest
```

### 3. Build the package

```bash
pipenv run python -m build
```

This creates a `dist/` folder containing a `.whl` file and a `.tar.gz` file,
which are the files uploaded to PyPI.

### 4. Make a change

1. Create a feature branch: `git checkout -b my-feature`
2. Commit your changes and push the branch.
3. Open a pull request into `main`. GitHub Actions runs the tests on
   Python 3.11 and 3.12, and a teammate reviews and merges it.

## Configuration

No configuration is needed. The package does not use environment variables,
a `.env` file, secret keys, or a database, so there is nothing to set up
before running it.

## Team

- [YusefMoustafa](https://github.com/YusefMoustafa)
- [sing1179](https://github.com/sing1179)
- [TonyyZhou](https://github.com/TonyyZhou)
- [denisekos](https://github.com/denisekos)
