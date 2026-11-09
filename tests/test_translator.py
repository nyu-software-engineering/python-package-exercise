from ascend import translator


class Tests:

    def test_swaps_multiple_words_and_phrases(self):
        assert translator.translate_sentence("I worked out, then studied.") == (
            "I gymmaxxed, then studymaxxed."
        )
        assert translator.translate_sentence("Stop making excuses and improve!") == (
            "Stop coping and ascend!"
        )
        assert translator.translate_sentence("He outshined me after a big setback.") == (
            "He mogged me after a brutal failo."
        )
        assert translator.translate_sentence("Its standout feature hid its weak spot.") == (
            "Its halo hid its failo."
        )
        assert translator.translate_sentence("The comeback never started.") == (
            "The comeback never began."
        )

    def test_phrase_takes_priority(self):
        assert translator.translate_sentence("I outshined everyone.") == (
            "I mogged the whole lobby."
        )
        assert translator.translate_sentence("I want to work out.") == "I want to gymmaxx."

    def test_preserves_punctuation_and_initial_capital(self):
        assert translator.translate_sentence('“Studied?!” (Improved.)') == (
            '“Studymaxxed?!” (Ascended.)'
        )
        assert translator.translate_sentence('“Worked out?!” (Studied.)') == (
            '“Gymmaxxed?!” (Studymaxxed.)'
        )
        assert translator.translate_sentence("It’s over...") == "Its so over..."
        assert translator.translate_sentence("I worked, out and understudied.") == (
            "I worked, out and understudied."
        )

    def test_translates_three_word_phrases(self):
        assert translator.translate_sentence('“Everything is ruined?!”') == (
            '“Everything is kirked?!”'
        )
        assert translator.translate_sentence("Everything is, ruined.") == (
            "Everything is, ruined."
        )

    def test_unmatched_input_stays_exactly_as_written(self):
        original = "  Did the train arrive?\t Finally!  "
        assert translator.translate_sentence(original) == original
        assert translator.translate_sentence("?!") == "?!"

    def test_normalizes_spacing_after_a_swap(self):
        assert translator.translate_sentence("  I  studied\tthen improved. ") == (
            "I studymaxxed then ascended."
        )

    def test_invalid_inputs(self):
        assert translator.translate_sentence("") is None
        assert translator.translate_sentence("   \t\n") is None
        assert translator.translate_sentence(None) is None
        assert translator.translate_sentence(["worked out"]) is None
