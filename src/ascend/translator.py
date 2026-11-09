_PUNCTUATION = ".,!?;:()[]{}\"'“”‘’…—"

_WORD_SWAPS = {
    "studied": "studymaxxed",
    "studying": "studymaxxing",
    "improve": "ascend",
    "improves": "ascends",
    "improved": "ascended",
    "improving": "ascending",
    "outshine": "mog",
    "outshines": "mogs",
    "outshined": "mogged",
    "outshining": "mogging",
    "femoid": "foid",
    "femoids": "foids",
}

_PHRASE_SWAPS = {
    "work out": "gymmaxx",
    "worked out": "gymmaxxed",
    "working out": "gymmaxxing",
    "glow up": "ascend",
    "glowed up": "ascended",
    "glowing up": "ascending",
    "get better": "ascend",
    "got better": "ascended",
    "getting better": "ascending",
    "study for": "studymaxx for",
    "make excuses": "cope",
    "made excuses": "coped",
    "making excuses": "coping",
    "an excuse": "pure cope",
    "big setback": "brutal failo",
    "weak spot": "failo",
    "standout feature": "halo",
    "major improvement": "massive ascension",
    "small improvement": "softmaxxing gain",
    "outshined everyone": "mogged the whole lobby",
    "beat everyone": "mogged the whole lobby",
    "did better than everyone": "mogged the whole lobby",
    "did better than me": "mogged me",
    "did better than you": "mogged you",
    "did better than him": "mogged him",
    "did better than her": "mogged her",
    "did better than us": "mogged us",
    "did better than them": "mogged them",
    "made a mistake": "fumbled",
    "i messed up": "i fumbled",
    "we messed up": "we fumbled",
    "it's over": "its jover",
    "it's so over": "its jover",
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
    "faking height": "heightfrauding",
    "lying about my height": "heightfrauding",
    "just pretending": "just larping",
    "making stuff up": "larping",
    "an average person": "a normie",
    "average person": "normie",
    "average people": "normies",
    "normal person": "normie",
    "very handsome guy": "chad",
}
_MAX_PHRASE_WORDS = 4

_ACTION_CUES = (
    "try", "tries", "tried", "trying",
    "want", "wants", "wanted",
    "need", "needs", "needed",
    "plan", "plans", "planned", "planning",
)
_ACTION_MODIFIERS = ("carefully", "just", "quickly", "quietly", "really", "slowly")
_SKIP_ACTIONS = ("be", "have", "do", "not", "never")


def _split_punctuation(token):
    without_leading = token.lstrip(_PUNCTUATION)
    word = without_leading.rstrip(_PUNCTUATION)
    leading_punctuation = token[:len(token) - len(without_leading)]
    trailing_punctuation = without_leading[len(word):]
    return leading_punctuation, word, trailing_punctuation


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


def translate_sentence(text):
    """Rewrite matching text in BP slang and return None for invalid input."""
    if not isinstance(text, str) or not text.strip():
        return None

    word_parts = []
    for token in text.split():
        word_parts.append(_split_punctuation(token))

    translated_words = []
    made_swap = False
    word_index = 0
    while word_index < len(word_parts):
        leading_punctuation, word, trailing_punctuation = word_parts[word_index]
        lookup_word = word.lower()
        replacement = None
        matched_word_count = 1

        phrase = lookup_word
        phrase_trailing_punctuation = trailing_punctuation
        phrase_limit = min(word_index + _MAX_PHRASE_WORDS, len(word_parts))
        for next_index in range(word_index + 1, phrase_limit):
            next_leading, next_word, next_trailing = word_parts[next_index]
            if phrase_trailing_punctuation or next_leading:
                break
            phrase = f"{phrase} {next_word.lower()}"
            phrase_trailing_punctuation = next_trailing
            lookup_phrase = phrase.replace("’", "'")
            if lookup_phrase in _PHRASE_SWAPS:
                replacement = _PHRASE_SWAPS[lookup_phrase]
                trailing_punctuation = next_trailing
                matched_word_count = next_index - word_index + 1

        if replacement is None and lookup_word in _WORD_SWAPS:
            replacement = _WORD_SWAPS[lookup_word]

        if replacement is None and _can_maxx_action(word_parts, word_index, lookup_word):
            replacement = f"{lookup_word}maxx"

        if replacement is not None:
            if word[0].isupper():
                replacement = replacement.capitalize()
            word = replacement
            made_swap = True

        translated_words.append(f"{leading_punctuation}{word}{trailing_punctuation}")
        word_index += matched_word_count

    if not made_swap:
        return text

    return " ".join(translated_words)
