from typing import Sequence
import re
from wortfilter import Filter


def normalizeAllowedLetters(allowedLetters: str) -> str:
    return allowedLetters.lower() + allowedLetters.upper()

def normalizeWordList(wordList: str) -> Sequence[str]:
    assert isinstance(wordList, str)
    words = re.split('[^\wäöüÄÖÜß]+', wordList)
    sortedList = sorted(words)
    for i in reversed(range(len(sortedList)-1)):
        if sortedList[i] == sortedList[i+1]:
            del sortedList[i+1]
    while sortedList[0] == "":
        del sortedList[0]
    return sortedList

def filter(wordList: str, allowedLetters: str) -> str:
    normalizedAllowedLetters = normalizeAllowedLetters(allowedLetters)
    normalizedWordList = normalizeWordList(wordList)
    filteredWordList = Filter.filter(normalizedWordList, normalizedAllowedLetters)
    return "\n".join(filteredWordList)
