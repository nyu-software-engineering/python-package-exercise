from ascend import models

def test_pick_model_valid_categories():
    assert models.pick_model("runway") == "Bella Hadid"
    assert models.pick_model("editorial") == "Vittoria Ceretti"
    assert models.pick_model("classic") == "Kate Moss"
    assert models.pick_model("angel") == "Adriana Lima"
    assert models.pick_model("high-fashion") == "Anok Yai"

def test_pick_model_invalid_category():
    try:
        models.pick_model("unknown")
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"

def test_pick_model_invalid_type():
    try:
        models.pick_model(123)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"
