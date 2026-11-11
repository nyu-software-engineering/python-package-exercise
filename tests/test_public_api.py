import realesagent
from realesagent import (
    apology_multiplier,
    desperation_level,
    extension_request,
    generate_excuse,
    grade_beg,
    professionalize,
    professor_reply,
    subject_line,
    absence_excuse,
)
from realesagent.excuses import generate_excuse as original_generate_excuse


def test_all_nine_functions_are_public():
    functions = {
        "generate_excuse": generate_excuse,
        "desperation_level": desperation_level,
        "professionalize": professionalize,
        "extension_request": extension_request,
        "grade_beg": grade_beg,
        "subject_line": subject_line,
        "apology_multiplier": apology_multiplier,
        "professor_reply": professor_reply,
        "absence_excuse": absence_excuse,
    }

    assert set(realesagent.__all__) == set(functions)
    assert len(realesagent.__all__) == 9

    for name, function in functions.items():
        assert callable(function)
        assert getattr(realesagent, name) is function

    assert generate_excuse is original_generate_excuse
