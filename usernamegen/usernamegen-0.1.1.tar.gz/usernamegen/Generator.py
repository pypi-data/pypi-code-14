"""Wordlist based Markov chain username generator."""
from MarkovChain import MarkovChain
import random


class Generator():
    """Generates random usernames based on a wordlist and formatters."""

    def __init__(self, words, size, min):
        """Initialize Markov chain with a list of words and a size.

        :param words: List of words
        :type words: list
        :param size: Letters that need to match
        :type size: int
        :param min: Minimum username length
        :type min: int
        """
        self.size = size
        self.min = min
        self.formatters = []

        self.markov = MarkovChain(words, size)

    def getWords(self):
        """Return randomly generated words.

        :return: Letters that need to match
        :rtype size: list
        """
        words = []
        length = 0
        while length < self.min:
            word = self.markov.getWord()
            words.append(word)
            length += len(word)

        return words

    def setFormatters(self, formatters):
        """Set the formatters.

        :param formatters: List of formatters and their weight
        :type formatters: list
        """
        self.formatters = []
        for i in range(0, len(formatters)):
            formatter = formatters[i]
            for j in range(0, formatter['weight']):
                self.formatters.append(formatter['format'])

    def getString(self):
        """Return a randomly generated username.

        :return: Randomly generated username
        :rtype size: str
        """
        words = self.getWords()

        try:
            formatter = random.choice(self.formatters)
        except IndexError:
            raise Exception('At least one formatter needs to be provided')

        return formatter().format(words)
