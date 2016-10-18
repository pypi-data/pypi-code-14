# -*- coding: utf-8 -*-

"""
Custom exceptions for j1bz.expression package.

ParseError and ParserGenerationError are both used as wrappers respectively
for GrakoParseError and GrakoError exceptions family. Thus, it is possible to
use this package without bothering about Grako.
"""


class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParserGenerationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
