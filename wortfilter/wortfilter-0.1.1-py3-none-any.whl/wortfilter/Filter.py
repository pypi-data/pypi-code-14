from typing import Sequence


def filter(wordList: Sequence[str], allowedLetters: str) -> Sequence[str]:
    return [word for word in wordList if all(letter in allowedLetters for letter in word)]
