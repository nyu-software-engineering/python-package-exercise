# Python Package Exercise

A little exercise to create a Python package, build it, test it, distribute it, and use it.

## Concept

A _package_ is software that has been built, tested, and distributed in a way that makes it easy for other developers to download, install, and configure to add extra functionality to their own programs. Your job is to create a Python package that brings a little bit of joy and levity to the lives of other developers. The package you create should be lighthearted and not "serious" software. However, you will create it following _rigorous_ software engineering practices.

## Inspiration

Some inspirational Python packages, for example:

- [pyjokes](https://pypi.org/project/pyjokes/)
- [pyfiglet](https://github.com/pwaller/pyfiglet)
- [pycowsay](https://pypi.org/project/pycowsay/)
- [emoji](https://pypi.org/project/emoji/)
- [freegames](https://pypi.org/project/freegames/)

## Requirements

Create a Python package with at least **four functions that accept arguments** which influence their behavior. The package must be distributed in the [PyPI](https://pypi.org/) repository and installable via [pip](https://pypi.org/project/pip/).

- Use [pipenv](https://packaging.python.org/en/latest/tutorials/managing-dependencies/) to manage the package dependencies and virtual environments with a `Pipfile`.
- Use [pytest](https://docs.pytest.org/en/latest/) to write and run tests to validate that your package code behaves as expected. Create as many tests as necessary to thorooughly verify each function's expected behavior - this should be no fewer than three tests per package function.
- Use [setuptools](https://setuptools.readthedocs.io/en/latest/) to create the package artifacts.
- Use [twine](https://pypi.org/project/twine/) to upload the package to PyPI.
- Use [GitHub Actions](https://github.com/actions) to build your package and run your tests on two different recent versions of Python with every pull request to the `main` branch of your GitHub repository.

Create an example program that uses all functions of your package and demonstrates its complete functionality.

## Developer workflow

All team members must have visibly contributed to the code using their own git/GitHub accounts in order to claim that they contributed to the project.

All code changes must be done in feature branches and not directly in the `main` branch.

To merge code from a feature branch into the `main` branch, do the following:

1. Create a pull request from the feature branch to the `main` branch.
1. Ask a fellow developer to review your code.
1. The reviewer must review the code and run unit tests to verify that the functions behave as expepcted.
1. If the reviewer has any concerns, discuss then and make any changes agreed upon.
1. Merge the pull request into the `main` branch.
1. Delete the feature branch.
1. Pull the latest changes from the remote `main` branch to your local `main` branch.

**Warning**: the longer you let code sit in a feature branch, the more likely your team is to end up in [merge hell](https://en.wikipedia.org/wiki/Merge_hell). . Merge feature branches into `main` often to avoid this fate.

## Documentation

Replace the contents of the [README.md](./README.md) file with a beautifully-formatted Markdown file including a plain-language **description** of your project and **clear instructions**, including exact **code examples**, for:

- how to install your package
- how to run the tests included in your package
- how to use your package in a Python program

Include a [badge](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge) at the top of the `README.md` file showing the result of the latest build/test workflow run.

Include the names of all teammates as links to their GitHub profiles in the README.md file.
