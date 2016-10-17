# -*- coding: utf-8 -*-


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
