from os import getenv as __getenv
from os.path import join as J

HOME = __getenv("HOME")

__all__ = [
    'HOME',
    'J',
]