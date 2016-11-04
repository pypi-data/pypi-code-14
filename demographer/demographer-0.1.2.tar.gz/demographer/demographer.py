from abc import ABCMeta, abstractmethod

class Demographer(object):
    """An abstract base class for *demographers* that identify demographic characteristics of authors from a tweet."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_tweet(self, tweet):
        """Return a dictionary containing a classification for this tweet"""
        pass