import pyDeciders
from pyDeciders.cli import main


def test_package_imports():
    assert pyDeciders.__name__ == "pyDeciders"
