import importlib
from pathlib import Path


def test_package_imports():
    package = importlib.import_module("package")

    assert package is not None
    assert package.__name__ == "package"
    assert package.__file__ is not None
    assert Path(package.__file__).name == "__init__.py"