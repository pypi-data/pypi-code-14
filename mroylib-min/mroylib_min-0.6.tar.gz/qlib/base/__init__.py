from os import getenv as __getenv
from os.path import join as J

HOME = __getenv("HOME")
SHELL = __getenv("SHELL").split("/").pop()
__all__ = [
    'HOME',
    'J',
    'SHELL',
]