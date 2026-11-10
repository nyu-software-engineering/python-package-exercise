from project.magic8ball import select_category


def test_valid_numbers():
    for number in range(9):
        result = select_category(number)
        assert result in ["Positive", "Non-Committal", "Negative"]

def test_invalid_numbers():
    assert select_category(-1) == "Invalid number"
    assert select_category(9) == "Invalid number"
    assert select_category(100) == "Invalid number"

def test_invalid_types():
    assert select_category("hello") == "Invalid number"
    assert select_category(2.5) == "Invalid number"
    assert select_category(None) == "Invalid number"

def test_random_categories():
    results = set()

    for i in range(100):
        results.add(select_category(5))

    assert "Positive" in results
    assert "Non-Committal" in results
    assert "Negative" in results
