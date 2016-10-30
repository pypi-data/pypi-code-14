# -*- coding: utf-8 -*-


class MissingArgumentException(Exception):
    """
    >>> exception = MissingArgumentException("1st argument")
    >>> exception.__str__()
    'Missing value for \"1st argument\"'
    """
    def __init__(self, arg):
        self.argument = arg

    def __str__(self):
        return "Missing value for \"" + self.argument + "\""
