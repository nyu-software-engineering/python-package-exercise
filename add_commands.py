from get_stage import get_stage


def add_commands(pet, count=1):
    """Add terminal commands to a pet and update its stage.

    Args:
        pet: a pet dictionary made by create_egg().
        count: how many commands to add (a positive integer, default 1).

    Returns:
        The same pet dictionary, with commands_run and stage updated.

    Example:
        >>> from create_egg import create_egg
        >>> pet = create_egg("Bob", hatch_at=10)
        >>> pet = add_commands(pet, 5)
        >>> pet["commands_run"]
        5
        >>> pet["stage"]
        'cracking'
    """
    if not isinstance(pet, dict):
        raise TypeError("pet must be a dictionary")

    for key in ("name", "hatch_at", "commands_run", "stage"):
        if key not in pet:
            raise ValueError(f"pet is missing key: {key}")

    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("count must be an integer")
    
    if count <= 0:
        raise ValueError("count must be positive")


    pet["commands_run"] += count
    pet["stage"] = get_stage(pet["commands_run"], pet["hatch_at"])
    return pet

 