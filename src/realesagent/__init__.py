"""Funny student excuses and even funnier responses ;)"""

from .excuses import generate_excuse, grade_beg, apology_multiplier, absence_excuse
from .emails import extension_request, subject_line
from .student import desperation_level, professionalize
from .responses import professor_reply

__all__ = [
    "generate_excuse",
    "desperation_level",
    "professionalize",
    "extension_request",
    "grade_beg",
    "subject_line",
    "apology_multiplier",
    "professor_reply",
    "absence_excuse"
]
