from desktop_cat import Cat, MOODS, run


def test_new_cat_defaults():
    cat = Cat()
    assert cat.name == "Whiskers"
    assert cat.mood == "happy"
    assert cat.mood in MOODS
    cat.say("test test test testtesttesttesttest")
    run() #begin window loop