from desktop_cat import Cat

def test_status_basic():
    cat = Cat(name="Milo", mood="sad")
    assert "Milo" in cat.status()
    assert "sad" in cat.status()
    assert "Hunger" not in cat.status()

def test_status_long():
    cat = Cat()
    cat.times_petted = 3
    cat.foods_eaten = {"fish": 2}
    text = cat.status(long=True)
    assert "Petted 3 times" in text
    assert "Meals eaten: 2" in text
    assert "Hunger: 5/10" in text

def test_status_returns_string():
    assert isinstance(Cat().status(), str)