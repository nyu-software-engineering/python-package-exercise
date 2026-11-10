<!-- badge -->

# Fun Casino

FunCasino is a Python package that simulates some of the most popular casino games, including blackjack, roulette, and slots, for educational purposes.

<!-- [PyPI Link](https://www.google.com/) -->

## Team Members
- [Shuo Cao](https://github.com/ShuoWu6529)
- [Jack Jiang](https://github.com/jack-k-jiang)
- [Ronald Szeto](https://github.com/ronaldszeto)
- [Eric Wu](https://github.com/ew2725)
- [Ruikun Xu](https://github.com/xuruikun)

## Installation & Contribution

### 0. Prerequisites

- Python 3.15

### 1. Clone repository

Clone a copy of this repository to your local machine from GitHub and open the repository directory.

### 2. Install dependencies and set up virtual environment

After cloning this repository, run `pipenv install --dev` from the main project directory. This creates the project's virtual environment and installs everything listed in the `Pipfile`:

- `[packages]` - what the package itself needs to run. Here, that's just the package itself, installed in "_editable_" mode.
- `[dev-packages]` - tools needed only while developing the package, such as `pytest`, `coverage`, [build](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives), and [twine](https://packaging.python.org/en/latest/key_projects/#twine). The `--dev` flag installs these too.

### 3. Run the program

FunCasino could be run as a program through `pipenv run python -m funcasino`. Each game is also an importable module that can be used in any file after downloading the package.

### 4. Running tests

Simple example unit tests are included within the `tests` directory. To run these tests...

1. Activate the virtual environment, if not yet done, e.g. `pipenv shell`.
2. Install all the project's dependencies, including dev dependencies like `pytest`, into the virtual environment, e.g. `pipenv install --dev`.
3. Run the tests from the main project directory: `python3 -m pytest`.
4. Tests should never fail. Any failed tests indicate that the production code is behaving differently from the behavior the tests expect.

### Contribute

Contributions are always welcome! If there are any bugs or feature suggestions, feel free to open an issue describing it.

To contribute to issues:

1. Fork this repository and clone your fork to your local machine.
2. Follow the installation & setup instructions.
3. Make your changes by fixing an issue or adding a feature (make sure to add or update tests if necessary).
4. Run the tests with `pipenv run python -m pytest`.
5. Commit the changes, push them to the forked repository, and open a pull request explaining your changes.

## Documentation

### Blackjack

### Coin Toss

### Slots

### Craps

### Roulette