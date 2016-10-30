# -*- coding: utf-8 -*-


class InputArgument:
    """
    """

    ARGUMENT_REQUIRED = 1
    ARGUMENT_OPTIONAL = '?'

    def __init__(self, argumentName, description, mode=ARGUMENT_REQUIRED, defaultValue=None, type_=str):
        self.name = argumentName
        self.value = defaultValue
        self.description = description
        self.type = type_
        self.mode = mode

    def setValue(self, value):
        self.value = value

    def __str__(self):
            return "<" + self.name + ">"

    def __repr__(self):
        return self.__str__()
