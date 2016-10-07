from builtins import super

from .. import session
from ..tecutil import sv


class Font(session.Style):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent._sv, sv.TEXTSHAPE, **parent._style_attrs)

    @property
    def bold(self):
        return self._get_style(bool, sv.ISBOLD)

    @bold.setter
    def bold(self, value):
        self._set_style(bool(value), sv.ISBOLD)

    @property
    def italic(self):
        return self._get_style(bool, sv.ISITALIC)

    @italic.setter
    def italic(self, value):
        self._set_style(bool(value), sv.ISITALIC)

    @property
    def size(self):
        return self._get_style(float, sv.HEIGHT)

    @size.setter
    def size(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def size_units(self):
        return self._get_style(Units, sv.SIZEUNITS)

    @size_units.setter
    def size_units(self, value):
        self._set_style(Units(value), sv.SIZEUNITS)

    @property
    def typeface(self):
        return self._get_style(Font, sv.FONTFAMILY)

    @typeface.setter
    def typeface(self, value):
        self._set_style(Font(value), sv.FONTFAMILY)
