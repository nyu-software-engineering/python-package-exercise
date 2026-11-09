_PUNCTUATION = ".,!?;:()[]{}\"'“”‘’…—"
_MAX_PHRASE_WORDS = 8

_IDIOM_SWAPS = {
    "femoid": "foid",
    "femoids": "foids",
    "an excuse": "pure cope",
    "big setback": "brutal failo",
    "weak spot": "failo",
    "standout feature": "halo",
    "major improvement": "massive ascension",
    "small improvement": "softmaxxing gain",
    "outshined everyone": "mogged the whole lobby",
    "beat everyone": "mogged the whole lobby",
    "it's over": "its jover",
    "its over": "its jover",
    "it is over": "its jover",
    "it's hopeless": "its jover",
    "i'm screwed": "its jover for me",
    "we're screwed": "its jover for us",
    "we're done for": "its jover for us",
    "never started": "never began",
    "everything is ruined": "everything is kirked",
    "basement dweller": "chud",
    "basement dwellers": "chuds",
    "wishful thinking": "copium",
    "good news": "lifefuel",
    "great news": "lifefuel",
    "encouraging news": "hopefuel",
    "just pretending": "just larping",
    "an average person": "a normie",
    "average person": "normie",
    "average people": "normies",
    "normal person": "normie",
    "very handsome guy": "chad",
    "proud of": "mirin",
    "got rejected": "got blackpilled",
    "mihir": "HTN",
    "hit the books": "studymaxx",
    "call it a day": "log off",
    "on top of the world": "peak aura",
    "sleep": "restmaxx",
    "hydrate": "watermaxx",
}
_END_PHRASE_SWAPS = {"the best": "peak", "the worst": "brutal"}

_VERB_BASES = {
    "study": "studymaxx",
    "improve": "ascend",
    "outshine": "mog",
    "work out": "gymmaxx",
    "glow up": "ascend",
    "get better": "ascend",
    "make excuses": "cope",
    "make a mistake": "fumble",
    "make stuff up": "larp",
    "fake height": "heightfraud",
    "win the game": "mog the whole lobby",
    "go to the gym": "gymmaxx",
    "eat healthy": "dietmaxx",
    "procrastinate": "rot",
}
_OUTCOME_BASES = {"win": "mog", "lose": "fumble", "fail": "fumble", "lie": "fraud"}
_OUTCOME_OBJECTS = ("game", "match", "race", "round", "test", "exam", "class", "money")
_VERB_FORM_EXCEPTIONS = {
    "eat": ("eats", "ate", "eating"),
    "get": ("gets", "got", "getting"),
    "go": ("goes", "went", "going"),
    "lie": ("lies", "lied", "lying"),
    "lose": ("loses", "lost", "losing"),
    "make": ("makes", "made", "making"),
    "mog": ("mogs", "mogged", "mogging"),
    "plan": ("plans", "planned", "planning"),
    "rot": ("rots", "rotted", "rotting"),
    "study": ("studies", "studied", "studying"),
    "try": ("tries", "tried", "trying"),
    "win": ("wins", "won", "winning"),
    "sleep": ("sleeps", "slept", "sleeping"),
    "hydrate": ("hydrates", "hydrated", "hydrating"),
}
_VERB_ALIASES = {"outshone": "outshined"}

_ADJECTIVE_SWAPS = {
    "tired": "cooked",
    "exhausted": "cooked",
    "calm": "low cortisol",
    "relaxed": "low cortisol",
    "confident": "low cortisol",
    "focused": "locked in",
    "good": "based",
    "great": "lifefueled",
    "happy": "lifefueled",
    "excited": "lifefueled",
    "bad": "brutal",
    "terrible": "brutal",
    "annoying": "brutal",
    "awkward": "an aura loss",
    "ruined": "kirked",
    "angry": "seething",
    "mad": "seething",
}
_ADJECTIVE_CUES = ("feel", "feels", "felt", "look", "looks", "looked", "seem", "seems", "seemed")
_INTENSIFIER_SWAPS = {
    "really": "legit", "very": "unironically", "so": "giga", "super": "giga",
    "extremely": "giga", "incredibly": "giga",
}
_INTENSIFIERS = tuple(_INTENSIFIER_SWAPS)

_COMPARISON_DIMENSIONS = {
    "taller": "height",
    "stronger": "gym",
    "smarter": "IQ",
    "richer": "money",
    "faster": "speed",
    "bigger": "frame",
    "funnier": "jester",
    "hotter": "looks",
    "prettier": "looks",
    "better": "",
}

_SUBJECT_PRONOUNS = ("i", "you", "he", "she", "it", "we", "they")
_OBJECT_PRONOUNS = ("me", "you", "him", "her", "us", "them")
_POSSESSIVE_SUBJECTS = {
    "i": "my", "you": "your", "he": "his", "she": "her", "we": "our", "they": "their",
}
_POSSESSIVES = tuple(_POSSESSIVE_SUBJECTS.values())
_NOUN_CUES = ("a", "an", "the", "this", "that", "these", "those") + _POSSESSIVES
_PERSON_NOUNS = (
    "brother", "sister", "friend", "friends", "mom", "dad", "parents", "teacher",
    "coach", "teammate", "teammates", "student", "students", "kids", "people", "guy",
)
_NONPERSON_WORDS = (
    "it", "that", "this", "things", "everything", "something", "nothing", "plan", "plans",
    "expected", "usual", "normal", "average", "before", "ever", "yesterday", "today", "brakes",
)

_BE_VERBS = ("am", "is", "are", "was", "were")
_BE_CONTRACTIONS = {
    "im": ("i", "am"), "youre": ("you", "are"), "hes": ("he", "is"),
    "shes": ("she", "is"), "its": ("it", "is"), "were": ("we", "are"),
    "theyre": ("they", "are"),
}
_BE_CUES = _BE_VERBS + tuple(cue for cue in _BE_CONTRACTIONS if cue not in _BE_VERBS)

_SLOT_FOLLOWERS = ("again", "and", "before", "but", "because", "since", "to", "today", "yesterday")
_COMPARISON_FOLLOWERS = _SLOT_FOLLOWERS + ("at", "in", "on", "now", "too", "though")
_ADJECTIVE_FOLLOWERS = _COMPARISON_FOLLOWERS + ("about", "after", "enough", "for", "with")

_ACTION_MODIFIERS = (
    "always", "probably", "also", "still", "often", "usually", "sometimes",
    "definitely", "actually", "already", "even", "just", "then", "soon",
    "carefully", "quickly", "quietly", "slowly",
) + _INTENSIFIERS
_SKIP_ACTIONS = (
    "be", "have", "do", "not", "never", "go", "get", "stop", "start", "keep",
    "learn", "say", "hang",
) + _NOUN_CUES + _ACTION_MODIFIERS
_DESTINATIONS = ("home", "school", "work", "bed", "class", "college", "church", "town", "dinner")


def translate_sentence(text):
    """Rewrite matching text in BP slang and return None for invalid input."""
    if not isinstance(text, str) or not text.strip():
        return None

    translated_lines = []
    for line in text.splitlines(keepends=True):
        line_text = line.splitlines()[0]
        line_ending = line[len(line_text):]
        translated_lines.append(_translate_line(line_text) + line_ending)
    return "".join(translated_lines)


def _translate_line(text):
    word_parts = []
    lookup_words = []
    for token in text.split():
        parts = _split_punctuation(token)
        word_parts.append(parts)
        _, word, _ = parts
        lookup = word.lower().replace("’", "'")
        lookup_words.append(_VERB_ALIASES.get(lookup, lookup))

    translated_words = []
    made_swap = False
    word_index = 0
    previous_comparison_verb = None
    while word_index < len(word_parts):
        leading_punctuation, word, trailing_punctuation = word_parts[word_index]
        replacement, matched_word_count, previous_comparison_verb = _find_swap(
            word_parts, lookup_words, word_index, previous_comparison_verb
        )

        if replacement is None and _can_maxx_action(word_parts, lookup_words, word_index):
            replacement = lookup_words[word_index] + "maxx"

        if replacement is not None:
            last_index = word_index + matched_word_count - 1
            matched_words = " ".join(parts[1] for parts in word_parts[word_index:last_index + 1])
            if matched_words.isupper():
                replacement = replacement.upper()
            elif word[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            word = replacement
            trailing_punctuation = word_parts[last_index][2]
            made_swap = True

        translated_words.append(f"{leading_punctuation}{word}{trailing_punctuation}")
        word_index += matched_word_count

    if not made_swap:
        return text

    return " ".join(translated_words)


def _find_swap(word_parts, lookup_words, start_index, previous_comparison_verb):
    phrase_limit = min(start_index + _MAX_PHRASE_WORDS, len(word_parts))
    last_index = start_index
    while last_index + 1 < phrase_limit and _phrase_continues(word_parts, last_index):
        last_index += 1

    for end_index in range(last_index, start_index - 1, -1):
        replacement, comparison_verb = _match_phrase(
            word_parts, lookup_words, start_index, end_index, previous_comparison_verb
        )
        if replacement is not None:
            _, _, trailing_punctuation = word_parts[end_index]
            if trailing_punctuation not in ("", ","):
                comparison_verb = None
            return replacement, end_index - start_index + 1, comparison_verb

    return _outcome_swap(word_parts, lookup_words, start_index), 1, None


def _match_phrase(word_parts, lookup_words, start_index, end_index, previous_comparison_verb):
    words = lookup_words[start_index:end_index + 1]
    phrase = " ".join(words)
    if phrase in _IDIOM_SWAPS:
        return _IDIOM_SWAPS[phrase], None

    replacement = _verb_phrase_swap(phrase, word_parts, lookup_words, start_index, end_index)
    if replacement is not None or len(words) == 1:
        return replacement, None

    next_word = _next_word_in_phrase(word_parts, lookup_words, end_index)
    if not next_word and phrase in _END_PHRASE_SWAPS:
        return _END_PHRASE_SWAPS[phrase], None

    original_words = [parts[1] for parts in word_parts[start_index:end_index + 1]]
    if len(words) >= 3:
        replacement = _slot_swap(words, original_words, next_word)
        if replacement is not None:
            return replacement, None

    replacement, comparison_verb = _person_phrase_swap(
        words, original_words, next_word, previous_comparison_verb
    )
    if replacement is not None:
        return replacement, comparison_verb

    return _adjective_swap(words, original_words, next_word), None


def _split_punctuation(token):
    without_leading = token.lstrip(_PUNCTUATION)
    word = without_leading.rstrip(_PUNCTUATION)
    leading_punctuation = token[:len(token) - len(without_leading)]
    trailing_punctuation = without_leading[len(word):]
    return leading_punctuation, word, trailing_punctuation


def _phrase_continues(word_parts, word_index):
    next_index = word_index + 1
    if next_index == len(word_parts):
        return False
    _, _, trailing_punctuation = word_parts[word_index]
    leading_punctuation, _, _ = word_parts[next_index]
    return not (trailing_punctuation or leading_punctuation)


def _next_word_in_phrase(word_parts, lookup_words, word_index):
    if _phrase_continues(word_parts, word_index):
        return lookup_words[word_index + 1]
    return ""


def _looks_like_name(word):
    lookup = word.lower()
    return (
        word.isalpha() and word.istitle()
        and lookup not in _SUBJECT_PRONOUNS and lookup not in _NONPERSON_WORDS
    )


def _is_person_subject(word):
    lookup = word.lower()
    return (
        (lookup in _SUBJECT_PRONOUNS and lookup != "it")
        or lookup in _PERSON_NOUNS or _looks_like_name(word)
    )


def _has_person_subject(word_parts, lookup_words, start_index):
    subject_index = start_index - 1
    while subject_index >= 0 and _phrase_continues(word_parts, subject_index):
        subject = lookup_words[subject_index]
        if subject in _BE_VERBS or subject in _SUBJECT_LINKS:
            subject_index -= 1
            continue
        contraction = subject.replace("'", "")
        if contraction in _BE_CONTRACTIONS:
            return contraction != "its"
        return _is_person_subject(word_parts[subject_index][1])
    return False


def _verb_forms(base):
    if base in _VERB_FORM_EXCEPTIONS:
        present, past, ongoing = _VERB_FORM_EXCEPTIONS[base]
    else:
        present = base + "s"
        if base.endswith(("s", "sh", "ch", "x", "z")):
            present = base + "es"
        past = base + "ed"
        ongoing = base + "ing"
        if base.endswith("e"):
            past = base + "d"
            ongoing = base[:-1] + "ing"
    return base, present, past, ongoing


def _build_verb_swaps(verb_bases):
    swaps = {}
    for source, slang in verb_bases.items():
        source_verb, source_space, source_tail = source.partition(" ")
        slang_verb, slang_space, slang_tail = slang.partition(" ")
        for source_form, slang_form in zip(_verb_forms(source_verb), _verb_forms(slang_verb)):
            swaps[source_form + source_space + source_tail] = slang_form + slang_space + slang_tail
    return swaps


_VERB_SWAPS = _build_verb_swaps(_VERB_BASES)
_OUTCOME_SWAPS = _build_verb_swaps(_OUTCOME_BASES)
_LIE_FORMS = _verb_forms("lie")
_FRAUD_FORMS = _verb_forms("fraud")
_MOG_BASE, _MOG_PRESENT, _MOG_PAST, _ = _verb_forms("mog")
_ACTION_CUES = (
    _verb_forms("try") + _verb_forms("want") + _verb_forms("need") + _verb_forms("plan")
    + _verb_forms("decide") + ("have", "has", "had")
)
_SUBJECT_LINKS = ("will", "should", "to", "gonna", "going") + _ACTION_CUES + _ACTION_MODIFIERS


def _verb_phrase_swap(phrase, word_parts, lookup_words, start_index, end_index):
    replacement = _VERB_SWAPS.get(phrase)
    if replacement is None:
        return None
    if phrase in ("study", "studies"):
        if not _study_is_an_action(word_parts, lookup_words, start_index):
            return None
    if replacement.startswith("gymmaxx") and lookup_words[end_index] == "out":
        if not _work_out_is_exercise(word_parts, lookup_words, start_index, end_index):
            return None
    return replacement


def _study_is_an_action(word_parts, lookup_words, word_index):
    previous_word = ""
    if word_index > 0 and _phrase_continues(word_parts, word_index - 1):
        previous_word = lookup_words[word_index - 1]
    if previous_word in _SUBJECT_PRONOUNS or previous_word in _PERSON_NOUNS:
        return True

    return (
        previous_word not in _NOUN_CUES
        and _next_word_in_phrase(word_parts, lookup_words, word_index) == "for"
    )


def _work_out_is_exercise(word_parts, lookup_words, start_index, end_index):
    next_word = _next_word_in_phrase(word_parts, lookup_words, end_index)
    if next_word in ("what", "how", "why", "where", "whether"):
        return False
    if next_word in _NOUN_CUES and lookup_words[end_index + 1:end_index + 3] != ["a", "lot"]:
        return False

    if start_index == 0:
        return True
    if lookup_words[start_index] == "working" and _phrase_continues(word_parts, start_index - 1):
        if lookup_words[start_index - 1] in ("after", "before"):
            return True
    return _has_person_subject(word_parts, lookup_words, start_index)


def _outcome_swap(word_parts, lookup_words, word_index):
    verb = lookup_words[word_index]
    if verb not in _OUTCOME_SWAPS or not _has_person_subject(word_parts, lookup_words, word_index):
        return None

    next_word = _next_word_in_phrase(word_parts, lookup_words, word_index)
    if verb in _LIE_FORMS:
        if not next_word or next_word == "again":
            return _OUTCOME_SWAPS[verb]
        return None

    object_index = word_index
    while next_word in _NOUN_CUES + ("all",):
        object_index += 1
        next_word = _next_word_in_phrase(word_parts, lookup_words, object_index)
    if (
        not next_word
        or next_word in _OUTCOME_OBJECTS
        or next_word in ("at", "again", "today", "yesterday")
    ):
        return _OUTCOME_SWAPS[verb]
    return None


def _can_maxx_action(word_parts, lookup_words, word_index):
    leading_punctuation, original_word, _ = word_parts[word_index]
    lookup_word = lookup_words[word_index]
    if word_index < 2 or leading_punctuation or not lookup_word.isalpha():
        return False
    if lookup_word in _SKIP_ACTIONS or lookup_word.endswith(("maxx", "maxxed", "maxxing")):
        return False
    if lookup_word == "work":
        if _next_word_in_phrase(word_parts, lookup_words, word_index) == "out":
            return False

    cue_index = word_index - 1
    while cue_index > 0 and lookup_words[cue_index] in _ACTION_MODIFIERS:
        if not _phrase_continues(word_parts, cue_index):
            return False
        cue_index -= 1
    if cue_index < 1 or not _phrase_continues(word_parts, cue_index - 1):
        return False

    if not _phrase_continues(word_parts, cue_index):
        return False
    cue = lookup_words[cue_index]
    previous_word = lookup_words[cue_index - 1]
    if cue == "to":
        if previous_word == "going":
            return (
                cue_index >= 2 and _phrase_continues(word_parts, cue_index - 2)
                and lookup_words[cue_index - 2].replace("'", "") in _BE_CUES
                and original_word.islower() and lookup_word not in _DESTINATIONS
            )
        return previous_word in _ACTION_CUES
    if cue in ("will", "should"):
        return previous_word in _SUBJECT_PRONOUNS or previous_word in _PERSON_NOUNS
    if cue == "gonna":
        return previous_word.replace("'", "") in _BE_CUES
    return False


def _slot_swap(words, original_words, next_word):
    first_word = original_words[0]
    last_word = original_words[-1]
    if words[-1] == "over" and words[-2] in _INTENSIFIERS:
        return _IDIOM_SWAPS.get(" ".join(words[:-2] + ["over"]))
    if words[-2:] == ["messed", "up"] and _is_person_subject(first_word):
        modifiers = words[1:-2]
        if not modifiers:
            return f"{first_word} fumbled"
        if len(modifiers) == 1 and modifiers[0] in _INTENSIFIERS:
            return f"{first_word} {original_words[1]} fumbled"
    if words[:3] == ["did", "better", "than"]:
        target = _comparison_target(words[3:], original_words[3:], next_word)
        if target is not None:
            return f"{_MOG_PAST} {target}"
    if len(words) != 4 or not last_word.isalpha():
        return None

    last_lookup = words[-1]
    if words[0] in _LIE_FORMS and words[1] == "about" and words[2] in _POSSESSIVES:
        slot_ends_here = not next_word or next_word in _SLOT_FOLLOWERS
        if slot_ends_here and last_lookup not in _NOUN_CUES:
            fraud_form = _FRAUD_FORMS[_LIE_FORMS.index(words[0])]
            return last_word + fraud_form
    return None


def _person_phrase_swap(words, original_words, next_word, previous_comparison_verb):
    if words[0] == "and" and previous_comparison_verb:
        comparison = _comparative_swap(
            previous_comparison_verb, words[1:], original_words[1:], next_word
        )
        if comparison is not None:
            return f"{original_words[0]} {comparison}", previous_comparison_verb
        return None, None

    subject = original_words[0]
    contraction = _BE_CONTRACTIONS.get(words[0].replace("'", ""))
    if contraction is not None and words[0] not in _BE_VERBS:
        subject_lookup, be_verb = contraction
        if subject_lookup == "it":
            return None, None
        subject = subject[:len(subject_lookup)]
        predicate_index = 1
    elif len(words) >= 3 and words[1] in _BE_VERBS and _is_person_subject(subject):
        be_verb = words[1]
        predicate_index = 2
    else:
        return None, None

    predicate = words[predicate_index:]
    stress_phrase = _stress_swap(subject, predicate, next_word)
    if stress_phrase is not None:
        return stress_phrase, None

    comparison = _comparative_swap(be_verb, predicate, original_words[predicate_index:], next_word)
    if comparison is not None:
        return f"{subject} {comparison}", be_verb
    return None, None


def _stress_swap(subject, predicate, next_word):
    has_intensifier = predicate[0] in _INTENSIFIERS
    state = predicate[1:] if has_intensifier else predicate
    if state not in (
        ["stressed"], ["stressed", "out"], ["stressed", "about"], ["stressed", "out", "about"]
    ):
        return None
    has_topic = state[-1] == "about"
    if not has_topic and next_word and next_word not in _SLOT_FOLLOWERS:
        return None

    possessive = _POSSESSIVE_SUBJECTS.get(subject.lower())
    if possessive is None:
        possessive = subject + ("'" if subject.lower().endswith("s") else "'s")
    emphasis = "really " if has_intensifier else ""
    topic = " over" if has_topic else ""
    return f"{possessive} cortisol {emphasis}spiked{topic}"


def _comparative_swap(be_verb, words, original_words, next_word):
    if not words:
        return None
    adjective_index = 0
    if words[:2] in (["so", "much"], ["a", "lot"]):
        adjective_index = 2
    elif words[0] == "way":
        adjective_index = 1

    if len(words) < adjective_index + 3:
        return None
    dimension = _COMPARISON_DIMENSIONS.get(words[adjective_index])
    if dimension is None or words[adjective_index + 1] != "than":
        return None
    target_index = adjective_index + 2
    target = _comparison_target(words[target_index:], original_words[target_index:], next_word)
    if target is None:
        return None

    mog_verb = _MOG_BASE
    if be_verb == "is":
        mog_verb = _MOG_PRESENT
    elif be_verb in ("was", "were"):
        mog_verb = _MOG_PAST
    emphasis = "giga " if adjective_index else ""
    return f"{emphasis}{dimension}{mog_verb} {target}"


def _comparison_target(words, original_words, next_word):
    if next_word in _BE_VERBS:
        return None
    if words == ["everyone"]:
        return "the whole lobby"
    if len(words) == 1:
        if words[0] == "her" and next_word and next_word not in _COMPARISON_FOLLOWERS:
            return None
        if words[0] in _OBJECT_PRONOUNS or _looks_like_name(original_words[0]):
            return original_words[0]
    if len(words) == 2 and words[0] in _POSSESSIVES and words[1] in _PERSON_NOUNS:
        return " ".join(original_words)
    return None


def _adjective_swap(words, original_words, next_word):
    adjective = words[-1]
    if adjective not in _ADJECTIVE_SWAPS or (next_word and next_word not in _ADJECTIVE_FOLLOWERS):
        return None

    prefix = []
    adjective_index = 0
    if words[0].replace("'", "") in _BE_CUES or words[0] in _ADJECTIVE_CUES:
        prefix.append(original_words[0])
        adjective_index += 1
    if words[adjective_index] in _INTENSIFIER_SWAPS:
        prefix.append(_INTENSIFIER_SWAPS[words[adjective_index]])
        adjective_index += 1
    if adjective_index == len(words) - 1 and prefix:
        return " ".join(prefix + [_ADJECTIVE_SWAPS[adjective]])
    return None
