from realesagent import desperation_level, professionalize


def test_desperation_bounds_and_each_input():
    assert desperation_level(100, 72, 0) == 1
    assert desperation_level(0, -1, 10) == 10
    assert desperation_level(80, 72, 0) == 2
    assert desperation_level(100, 48, 0) == 2
    assert desperation_level(100, 72, 1) == 2
    assert type(desperation_level(69.4, 12.5, 2)) is int


def test_deadline_boundaries():
    cases = [(49, 1), (48, 2), (25, 2), (24, 3), (1, 3), (0, 4), (-1, 4), (-100, 4)]
    for hours, expected in cases:
        assert desperation_level(100, hours, 0) == expected


def test_grade_boundaries():
    assert desperation_level(100, 72, 0) == 1
    assert desperation_level(99.9, 72, 0) == 2
    assert desperation_level(80, 72, 0) == 2
    assert desperation_level(79.9, 72, 0) == 3
    assert desperation_level(0, 72, 0) == 6


def test_missing_assignments_cap():
    assert desperation_level(100, 72, 2) == 3
    assert desperation_level(100, 72, 3) == 4
    assert desperation_level(100, 72, 100) == 4


def test_desperation_invalid_inputs():
    cases = [
        (-1, 72, 0, ValueError),
        (101, 72, 0, ValueError),
        (float("nan"), 72, 0, ValueError),
        (50, float("inf"), 0, ValueError),
        (50, float("-inf"), 0, ValueError),
        (50, float("nan"), 0, ValueError),
        ("50", 72, 0, TypeError),
        (True, 72, 0, TypeError),
        (50, None, 0, TypeError),
        (50, False, 0, TypeError),
        (50, 72, -1, ValueError),
        (50, 72, 1.5, TypeError),
        (50, 72, True, TypeError),
    ]
    for grade, hours, missing, expected_error in cases:
        try:
            desperation_level(grade, hours, missing)
        except expected_error:
            pass
        else:
            assert False, "Expected an error for invalid desperation input"


def test_professionalize_recognized_phrases():
    cases = [
        ("I overslept", "circadian scheduling"),
        ("I slept in", "circadian scheduling"),
        ("I forgot", "task retention"),
        ("I procrastinated", "planning phase"),
        ("My internet broke", "digital connectivity"),
        ("My dog ate my homework", "canine review"),
    ]
    for truth, phrase in cases:
        assert phrase in professionalize(truth)


def test_professionalize_normalization_and_fallback():
    assert professionalize("  I   OVERSLEPT ") == professionalize("I overslept")
    result = professionalize("  My bicycle   vanished ")
    assert '"My bicycle vanished"' in result
    assert "respectfully request your consideration" in result


def test_professionalize_invalid_input():
    cases = [
        ("", ValueError),
        (" \n\t", ValueError),
        (None, TypeError),
        (42, TypeError),
    ]
    for truth, expected_error in cases:
        try:
            professionalize(truth)
        except expected_error:
            pass
        else:
            assert False, "Expected an error for invalid explanation text"
