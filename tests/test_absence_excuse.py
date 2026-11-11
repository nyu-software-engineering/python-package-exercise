import pytest
from realesagent.excuses import absence_excuse


def test_absence_excuse():
    result = absence_excuse("English")

    assert isinstance(result, str)
    assert "English" in result
    assert len(result) > 0


def test_absence_excuse_empty_name():
    with pytest.raises(ValueError):
        absence_excuse("")

    with pytest.raises(ValueError):
        absence_excuse("   ")


def test_absence_excuse_invalid_type():
    with pytest.raises(TypeError):
        absence_excuse(None)

    with pytest.raises(TypeError):
        absence_excuse(123)

    with pytest.raises(TypeError):
        absence_excuse(True)


def test_absence_excuse_whitespace():
    result = absence_excuse("  Operating Systems  ")

    assert isinstance(result, str)
    assert "Operating Systems" in result
    assert "  Operating Systems  " not in result
