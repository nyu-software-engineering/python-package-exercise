import pytest
from pyfakefacts.discoveries import generate_discovery

def test_valid_discovery():
    result = generate_discovery("physics", 5)

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_valid_absurdity_boundaries():
    assert isinstance(generate_discovery("biology", 1), str)
    assert isinstance(generate_discovery("biology", 10), str)


def test_invalid_field():
    with pytest.raises(ValueError):
        generate_discovery("magic", 5)


def test_invalid_absurdity():
    with pytest.raises(ValueError):
        generate_discovery("physics", 11)

    with pytest.raises(ValueError):
        generate_discovery("physics", 0)