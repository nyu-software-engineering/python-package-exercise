def create_egg(name, hatch_at=50):
    

    if not isinstance(name, str):

        raise TypeError("name must be a string")
    

    name = name.strip()

    if not name:

        raise ValueError("name cannot be empty")
    

    if isinstance(hatch_at, bool) or not isinstance(hatch_at, int):

        raise TypeError("hatch_at must be an integer")
    

    if hatch_at <= 0:
        
        raise ValueError("hatch_at must be positive")

    return {
        "name": name,
        "hatch_at": hatch_at,
        "commands_run": 0,
        "stage": "egg",
    }