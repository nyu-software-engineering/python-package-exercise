from .get_stage import STAGES
import dateutil
import datetime

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
    "easter_egg": [
        "    .----.",
        "   /      \\",
        "  |/\\/\\/\\/\\|",
        "  |/\\/\\/\\/\\|",
        "   \\      /",
        "    '----'",
    ],
}

_MESSAGES = {
    "egg": "...",
    "cracking": "Is someone out there?",
    "hatchling": "I'm out!",
    "young python": "More commands, please!",
    "full python": "Hsss. I am complete.",
}


def pet_says(stage):
    """Return what the pet says at the given growth stage."""
    _check_stage(stage)
    return _MESSAGES[stage]


def _check_stage(stage):
    if not isinstance(stage, str):
        raise TypeError("stage must be a string")
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}, expected one of {STAGES}")


def _speech_bubble(message):
    width = len(message) + 2
    return [
        " " + "_" * width,
        "< " + message + " >",
        " " + "-" * width,
        "     \\",
    ]


def draw_pet(stage, message=None, easter_override=None):
    """Return ASCII art of the pet at the given growth stage.

    If message is given, the pet says it in a speech bubble above the art.
    """
    _check_stage(stage)
    if message is not None and not isinstance(message, str):
        raise TypeError("message must be a string")
    
    is_easter = (dateutil.easter.easter(datetime.datetime.now().year) == datetime.datetime.now().date()) or easter_override
    if is_easter and stage == "egg":
        stage = "easter_egg"

    lines = list(_ART[stage])
    if message:
        lines = _speech_bubble(message) + lines
    return "\n".join(lines)
