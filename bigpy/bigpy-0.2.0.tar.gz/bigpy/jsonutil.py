"""
A collection of useful JSON-related utilities.
"""
import numbers


def remove_empty_keys(d):
    """
    Deletes empty keys from the dictionary, recursively.
    The "empty" key is any key associated with the value
    that evaluates to `False`, e.g. `None`, empty string,
    empty list, etc.

    :param d: the dictionary or a list of dictionaries to "clean up".
    :type d: dict or list
    :return: the same dictionary or the list of dictionaries, with blank entries removed.
    """
    if isinstance(d, list):
        # if we have a list here, look for other lists and dictionaries
        # and clean them recursively
        for item in d:
            remove_empty_keys(item)
            # if the resulting item is empty after the cleanup, remove it
            if not item:
                d.remove(item)
    elif isinstance(d, dict):

        for key, value in d.items():
            # leave numbers out
            if isinstance(value, numbers.Number):
                continue

            # we are concerned with three cases here:
            #
            #   1. An empty value - we remove that key
            #   2. Another dictionary or list of dictionaries - we clean it up recursively
            #      (and remove it, if it is empty after the cleanup)
            #
            if not value:
                # case (1) - empty value
                del d[key]
            elif isinstance(value, (dict, list)):
                # case (2) - another dictionary or a list of dictionaries
                remove_empty_keys(value)
                # if we have removed all keys and that dictionary or list is now empty, remove it as well
                if not value:
                    del d[key]
    return d

