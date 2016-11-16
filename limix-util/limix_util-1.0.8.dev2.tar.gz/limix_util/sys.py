from __future__ import absolute_import
from sys import platform as _platform

def platform():
    """Returns whether it is running on `linux`, `osx`, or `win`."""
    if _platform == "linux" or _platform == "linux2":
        return 'linux'
    elif _platform == "darwin":
        return 'osx'
    elif _platform == "win32":
        return 'win'
    return 'unknown'
