import pytest
from project.magic8ball import custom_answer

class Tests:
    @pytest.fixture
    def example_fixture(self):
        yield
    def test_sanity_check(self, example_fixture):
        expected = True
        actual = True
        assert actual == expected
    def test_positive_answer(self):
        actual = custom_answer("I love this!", "positive")
        assert actual["positive"] == ["I love this!"]
    def test_non_commital_answer(self):
        actual = custom_answer("Eh", "non-committal")
        assert actual["non-committal"] == ["Eh"]
    def test_negative_answer(self):
        actual = custom_answer("I hate this", "negative")
        assert actual["negative"] == ["I hate this"]
    def test_invalid_category(self): 
        actual = custom_answer("I'm not sure", "neutral")
        expected = {"positive": [], "non-committal":[], "negative":[]}
        assert actual == expected
    def test_uppercase_category(self):
        actual = custom_answer("In Love!", "POSITIVE")
        assert actual["positive"] == ["In Love!"]
