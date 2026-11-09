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

## Usage

### Title generation

### Song selection

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
