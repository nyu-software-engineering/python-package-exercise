import pytest 
from desktop_cat import Cat

# Test that eating reduces hunger
def test_eating_reduces_hunger(monkeypatch):
    cat = Cat()
    starthunger = cat.hunger

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: True)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 2)

    cat.feed("fish")
    assert cat.hunger == starthunger - 2


# Test that hunger cannot go below 0
def test_hunger_cannot_go_below_0(monkeypatch):
    cat = Cat()
    cat.hunger = 2

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: True)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 5)

    cat.feed("fish")
    assert cat.hunger == 0


# Test that invalid food raises an error
def test_invalid_food_raises_error():
    cat = Cat()
    starthunger = cat.hunger
    start_foods_eaten = cat.foods_eaten.copy()

    with pytest.raises(ValueError) as error:
        cat.feed("Premium Kibble")
    
    assert str(error.value) == "Invalid food: premium kibble"
    assert cat.hunger == starthunger
    assert cat.foods_eaten == start_foods_eaten


# Test that eating a food adds it to foods_eaten
def test_eating_adds_to_foods_eaten():
    cat = Cat()
    cat.feed("fish")

    assert "fish" in cat.foods_eaten
    assert cat.foods_eaten["fish"] == 1


# Test that feeding a food twice increments the count in foods_eaten
def test_feeding_increments_count():
    cat = Cat()

    cat.feed("fish")
    cat.feed("fish")

    assert "fish" in cat.foods_eaten
    assert cat.foods_eaten["fish"] == 2
    assert len(cat.foods_eaten) == 1
    

# Test that liked food makes mood happy
def test_liked_food_makes_mood_happy(monkeypatch):
    cat = Cat()

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: True)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 2)

    reaction = cat.feed("kibble")
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} loved the kibble!"

# Test that disliked food makes mood sad
def test_disliked_food_sad_mood(monkeypatch):
    cat = Cat()

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: False)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 1)

    reaction = cat.feed("kibble")
    assert cat.mood == "sad"
    assert reaction == f"{cat.name} did not like the kibble."

# Test that disliked food makes mood angry, does not add to foods_eaten
def test_refused_food_angry_mood(monkeypatch):
    cat = Cat()
    starthunger = cat.hunger

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: False)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 0)

    reaction = cat.feed("kibble")
    assert cat.mood == "angry"
    assert reaction == f"{cat.name} refused to eat the kibble."
    assert cat.hunger == starthunger
    assert "kibble" not in cat.foods_eaten

# Test that text inputs are normalized
def test_text_input_normalized(monkeypatch):
    cat = Cat()

    monkeypatch.setattr("desktop_cat.cat.random.choice", lambda x: True)
    monkeypatch.setattr("desktop_cat.cat.random.randint", lambda low, high: 2)

    reaction = cat.feed("MILK")
    assert "milk" in cat.foods_eaten
    assert "MILK" not in cat.foods_eaten
    assert reaction == f"{cat.name} loved the milk!"