"""Implementation of a Markov chain."""
import random


class MarkovChain:
    """Markov chain."""

    def __init__(self, words, size):
        """Initialize Markov chain with a list of words and a size.

        :param words: List of words
        :type words: list
        :param size: Letters that need to match
        :type size: int
        """
        self.size = size
        self.starts = map(lambda word: word[:self.size], words)
        self.lookup = self._buildLookupTable(words)

    def _buildLookupTable(self, words):
        lookup = {}
        for word in words:
            for key, val in self._tuples(word):
                if key in lookup:
                    lookup[key].append(val)

                else:
                    lookup[key] = [val]

        return lookup

    def _tuples(self, word):
        word = word.strip()
        if len(word) >= self.size:
            word = word + "\n"
            for i in range(len(word) - self.size):
                yield(word[i:i + self.size], word[i + self.size])

    def getWord(self):
        """Get a word.

        :returns: A generated word
        :rtype: str
        """
        key = random.choice(self.starts)
        word = key
        try:
            next = random.choice(self.lookup[key])
            while next != "\n":
                word = word + next
                key = key[1:] + next
                next = random.choice(self.lookup[key])
        except KeyError:
            pass

        return word
