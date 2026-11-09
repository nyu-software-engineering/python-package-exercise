STAGES = ("egg", "cracking", "hatchling", "young python", "full python")


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


def get_stage(commands_run, hatch_at):
    _check_int(commands_run, "commands_run")
    _check_int(hatch_at, "hatch_at")
    if commands_run < 0:
        raise ValueError("commands_run cannot be negative")
    if hatch_at <= 0:
        raise ValueError("hatch_at must be positive")

    if commands_run * 2 < hatch_at:
        return "egg"
    if commands_run < hatch_at:
        return "cracking"
    if commands_run < hatch_at * 2:
        return "hatchling"
    if commands_run < hatch_at * 4:
        return "young python"
    return "full python"
