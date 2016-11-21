import re

_VERTEX_KEY_PATTERN = re.compile(r"^[^:=]+$")  # All characters except : and =


class ReadOnlyDict(dict):
    def __init__(self, dict_to_protect=None):
        super(ReadOnlyDict, self).__init__(dict_to_protect)

    def __setitem__(self, key, value):
        raise TypeError("__setitem__ is not permitted")

    def __delitem__(self, key):
        raise TypeError("__delitem__ is not permitted")

    def update(self, other=None, **kwargs):
        raise TypeError("update is not permitted")


def check_key(k):
    assert _VERTEX_KEY_PATTERN.match(k), "Invalid format '{}'. Characters ':' and '=' are not allowed"


def check_keys(keys):
    """
    Given a dict of keys, make sure they follow the required pattern and constraints

    :param dict[str, str] keys:
    """
    assert keys and isinstance(keys, dict) and len(keys) > 0, "Keys are mandatory (non empty dict)"

    for k, v in keys.iteritems():
        check_key(k)
        check_key(v)

    # Make sure values are unique
    assert len(set(keys.viewvalues())) == len(keys), "Same value for more than one key"
