from desktop_cat import Cat

# Checks output of basic status(), makes sure other attributes are not present
def test_status_basic():
    cat = Cat(name="Milo", mood="sad")
    assert "Milo" in cat.status()
    assert "sad" in cat.status()
    assert cat.status() == "Milo is feeling sad."
    assert "Hunger" not in cat.status()

# Makes sure extended attributes are present in Cat instance, and are printed accordingly
def test_status_long():
    cat = Cat()
    cat.times_petted = 3
    cat.foods_eaten = {"fish": 2}

    assert cat.times_petted == 3
    assert cat.foods_eaten == {"fish": 2}
    assert cat.hunger == 5

    text = cat.status(long=True)
    
    assert "Petted 3 times" in text
    assert "Meals eaten: 2" in text
    assert "Hunger: 5/10" in text

# Makes sure meal count is 0 if no foods have been eaten
def test_status_long_no_food():
    cat = Cat()
    text = cat.status(long=True)

    assert "Meals eaten: 0" in text

# Makes sure meal count counts all food types up
def test_status_long_multiple_foods():
    cat = Cat()
    cat.foods_eaten = {
        "fish": 2,
        "milk": 3,
        "kibble": 1
    }

    assert "Meals eaten: 6" in cat.status(long=True)

# Returns type
def test_status_returns_string():
    assert isinstance(Cat().status(), str)