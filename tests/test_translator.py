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
        assert translator.translate_sentence("We should study more.") == "We should studymaxx more."
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

    def test_guesses_actions_from_cues(self):
        assert translator.translate_sentence("I will laminate my notes. I'm gonna calibrate the telescope.") == (
            "I will laminatemaxx my notes. I'm gonna calibratemaxx the telescope."
        )
        assert translator.translate_sentence("Will Rogers left the plan on my desk.") == (
            "Will Rogers left the plan on my desk."
        )
        assert translator.translate_sentence("I’m going to cook dinner.") == "I’m going to cookmaxx dinner."
        assert translator.translate_sentence("I'm going to London.") == "I'm going to London."
        assert translator.translate_sentence("I have to study tonight.") == "I have to studymaxx tonight."
        assert translator.translate_sentence("Im gonna cook.") == "Im gonna cookmaxx."

    def test_maxx_rule_preserves_modifiers(self):
        assert translator.translate_sentence("I'm trying to quietly leave the room.") == (
            "I'm trying to quietly leavemaxx the room."
        )
        assert translator.translate_sentence("I want to quickly work out.") == (
            "I want to quickly gymmaxx."
        )
        assert translator.translate_sentence("I will always remember this.") == (
            "I will always remembermaxx this."
        )
        assert translator.translate_sentence("She will probably win.") == "She will probably mog."
        assert translator.translate_sentence("I will also still remember this.") == (
            "I will also still remembermaxx this."
        )

    def test_work_out_means_exercise_only_in_exercise_context(self):
        assert translator.translate_sentence("Things worked out fine.") == "Things worked out fine."
        assert translator.translate_sentence("It will work out.") == "It will work out."
        assert translator.translate_sentence("She will work out the details.") == (
            "She will work out the details."
        )
        assert translator.translate_sentence("Maya worked out a lot.") == "Maya gymmaxxed a lot."

    def test_matches_idioms_and_slots_with_intensifiers(self):
        assert translator.translate_sentence("It’s really over.") == "Its jover."
        assert translator.translate_sentence("I really messed up.") == "I really fumbled."

    def test_translates_focused_and_stressed_phrases(self):
        assert translator.translate_sentence("She is focused.") == "She is locked in."
        assert translator.translate_sentence("I am stressed.") == "My cortisol spiked."
        assert translator.translate_sentence("I'm really stressed out about class.") == (
            "My cortisol really spiked over class."
        )
        assert translator.translate_sentence("She's focused the camera.") == "She's focused the camera."
        assert translator.translate_sentence("She's stressed the importance of sleep.") == (
            "She's stressed the importance of sleep."
        )

    def test_translates_comparisons_between_people(self):
        assert translator.translate_sentence("He is taller than me.") == "He heightmogs me."
        assert translator.translate_sentence("I'm taller than Ted.") == "I heightmog Ted."
        assert translator.translate_sentence("They were faster than my brother.") == (
            "They speedmogged my brother."
        )
        assert translator.translate_sentence("She is a lot smarter than my sister.") == (
            "She giga IQmogs my sister."
        )
        assert translator.translate_sentence("She is better than everyone.") == (
            "She mogs the whole lobby."
        )

    def test_leaves_other_meanings_intact(self):
        assert translator.translate_sentence("He is faster than last year.") == (
            "He is faster than last year."
        )
        assert translator.translate_sentence("He is taller than my brother is.") == (
            "He is taller than my brother is."
        )
        assert translator.translate_sentence("She is faster than her car.") == (
            "She is faster than her car."
        )
        assert translator.translate_sentence("Beat the eggs.") == "Beat the eggs."

    def test_translates_outcomes_in_context(self):
        assert translator.translate_sentence("We won the game. I failed my exam.") == (
            "We mogged the whole lobby. I fumbled my exam."
        )
        assert translator.translate_sentence("I lost all my money. He always wins.") == (
            "I fumbled all my money. He always mogs."
        )
        assert translator.translate_sentence("That guy is always lying.") == (
            "That guy is always frauding."
        )
        assert translator.translate_sentence("I lost my keys. He was lying on the floor.") == (
            "I lost my keys. He was lying on the floor."
        )

    def test_translates_adjectives_and_their_modifiers(self):
        assert translator.translate_sentence("I'm so tired. Really good. So annoying.") == (
            "I'm giga cooked. Legit based. Giga brutal."
        )
        assert translator.translate_sentence("She looks very confident. I'm so happy.") == (
            "She looks unironically low cortisol. I'm giga lifefueled."
        )
        assert translator.translate_sentence("That's really good news.") == "That's really lifefuel."
        assert translator.translate_sentence("It rained, so I left.") == "It rained, so I left."

    def test_leaves_light_verbs_and_translates_the_activity(self):
        assert translator.translate_sentence("I want to go to the gym.") == "I want to gymmaxx."
        assert translator.translate_sentence("I will start eating healthy.") == (
            "I will start dietmaxxing."
        )
        assert translator.translate_sentence("I need to stop procrastinating.") == (
            "I need to stop rotting."
        )
        assert translator.translate_sentence("I need to learn how to cook. I want to hang out.") == (
            "I need to learn how to cook. I want to hang out."
        )
        assert translator.translate_sentence("I feel great after working out.") == (
            "I feel lifefueled after gymmaxxing."
        )

    def test_translates_joined_comparisons_with_the_same_tense(self):
        assert translator.translate_sentence("She was smarter than him and richer than us.") == (
            "She IQmogged him and moneymogged us."
        )
        assert translator.translate_sentence("She was smarter than him, and richer than us.") == (
            "She IQmogged him, and moneymogged us."
        )
        assert translator.translate_sentence("She was smarter than him. And richer than us.") == (
            "She IQmogged him. And richer than us."
        )

    def test_translates_common_short_phrases(self):
        assert translator.translate_sentence("I'm proud of you. That was the best.") == (
            "I'm mirin you. That was peak."
        )
        assert translator.translate_sentence("I got rejected. My plans are ruined.") == (
            "I got blackpilled. My plans are kirked."
        )
        assert translator.translate_sentence("I got the best score.") == "I got the best score."

    def test_preserves_all_caps_and_line_breaks(self):
        assert translator.translate_sentence("IT’S OVER") == "ITS JOVER"
        assert translator.translate_sentence("I STUDIED.\r\n\r\nIt's over.\nThe train arrived.") == (
            "I STUDYMAXXED.\r\n\r\nIts jover.\nThe train arrived."
        )

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

    def test_mihir_alias(self):
        assert translator.translate_sentence("Mihir!") == "HTN!"
        assert translator.translate_sentence("mihir") == "HTN"
        assert translator.translate_sentence("mihir is a good guy") == "HTN is a good guy"
        assert translator.translate_sentence("mihir is a bad guy") == "HTN is a bad guy"
        assert translator.translate_sentence("mihir is a good guy") == "HTN is a good guy"

    def test_everyday_idioms(self):
        assert translator.translate_sentence("I hit the books.") == "I studymaxx."
        assert translator.translate_sentence("Call it a day.") == "Log off."
        assert translator.translate_sentence("She is on top of the world.") == "She is peak aura."

    def test_sleep_and_hydration_verbs(self):
        assert translator.translate_sentence("I need to sleep.") == "I need to restmaxx."
        assert translator.translate_sentence("She hydrated after the run.") == "She watermaxxed after the run."
        assert translator.translate_sentence("I'm going to sleep.") == "I'm going to restmaxx."

    def test_infers_actions_after_more_modals(self):
        assert translator.translate_sentence("I could budget.") == "I could budgetmaxx."
        assert translator.translate_sentence("They might nap.") == "They might napmaxx."
    
    def test_subject_be_adjective_phrases(self):
        assert translator.translate_sentence("She is so bored.") == "She is giga rotting."
        assert translator.translate_sentence("I'm nervous.") == "I'm high cortisol."

    def test_age_and_health_comparisons(self):
        assert translator.translate_sentence("She is older than me.") == "She agemogged me."
        assert translator.translate_sentence("He is fitter than Ted.") == "He fitnessmogs Ted."