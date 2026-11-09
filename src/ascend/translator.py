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
}

_PHRASE_SWAPS = {
    "work out": "gymmaxx",
    "worked out": "gymmaxxed",
    "working out": "gymmaxxing",
    "glow up": "ascend",
    "glowed up": "ascended",
    "glowing up": "ascending",
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
    "it's over": "its so over",
    "never started": "never began",
    "everything is ruined": "everything is kirked",
}
_MAX_PHRASE_WORDS = 3

def _split_punctuation(token):
    without_leading = token.lstrip(_PUNCTUATION)
    word = without_leading.rstrip(_PUNCTUATION)
    leading_punctuation = token[:len(token) - len(without_leading)]
    trailing_punctuation = without_leading[len(word):]
    return leading_punctuation, word, trailing_punctuation


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
