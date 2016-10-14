from typing import Sequence
import re
from wortfilter import Filter


def normalizeAllowedLetters(allowedLetters: str) -> str:
    return allowedLetters.lower() + allowedLetters.upper()

def normalizeWordList(wordList: str) -> Sequence[str]:
    wordList = re.sub(r"[^a-zA-Zäöüß]", " ", wordList) # replace all invalid characters with space
    wordList = re.sub(r"\s+", "\n", wordList) # one word per line, contract multiple whitespaces
    wordListSeq = [word for word in wordList.split('\n') if word != ""] # split into list and remove empty lines
    return sorted(set(wordListSeq)) # remove duplicates

def filter(wordList: str, allowedLetters: str) -> str:
    normalizedAllowedLetters = normalizeAllowedLetters(allowedLetters)
    normalizedWordList = normalizeWordList(wordList)
    filteredWordList = Filter.filter(normalizedWordList, normalizedAllowedLetters)
    return "\n".join(filteredWordList)
