# Ascend

## Build and test status

[![Build and test status](https://github.com/software-students-fall2026/python-package-exercise-runitback/actions/workflows/package-tests.yml/badge.svg?branch=main)](https://github.com/software-students-fall2026/python-package-exercise-runitback/actions/workflows/package-tests.yml)

## Description

Ascend is a Python package to change your life with looksmaxxing based on the viral black pill community.
Our team run-it-back are building functions that either can turn everyday topics into looksmaxxing slang and meme slop, whilst also giving the functionality to help you turn any idea you have into an edit.
This can entail suggesting a looksmaxxing song, top tier supermodel, or even just create stat cards based on a rating you are given from your looks for a hobby or everyday activity.

## Team members

- [Brian](https://github.com/BrianDai22)
- [Linh](https://github.com/katiettran)
- [Mihir](https://github.com/mihirgan06)
- [Theo](https://github.com/theoegoldstine)
- [Yash](https://github.com/yash-pandya9798)

## PyPI package

## Installation

To install Ascend from PyPI once it is published, run:

```bash
python -m pip install ascend-runitback
```

Ascend requires Python 3.13 or newer.

After installation, you can import the package into your Python program:

```python
from ascend import models
```

## Usage

### Title generation

The `make_title(activity, outcome)` function generates a random looksmaxxing-style edit title based on an activity and its outcome.

- `activity`: A non-empty string describing the activity, such as `"gym"` or `"study"`.
- `outcome`: Must be `"win"`, `"loss"`, or `"grind"`.

The function returns a randomly generated title as a string. It returns `None` if the inputs are invalid.

```python
from ascend import titles

print(titles.make_title("gym", "win"))
# Example output: "pov gymmaxxing brutal mog"

print(titles.make_title("study", "grind"))
# Example output: "studymaxxing update ascension pending"

print(titles.make_title("gym", "invalid"))
# Output: None
```
Results may vary because the function randomly selects phrases.

### Song selection

The `pick_song(category)` function recommends a song based on the category you choose.

- `category`: Must be `"gym"`, `"study"`, `"edit"`, `"chill"`, or `"BPCORE"`. Categories are case-sensitive.

The function returns a tuple containing the song title and artist. It returns `None` if the category is invalid.

```python
from ascend import songs

print(songs.pick_song("gym"))
# Output: ('METAMORPHOSIS', 'INTERWORLD')

print(songs.pick_song("study"))
# Output: ('Memory Reboot', 'VØJ, Narvent')

print(songs.pick_song("invalid"))
# Output: None
```

### Sentence translation

### Model selection

`pick_model(category)` returns a fashion model’s name as a string. The category must be `runway`, `editorial`, `classic`, `angel`, or `high-fashion`, spelled exactly as shown. The function raises `ValueError` for unsupported categories and non-string inputs.

```python
from ascend import models

print(models.pick_model("runway"))       # Bella Hadid
print(models.pick_model("high-fashion")) # Anok Yai
```

### Stat cards

## Example program

## Development setup

Make sure you have Git, Pipenv, and Python 3.13 or newer installed. Then clone the repo and install the package along with the dev dependencies.

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-runitback.git
cd python-package-exercise-runitback
pipenv install --dev
```

## Configuration

## Running tests

Run the tests from the repository folder.

```bash
pipenv run python -m pytest
```

## Building the package

Build the package from the same folder.

```bash
pipenv run python -m build
```

The build puts a wheel and a source archive in `dist/`.
