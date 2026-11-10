from pyfakefacts.facts import generate_fact

def test_generate_fact_returns_string():
    result = generate_fact("cats", "animals")

    assert isinstance(result, str)


def test_generate_fact_is_not_empty():
    result = generate_fact("cats", "animals")

    assert len(result.strip()) > 0


def test_generate_fact_contains_inputs():
    result = generate_fact("cats", "animals")

    assert "cats" in result
    assert "animals" in result