# Python Package Exercise
![build-test](https://github.com/software-students-fall2026/python-package-exercise-respin/actions/workflows/build-test.yml/badge.svg)

# terminal-pet-respin

A tiny pet python that lives in your terminal. It starts as an egg, and every
terminal command you run helps it grow: from egg, to cracking egg, to hatchling,
to young python, and finally to a full coiled python.

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

Pass a message to make the pet talk, or use `pet_says(stage)` for its default line:

```python
from terminal_pet_respin import draw_pet, pet_says

print(draw_pet("hatchling", pet_says("hatchling")))
```

```
 __________
< I'm out! >
 ----------
     \
     .---.
    ( O O )
     \   /~
  \/\/   \/\/
   \        /
    '------'
```



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


## Running the tests

```bash
pip install pipenv
pipenv install --dev
pipenv run pytest
```
