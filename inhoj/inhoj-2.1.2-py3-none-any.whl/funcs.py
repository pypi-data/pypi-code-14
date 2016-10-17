from functools import reduce


def getn(dictionary, *keys, fallback=None):
    """

    How to use:
        from inhoj.funcs import getn

        getn(m, "key1", "key2", "key3")
    """

    for key in keys:
        if key not in dictionary:
            return fallback
        dictionary = dictionary[key]
    return dictionary


def getni(dictionary, keys, fallback=None):
    keys = keys.split('.')
    return getn(dictionary, *keys, fallback=fallback)
