from builtins import super

from ..tecutil import Index, log_setattr, sv
from .. import session
from ..exception import *

@log_setattr
class Ticks(object):
    def __init__(self, axis):
        self.axis = axis
        self._sv = axis._sv + [sv.TICKS]

@log_setattr
class TickLabels(object):
    def __init__(self, axis):
        self.axis = axis
        self._sv = axis._sv + [sv.TICKLABEL]
