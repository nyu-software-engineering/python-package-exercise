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

    translated_words = []
    made_swap = False
    for token in text.split():
        leading_punctuation, word, trailing_punctuation = _split_punctuation(token)
        lookup_word = word.lower()
        if lookup_word in _WORD_SWAPS:
            replacement = _WORD_SWAPS[lookup_word]
            if word[0].isupper():
                replacement = replacement.capitalize()
            word = replacement
            made_swap = True

        translated_words.append(f"{leading_punctuation}{word}{trailing_punctuation}")

    if not made_swap:
        return text

    return " ".join(translated_words)
