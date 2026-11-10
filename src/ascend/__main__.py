import argparse
import sys

from .translator import translate_sentence

def main():
    parser = argparse.ArgumentParser(description="Translate text into BP slang.")
    parser.add_argument("text", nargs="*", help="Text to translate")
    args = parser.parse_args()

    text = " ".join(args.text) if args.text else sys.stdin.read()
    translated = translate_sentence(text)
    if translated is None:
        parser.error("provide non-empty text to translate")

    print(translated)

if __name__ == "__main__":
    main()