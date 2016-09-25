"""
Format list of strings.

Formatters take a list of words, format them some way and return a string.
"""

from abc import ABCMeta, abstractmethod, abstractproperty
import random


class Formatter:
    """Formatter base class."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def _transform(self, words):
        """Transform a list of strings.

        Every formatter needs to implement this method. The returned list may
        not have the same length as the source list.

        :param words: List of words
        :type words: list

        :returns: List of transformed words
        :rtype: list
        """
        raise NotImplementedError

    def format(self, words):
        """Transform and join the words.

        :param words: List of words
        :type words: list

        :returns: List of transformed words
        :rtype: str
        """
        return ''.join(self._transform(words))


class Join(Formatter):
    """Simply join all words."""

    def _transform(self, words):
        return words


class Underscore(Formatter):
    """Join with underscore."""

    def _transform(self, words):
        return list(''.join(l + '_' * (n < len(words) - 1)
                    for n, l in enumerate(words)))


class Capitalize(Formatter):
    """Capitalize first letter of every word."""

    def _transform(self, words):
        return map(lambda word: word.capitalize(), words)


class CapitalizeExceptFirst(Formatter):
    """Capitalize first letter of every word except the first."""

    def _transform(self, words):
        words = Capitalize()._transform(words)
        words[0] = words[0][:1].lower() + words[0][1:]
        return words


class AppendNumber(Formatter):
    """Append a number.

    If the last word is of length 4,then a year like number is appended,
    otherwise a number of up to 3 digits will be apended.
    """

    def _transform(self, words):
        last = words.pop()
        if len(last) is 4:
            words.append(str(random.randint(1600, 2300)))
        else:
            words.append(last)
            words.append(str(random.randint(0, 999)))

        return words


class CapitalizeAppendNumber(Formatter):
    """Capitalizes all words and appends a number."""

    def _transform(self, words):
        words = Capitalize()._transform(words)
        words = AppendNumber()._transform(words)
        return words
