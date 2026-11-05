from ascend.models import pick_model


def test_pick_model_valid_categories():
    assert pick_model("runway") == "Bella Hadid"
    assert pick_model("editorial") == "Vittoria Ceretti"
    assert pick_model("classic") == "Kate Moss"
    assert pick_model("angel") == "Adriana Lima"
    assert pick_model("high-fashion") == "Anok Yai"


def test_pick_model_invalid_category():
    try:
        pick_model("unknown")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_pick_model_invalid_type():
    try:
        pick_model(123)
        assert False, "Expected ValueError"
    except ValueError:
        pass