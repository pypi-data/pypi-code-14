from .__file import to_save, call_vim, file_search, fzip, zip_64

__all__ = [
    'to_save',
    'call_vim',
    'file_search',
    'j',
    'fzip',
    'zip_64'
]


def j(*paths):
    import os
    from functools import reduce
    return reduce(os.path.join, paths)