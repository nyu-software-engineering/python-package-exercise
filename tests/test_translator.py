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
        assert translator.translate_sentence("It’s over...") == "Its jover..."
        assert translator.translate_sentence("It's so over!") == "Its jover!"
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
        assert translator.translate_sentence("We’re done for, but I studied.") == (
            "Its jover for us, but I studymaxxed."
        )

    def test_swaps_meme_slang_in_context(self):
        assert translator.translate_sentence("That's wishful thinking, basement dweller.") == (
            "That's copium, chud."
        )
        assert translator.translate_sentence('She asked what "femoid" means.') == (
            'She asked what "foid" means.'
        )
        assert translator.translate_sentence("She is an average person.") == (
            "She is a normie."
        )
        assert translator.translate_sentence("Good news, I was just pretending.") == (
            "Lifefuel, I was just larping."
        )
        assert translator.translate_sentence("The woman left early.") == "The woman left early."

    def test_creates_slang_for_unfamiliar_actions(self):
        assert translator.translate_sentence("I'm trying to cook dinner.") == (
            "I'm trying to cookmaxx dinner."
        )
        assert translator.translate_sentence("Do you want to nap?") == "Do you want to napmaxx?"
        assert translator.translate_sentence("Try to budget!") == "Try to budgetmaxx!"

    def test_translates_everyday_phrasing(self):
        assert translator.translate_sentence("I got better, but she did better than me.") == (
            "I ascended, but she mogged me."
        )
        assert translator.translate_sentence("I need to study for the test. I'm screwed.") == (
            "I need to studymaxx for the test. Its jover for me."
        )
        assert translator.translate_sentence("I messed up. He was making stuff up.") == (
            "I fumbled. He was larping."
        )
        assert translator.translate_sentence("I did better than expected.") == (
            "I did better than expected."
        )

    def test_preserves_verb_forms_and_nouns(self):
        assert translator.translate_sentence("She works out and makes excuses.") == (
            "She gymmaxxes and copes."
        )
        assert translator.translate_sentence("We're getting better. It is over!") == (
            "We're ascending. Its jover!"
        )
        assert translator.translate_sentence("I study every night.") == "I studymaxx every night."
        assert translator.translate_sentence("Students study hard.") == "Students studymaxx hard."
        assert translator.translate_sentence("They outshone us.") == "They mogged us."
        assert translator.translate_sentence("The study for the course is ready.") == (
            "The study for the course is ready."
        )

    def test_fills_slots_from_the_sentence(self):
        assert translator.translate_sentence("She did better than Maya after they messed up.") == (
            "She mogged Maya after they fumbled."
        )
        assert translator.translate_sentence("She did better than everyone.") == (
            "She mogged the whole lobby."
        )
        assert translator.translate_sentence("I was lying about my age, but she lied about her salary.") == (
            "I was agefrauding, but she salaryfrauded."
        )
        assert translator.translate_sentence("I was lying about my new job.") == (
            "I was lying about my new job."
        )
        assert translator.translate_sentence("Maya messed up.") == "Maya fumbled."
        assert translator.translate_sentence("She did better than my brother.") == (
            "She mogged my brother."
        )
        assert translator.translate_sentence("She did better than Expected.") == (
            "She did better than Expected."
        )
        assert translator.translate_sentence("I was lying about my age to her.") == (
            "I was agefrauding to her."
        )

    def test_maxx_rule_preserves_modifiers(self):
        assert translator.translate_sentence("I'm trying to quietly leave the room.") == (
            "I'm trying to quietly leavemaxx the room."
        )
        assert translator.translate_sentence("I want to quickly work out.") == (
            "I want to quickly gymmaxx."
        )
        assert translator.translate_sentence("I want to always quietly leave.") == (
            "I want to always quietly leavemaxx."
        )

    def test_matches_idioms_and_slots_with_intensifiers(self):
        assert translator.translate_sentence("It’s really over.") == "Its jover."
        assert translator.translate_sentence("I really messed up.") == "I really fumbled."

    def test_leaves_context_and_already_maxxed_words_intact(self):
        assert translator.translate_sentence("I want to gymmaxx before my chemistry lab.") == (
            "I want to gymmaxx before my chemistry lab."
        )
        assert translator.translate_sentence("I studied and tried to be honest.") == (
            "I studymaxxed and tried to be honest."
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
