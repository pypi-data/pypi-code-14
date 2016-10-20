"""
    list
    ~~~~~~~~~~~~~

    A set of various list helpers.

    :copyright: (c) 2016 by Dusty Gamble.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '1.0'



def listify(obj):
    # Because None is used for specific functionality (auto-filling defaults),
    # preserve it.
    if obj is None:
        return None

    if type(obj) is str:
        obj = [obj, ]

    try:
        assert hasattr(obj, '__len__')
        assert obj.__len__
    except AssertionError:
        obj = [obj, ]

    return obj
