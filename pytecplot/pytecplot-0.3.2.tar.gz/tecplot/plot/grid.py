from .. import session
from ..tecutil import log_setattr, sv


class GridArea(session.Style):
    def __init__(self, axes):
        self.axes = axes
        super().__init__(axes._sv, sv.GRIDAREA, **axis._style_attrs)


class PreciseGrid(session.Style):
    def __init__(self, axes):
        self.axes = axes
        super().__init__(axes._sv, sv.PRECISEGRID, **axis._style_attrs)


class GridLinesStyle(session.Style):
    def __init__(self, axis, *svargs):
        super().__init__(axis._sv, *svargs, **axis._style_attrs)


class GridLines(GridLinesStyle):
    def __init__(self, axis):
        super().__init__(axis, sv.GRIDLINES)


class MinorGridLines(GridLinesStyle):
    def __init__(self, axis):
        super().__init__(axis, sv.MINORGRIDLINES)
