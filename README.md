# 🎱 Magic 8 Ball

[![Build & Test](https://github.com/software-students-fall2026/python-package-exercise-csyy/actions/workflows/build.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-csyy/actions/workflows/build.yml)

A Python package that works like a Magic 8 Ball. Ask a yes-or-no question, pick a number, and get your answer. You can also add your own answers.

**PyPI:** https://pypi.org/project/magic8ball-csyy/

## Install

Requires Python 3.12+.

```bash
pip install magic8ball-csyy
```

The package is imported as `project`.

## How to Use

```python
from project.magic8ball import (
    get_question,
    select_category,
    get_response,
    custom_answer,
    normalize_category,
)
```

### `get_question(question)`
Checks that the question is a non-empty string and returns it trimmed.

```python
get_question("  Will I pass?  ")   # "Will I pass?"
get_question("")                   # ValueError
```

### `select_category(number)`
Pick a number from 0 to 8. Returns `"Positive"`, `"Non-Committal"`, or `"Negative"` at random. Returns `"Invalid number"` for anything else.

```python
select_category(3)    # e.g. "Positive"
select_category(10)   # "Invalid number"
```

### `get_response(category, custom_answers=None)`
Returns a random answer from the category. You can pass in extra answers from `custom_answer()`.

```python
get_response("positive")                                # e.g. "It is certain"
get_response("negative", {"negative": ["No way!"]})     # may return "No way!"
```

### `custom_answer(answer, category)`
Adds your own answer to a category and returns it as a dictionary.

```python
custom_answer("Absolutely!", "positive")
# {"positive": ["Absolutely!"], "non-committal": [], "negative": []}
```

### `normalize_category(category)`
Cleans up a category name.

```python
normalize_category("Non Committal")   # "non-committal"
```

### Example Program

See [examples/example.py](https://github.com/software-students-fall2026/python-package-exercise-csyy/blob/main/examples/example.py) for a complete demonstration of all package functions.

Run the example from the repository's root directory:

```bash
pipenv run python -m examples.example
```

On Windows, if you get a `UnicodeEncodeError`, run `$env:PYTHONIOENCODING="utf-8"` in PowerShell first.


## Contributing

### 1. Clone the repository

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-csyy.git
cd python-package-exercise-csyy
```

### 2. Set up the environment

Install Python 3.12 or newer, then install Pipenv:

```bash
python -m pip install pipenv
```

Install the project dependencies:

```bash
pipenv sync --dev
```

### 3. Install the package locally

```bash
pipenv run python -m pip install -e .
```

### 4. Run the tests

```bash
pipenv run python -m pytest
```

### 5. Build the package

```bash
pipenv run python -m build
```

The generated distribution files will appear in the `dist/` directory.


## Configuration

No environment variables, `.env` files, or database are needed.

## Team

- [Coco Ke](https://github.com/LefeiKe)
- [Sofia Matari](https://github.com/sofia-matari)
- [Yazid](https://github.com/Dizay-53)
- [Yasmine](https://github.com/yasminek27)
- [Leslie Sampaney](https://github.com/Leslie-Sampaney)

## License

[GPL-3.0](https://github.com/software-students-fall2026/python-package-exercise-csyy/blob/main/LICENSE)
