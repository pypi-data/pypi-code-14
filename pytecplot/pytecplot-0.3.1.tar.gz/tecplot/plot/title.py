from builtins import super

from ..constant import *
from .. import session
from ..tecutil import sv
from .font import Font


class AxisTitle(session.Style):
    def __init__(self, axis):
        self.axis = axis
        super().__init__(axis._sv, sv.TITLE, **axis._style_attrs)

    @property
    def show_on_axis(self):
        return self._get_style(bool, sv.SHOWONAXISLINE)

    @show_on_axis.setter
    def show_on_axis(self, show):
        self._set_style(bool(show), sv.SHOWONAXISLINE)

    @property
    def color(self):
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def font(self):
        return Font(self)

    @property
    def offset(self):
        return self._get_style(float, sv.OFFSET)

    @offset.setter
    def offset(self, value):
        self._set_style(float(value), sv.OFFSET)

    @property
    def position(self):
        return self._get_style(float, sv.PERCENTALONGLINE)

    @position.setter
    def position(self, value):
        self._set_style(float(value), sv.PERCENTALONGLINE)

    @property
    def text(self):
        return self._get_style(float, sv.TEXT)

    @text.setter
    def text(self, value):
        self._set_style(float(value), sv.TEXT)


class Axis2DTitle(AxisTitle):
    @property
    def show_on_border_min(self):
        return self._get_style(bool, sv.SHOWONGRIDBORDERMIN)

    @show_on_border_min.setter
    def show_on_border_min(self, value):
        self._set_style(bool(value), sv.SHOWONGRIDBORDERMIN)

    @property
    def show_on_border_max(self):
        return self._get_style(bool, sv.SHOWONGRIDBORDERMAX)

    @show_on_border_max.setter
    def show_on_border_max(self, value):
        self._set_style(bool(value), sv.SHOWONGRIDBORDERMAX)


class Axis3DTitle(AxisTitle):
    @property
    def opposite_edge(self):
        return self._get_style(bool, sv.SHOWONOPPOSITEEDGE)

    @opposite_edge.setter
    def opposite_edge(self, value):
        self._set_style(bool(value), sv.SHOWONOPPOSITEEDGE)


class DataAxisTitle(AxisTitle):
    @property
    def text(self):
        title_mode = self._get_style(AxisTitleMode, sv.TITLEMODE)
        if title_mode is AxisTitleMode.UseText:
            return self._get_style(str, sv.TEXT)
        else:
            return title_mode

    @text.setter
    def text(self, value):
        if value is None:
            self._set_style(AxisTitleMode.NoTitle, sv.TITLEMODE)
        elif value is AxisTitleMode.UseVarName:
            self._set_style(AxisTitleMode.UseVarName, sv.TITLEMODE)
        else:
            self._set_style(AxisTitleMode.UseText, sv.TITLEMODE)
            self._set_style(str(value), sv.TEXT)


class DataAxis2DTitle(DataAxisTitle, Axis2DTitle):
    pass


class DataAxis3DTitle(DataAxisTitle, Axis3DTitle):
    pass


class RadialAxisTitle(DataAxis2DTitle):
    @property
    def show_on_all_radial_axes(self):
        return self._get_style(bool, sv.SHOWONALLAXES)

    @show_on_all_radial_axes.setter
    def show_on_all_radial_axes(self, value):
        self._set_style(bool(value), sv.SHOWONALLAXES)
