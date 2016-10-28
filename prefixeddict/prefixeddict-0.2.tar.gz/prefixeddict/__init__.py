try:
    from itertools import izip
    lazyzip = izip
except ImportError:
    lazyzip = zip


class PrefixedDict(object):
    """
    Prefixed dictionary, makes all keys be automatically prefixed with a given
    prefix.
    """

    def __init__(self, prefix, dictionary):
        """
        Args:
            prefix (str): the prefix you want to apply to the dictionary's
                          keys.
            dictionary (dict-like): the actual dictionary-like object which
                                    will be used to store data.
        """

        self.dictionary = dictionary
        self.prefix = prefix

    def __setitem__(self, key, value):
        self.dictionary[self.prefix + '-' + key] = value

    def __getitem__(self, key):
        return self.dictionary[self.prefix + '-' + key]

    def __contains__(self, key):
        return (self.prefix + '-' + key) in self.dictionary

    def keys(self):
        for key in self.dictionary.keys():
            if key.startswith(self.prefix + '-'):
                yield key.replace(self.prefix + '-', '')

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        return lazyzip(self.keys(), self.values())

    __iter__ = keys
