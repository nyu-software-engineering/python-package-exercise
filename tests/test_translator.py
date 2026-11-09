from ascend import translator


class Tests:

    def test_preserves_punctuation_and_initial_capital(self):
        assert translator.translate_sentence('“Studied?!” (Improved.)') == (
            '“Studymaxxed?!” (Ascended.)'
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
