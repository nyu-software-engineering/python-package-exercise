def pick_model(category):
    models = {
        "runway": "Bella Hadid",
        "editorial": "Vittoria Ceretti",
        "classic": "Kate Moss",
        "angel": "Adriana Lima",
        "high-fashion": "Anok Yai"
    }

    if not isinstance(category, str):
        raise ValueError("Category must be a string")

    if category not in models:
        raise ValueError("Invalid model category")

    return models[category]