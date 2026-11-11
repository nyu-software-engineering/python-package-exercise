from .pet import clamp

def increase_happiness(pet, happiness_change):
    """Increment pet happiness by specified amount"""
    pet["happiness"] = clamp(pet["happiness"] + happiness_change)
    return pet["happiness"]

def decrease_happiness(pet, happiness_change):
    """Decrement pet happiness by specified amount"""
    pet["happiness"] = clamp(pet["happiness"] - happiness_change)
    return pet["happiness"]
