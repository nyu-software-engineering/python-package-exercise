from .get_stage import STAGES

_ART = {
    "egg": [
        "    .----.",
        "   /      \\",
        "  |        |",
        "  |        |",
        "   \\      /",
        "    '----'",
    ],
    "cracking": [
        "    .-/\\-.",
        "   /  O O \\",
        "  |  /\\/\\  |",
        "  |        |",
        "   \\      /",
        "    '----'",
    ],
    "hatchling": [
        "     .---.",
        "    ( O O )",
        "     \\   /~",
        "  \\/\\/   \\/\\/",
        "   \\        /",
        "    '------'",
    ],
    "young python": [
        "      .---.",
        "     ( O O )~<",
        "      |   |",
        "   ___/   /",
        "  (______/",
    ],
    "full python": [
        "          .---.",
        "         ( O O )~<",
        "          \\   /",
        "    .-----'   '-----.",
        "   (  .-----------.  )",
        "    (  '---------'  )",
        "     '-------------'",
    ],
}


def draw_pet(stage):
    """Return ASCII art of the pet at the given growth stage."""
    if not isinstance(stage, str):
        raise TypeError("stage must be a string")
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}, expected one of {STAGES}")

    return "\n".join(_ART[stage])