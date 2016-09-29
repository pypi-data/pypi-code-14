from types import *
from enum import Enum

class TrileanValue(Enum):
    false = 0
    true = 1
    tri = 2

class trilean:
    def __init__ (self, x, y=None, z=None):
        if isinstance(x, bool):
            if isinstance(y, bool):
                self.value = Trilean.Parse(x, y)
                self.table = Trilean.createTable(self.value)
                self.embedded = z
            else:
                self.value = Trilean.Parse(x)
                self.table = Trilean.createTable(self.value)
                self.embedded = y
        elif isinstance(x, int):
            if x <= 2:
                self.value = x
                self.table = Trilean.createTable(x)
                self.embedded = y
            else:
                raise ValueError("Error: Trilean values must range from 0 to 2")
        elif isinstance(x, TrileanValue):
            self.value = x.value
            self.table = Trilean.createTable(x)
            self.embedded = y
        elif isinstance(x, str):
            self.value = Trilean.Parse(x)
            self.table = Trilean.createTable(self.value)
            self.embedded = y
        else:
            raise ValueError("Invalid argument type. Type of first argument must either be number, boolean, or string. Type of second object must either be boolean or desired embedded object (for all patterns other than bool, bool, embedded). Type of third object must be desired embedded object (for pattern bool, bool, embedded)")

class Trilean:
    @staticmethod
    def Parse(x, y = False):
        if isinstance(x, bool):
            if y is True:
                return TrileanValue.tri.value
            elif x is True:
                return TrileanValue.true.value
            else:
                return TrileanValue.false.value
        elif isinstance(x, str):
            if x is "False" or x is "0" or x is "false":
                return TrileanValue.false.value
            elif x is "True" or x is "1" or x is "true":
                return TrileanValue.true.value
            elif x is "Tri" or x is "2" or x is "tri":
                return TrileanValue.tri.value
            else:
                raise ValueError("Error: Invalid argument at position 0")
        else:
            raise ValueError("Error: Invalid argument at position 0")
    @staticmethod
    def createTable(x):
        if isinstance(x, int) or isinstance(x, TrileanValue):
            if x is TrileanValue.false or x is TrileanValue.false.value:
                return [False, False]
            elif x is TrileanValue.true or x is TrileanValue.true.value:
                return [True, False]
            elif x is TrileanValue.tri or x is TrileanValue.tri.value:
                return [False, True]
            else:
                raise ValueError("Error: Invalid argument at position 0")
        else:
            raise ValueError("Error: Invalid argument at position 0")
