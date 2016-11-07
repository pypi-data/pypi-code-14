"""
aiopixiv - an async way to access the pixiv API.
"""

from aiopixiv.wrapper import BaseAPI, PixivError, PixivAuthFailed
from aiopixiv.v5 import PixivAPIv5

__version__ = "1.0.0"
__author__ = "Isaac Dickinson"

__all__ = ("PixivError", "PixivAuthFailed", "PixivAPIv5")
