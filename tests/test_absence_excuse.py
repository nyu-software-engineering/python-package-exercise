from realesagent.excuses import absence_excuse


def test_absence_excuse():
    result = absence_excuse("English")

    assert isinstance(result, str)
    assert "English" in result
    assert len(result) > 0