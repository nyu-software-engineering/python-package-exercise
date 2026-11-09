_PUNCTUATION = ".,!?;:()[]{}\"'“”‘’…—"
_MAX_PHRASE_WORDS = 5

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
    "encouraging news": "hopefuel",
    "just pretending": "just larping",
    "an average person": "a normie",
    "average person": "normie",
    "average people": "normies",
    "normal person": "normie",
    "very handsome guy": "chad",
}

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
}

_VERB_FORM_EXCEPTIONS = {
    "get": ("gets", "got", "getting"),
    "lie": ("lies", "lied", "lying"),
    "make": ("makes", "made", "making"),
    "mog": ("mogs", "mogged", "mogging"),
    "study": ("studies", "studied", "studying"),
}
_VERB_ALIASES = {"outshone": "outshined"}

_INTENSIFIERS = ("really", "so", "very")

_SUBJECT_PRONOUNS = ("i", "you", "he", "she", "it", "we", "they")
_POSSESSIVE_SUBJECTS = {
    "i": "my", "you": "your", "he": "his", "she": "her", "we": "our", "they": "their",
}
_POSSESSIVES = tuple(_POSSESSIVE_SUBJECTS.values())
_NOUN_CUES = ("a", "an", "the", "this", "that", "these", "those") + _POSSESSIVES
_PERSON_NOUNS = (
    "brother", "sister", "friend", "friends", "mom", "dad", "parents", "teacher",
    "coach", "teammate", "teammates", "student", "students", "kids", "people", "guy",
)
_OBJECT_PRONOUNS = ("me", "you", "him", "her", "us", "them")
_NONPERSON_WORDS = (
    "it", "that", "this", "things", "everything", "something", "nothing", "plan", "plans",
    "expected", "usual", "normal", "average", "before", "ever", "yesterday", "today", "brakes",
)

_BE_VERBS = ("am", "is", "are", "was", "were")
_SLOT_FOLLOWERS = ("again", "and", "before", "but", "because", "since", "to", "today", "yesterday")
_COMPARISON_FOLLOWERS = _SLOT_FOLLOWERS + ("at", "in", "on", "now", "too", "though")

_ACTION_MODIFIERS = ("carefully", "just", "quickly", "quietly", "really", "slowly")
_SKIP_ACTIONS = ("be", "have", "do", "not", "never")


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
_LIE_FORMS = _verb_forms("lie")
_FRAUD_FORMS = _verb_forms("fraud")
_MOG_PAST = _verb_forms("mog")[2]
_ACTION_CUES = (
    "try", "tries", "tried", "trying",
    "want", "wants", "wanted",
    "need", "needs", "needed",
    "plan", "plans", "planned", "planning",
)


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


def _can_maxx_action(word_parts, word_index, lookup_word):
    leading_punctuation, _, _ = word_parts[word_index]
    if word_index < 2 or leading_punctuation or not lookup_word.isalpha():
        return False
    if lookup_word in _SKIP_ACTIONS or lookup_word in _ACTION_MODIFIERS:
        return False
    if lookup_word.endswith(("maxx", "maxxed", "maxxing")):
        return False

    to_index = word_index - 1
    modifier_start, modifier, modifier_end = word_parts[to_index]
    if modifier.lower() in _ACTION_MODIFIERS and not (modifier_start or modifier_end):
        to_index -= 1
    if to_index < 1:
        return False

    _, cue, cue_end = word_parts[to_index - 1]
    to_start, to_word, to_end = word_parts[to_index]
    return (
        cue.lower() in _ACTION_CUES
        and to_word.lower() == "to"
        and not (cue_end or to_start or to_end)
    )


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


def _verb_phrase_swap(phrase, word_parts, lookup_words, start_index, end_index):
    replacement = _VERB_SWAPS.get(phrase)
    if replacement is None:
        return None
    if phrase in ("study", "studies"):
        if not _study_is_an_action(word_parts, lookup_words, start_index):
            return None
    return replacement


def _find_swap(word_parts, lookup_words, start_index):
    replacement = None
    matched_word_count = 1
    words = []
    original_words = []
    phrase_limit = min(start_index + _MAX_PHRASE_WORDS, len(word_parts))

    for end_index in range(start_index, phrase_limit):
        if end_index > start_index and not _phrase_continues(word_parts, end_index - 1):
            break
        words.append(lookup_words[end_index])
        original_words.append(word_parts[end_index][1])
        phrase = " ".join(words)
        candidate = _IDIOM_SWAPS.get(phrase)

        if candidate is None:
            candidate = _verb_phrase_swap(phrase, word_parts, lookup_words, start_index, end_index)

        if candidate is None and len(words) >= 2:
            next_word = _next_word_in_phrase(word_parts, lookup_words, end_index)
            if len(words) >= 3:
                candidate = _slot_swap(words, original_words, next_word)

        if candidate is not None:
            replacement = candidate
            matched_word_count = len(words)

    return replacement, matched_word_count


def translate_sentence(text):
    """Rewrite matching text in BP slang and return None for invalid input."""
    if not isinstance(text, str) or not text.strip():
        return None

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
    while word_index < len(word_parts):
        leading_punctuation, word, trailing_punctuation = word_parts[word_index]
        replacement, matched_word_count = _find_swap(word_parts, lookup_words, word_index)

        if replacement is None and _can_maxx_action(word_parts, word_index, lookup_words[word_index]):
            replacement = lookup_words[word_index] + "maxx"

        if replacement is not None:
            last_index = word_index + matched_word_count - 1
            if word[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            word = replacement
            trailing_punctuation = word_parts[last_index][2]
            made_swap = True

        translated_words.append(f"{leading_punctuation}{word}{trailing_punctuation}")
        word_index += matched_word_count

    if not made_swap:
        return text

    return " ".join(translated_words)
