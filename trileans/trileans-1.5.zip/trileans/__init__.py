from types import *
from enum import Enum

class TrileanValue(Enum):
    False = 0
    True = 1
    Tri = 2

class trilean:
    def __init__ (self, x, y=None, z=None):
        if type(x) is IntType:
            if x <= 2:
                self.value = x
                self.table = Trilean.createTable(x)
                self.embedded = y
            else:
                raise ValueError("Error: Trilean values must range from 0 to 2")
        elif type(x) is BooleanType:
            if type(y) is BooleanType:
                self.value = Trilean.Parse(x, y)
                self.table = Trilean.createTable(self.value)
                self.embedded = z
            else:
                self.value = Trilean.Parse(x)
                self.table = Trilean.createTable(self.value)
                self.embedded = y
        elif type(x) is StringType:
            self.value = Trilean.Parse(x)
            self.table = Trilean.createTable(self.value)
            self.embedded = y
        else:
            raise ValueError("Invalid argument type. Type of first argument must either be number, boolean, or string. Type of second object must either be boolean or desired embedded object (for all patterns other than bool, bool, embedded). Type of third object must be desired embedded object (for pattern bool, bool, embedded)")

class Trilean:
    @staticmethod
    def Parse(x, y = False):
        if type(x) is BooleanType:
            if y is True:
                return TrileanValue.Tri
            elif x is True:
                return TrileanValue.True
            else:
                return TrileanValue.False
        elif type(x) is StringType:
            if x is "False" or x is "0" or x is "false":
                return TrileanValue.False
            elif x is "True" or x is "1" or x is "true":
                return TrileanValue.True
            elif x is "Tri" or x is "2" or x is "tri":
                return TrileanValue.Tri
            else:
                raise ValueError("Error: Invalid argument at position 0")
        else:
            raise ValueError("Error: Invalid argument at position 0")
    @staticmethod
    def createTable(x):
        if type(x) is IntType:
            if x is TrileanValue.False:
                return [False, False]
            elif x is TrileanValue.True:
                return [True, False]
            elif x is TrileanValue.Tri:
                return [False, True]
            else:
                raise ValueError("Error: Invalid argument at position 0")
        else:
            raise ValueError("Error: Invalid argument at position 0")