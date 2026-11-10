from realesagent import professor_reply


def test_professor_reply_tones():
    cases = [
        ("strict", "As stated in the syllabus"),
        ("sympathetic", "Let's discuss a realistic plan"),
        ("sarcastic", "A remarkable plot twist"),
    ]
    for tone, phrase in cases:
        result = professor_reply("I need an extension.", tone)
        assert phrase in result
        assert '"I need an extension."' in result
        assert result.endswith("Your Fictional Professor")


def test_professor_reply_uses_email_and_defaults_to_strict():
    assert professor_reply("Help") == professor_reply("Help", "strict")
    assert professor_reply("Grade question") != professor_reply("Extension question")
    assert '"Please help"' in professor_reply("  Please\n help ")


def test_professor_reply_invalid_inputs():
    cases = [
        ("", "strict", ValueError),
        (" \n", "strict", ValueError),
        (None, "strict", TypeError),
        (42, "strict", TypeError),
        ("Help", "angry", ValueError),
        ("Help", "Strict", ValueError),
        ("Help", None, TypeError),
    ]
    for email, tone, expected_error in cases:
        try:
            professor_reply(email, tone)
        except expected_error:
            pass
        else:
            assert False, "Expected an error for invalid email or tone"
