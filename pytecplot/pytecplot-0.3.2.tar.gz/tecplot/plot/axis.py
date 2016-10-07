from builtins import super

from six import string_types

from ..constant import *
from ..exception import *
from .. import session
from ..tecutil import Index, log_setattr, sv
from .grid import GridLines, MinorGridLines
from .ticks import TickLabels, Ticks
from .title import (Axis2DTitle, DataAxis2DTitle, DataAxis3DTitle,
                    RadialAxisTitle)


class Axis(session.Style):
    def __init__(self, axes, name, **kwargs):
        self.axes = axes
        self.name = name
        kw = axes._style_attrs.copy()
        kw.update(**kwargs)
        super().__init__(axes._sv, Axis._sv_detail(name), **kw)

    @staticmethod
    def _sv_detail(name):
        if isinstance(name, string_types):
            return getattr(sv, name.upper() + 'DETAIL')
        else:
            _tr = {sv.X: sv.XDETAIL, sv.Y: sv.YDETAIL, sv.Z: sv.ZDETAIL,
                   sv.R: sv.RDETAIL, sv.THETA: sv.THETADETAIL}
            return _tr[name]

    @property
    def show(self):
        return self._get_style(bool, sv.SHOWAXIS)

    @show.setter
    def show(self, show):
        self._set_style(bool(show), sv.SHOWAXIS)

    @property
    def min(self):
        return self._get_style(float, sv.RANGEMIN)

    @min.setter
    def min(self, value):
        self._set_style(float(value), sv.RANGEMIN)

    @property
    def max(self):
        return self._get_style(float, sv.RANGEMAX)

    @max.setter
    def max(self, value):
        self._set_style(float(value), sv.RANGEMAX)

    @property
    def ticks(self):
        return Ticks(self)

    @property
    def tick_labels(self):
        return TickLabels(self)

    @property
    def grid_lines(self):
        return GridLines(self)

    @property
    def minor_grid_lines(self):
        return MinorGridLines(self)

    @property
    def title(self):
        return Axis2DTitle(self)

    def __eq__(self, that):
        return (isinstance(that, type(self)) and self.name == that.name and
                self.axes == that.axes)

    def __ne__(self, that):
        return not (self == that)


class ReversibleAxis(Axis):
    '''
    reverse
    '''


class LinearAxis(Axis):
    '''
    preserve_length
    '''


class DataAxis(Axis):
    @property
    def title(self):
        return DataAxis2DTitle(self)


class FieldAxis(DataAxis):
    @property
    def variable(self):
        """The `Variable` assigned to this axis.

        :type: `Variable`

        This is the spatial variable associated with this axis
        and is usually one of ``(X, Y, Z)``.

        Example::
            >>> import tecplot as tp
            >>> fr = tp.active_frame()
            >>> ds = fr.dataset
            >>> axes = fr.plot().axes
            >>> axes.x_axis.variable.name, axes.y_axis.variable.name
            ('X', 'Y')
            >>> axes.x_axis.variable = ds.variable('U')
            >>> axes.y_axis.variable = ds.variable('V')
            >>> axes.x_axis.variable.name, axes.y_axis.variable.name
            ('U', 'V')
        """
        ds = self.axes.plot.frame.dataset
        return ds.variable(self.variable_index)

    @variable.setter
    def variable(self, v):
        self.variable_index = v.index

    @property
    def variable_index(self):
        return self._get_style(Index, sv.VARNUM)

    @variable_index.setter
    def variable_index(self, i):
        self._set_style(Index(i), sv.VARNUM)


class IndexedLineAxis(DataAxis, LinearAxis, ReversibleAxis):
    def __init__(self, axes, name, index):
        self.index = Index(index)
        super().__init__(axes, name, offset1=self.index)

    def __eq__(self, that):
        return (isinstance(that, type(self)) and self.index == that.index and
                self.name == that.name and self.axes == that.axes)

    def __ne__(self, that):
        return not (self == that)


class Cartesian2DFieldAxis(FieldAxis, LinearAxis, ReversibleAxis):
    pass


class Cartesian3DFieldAxis(FieldAxis, LinearAxis):
    @property
    def title(self):
        return DataAxis3DTitle(self)


class PolarAngleLineAxis(DataAxis, ReversibleAxis):
    def __init__(self, axes):
        super().__init__(axes, sv.THETA)

    @property
    def mode(self):
        """Units used for the theta axis.

        :type: `ThetaMode`

        Possible values: `ThetaMode.Degrees`, `ThetaMode.Radians`,
        `ThetaMode.Arbitrary`.
        """
        return self.axes._get_style(ThetaMode, sv.THETAMODE)

    @mode.setter
    def mode(self, value):
        self.axes._set_style(ThetaMode(value), sv.THETAMODE)

    @property
    def period(self):
        """Returns or sets the theta_period property.

        :type: `float`
        """
        return self.axes._get_style(float, sv.THETAPERIOD)

    @period.setter
    def period(self, value):
        self.axes._set_style(float(value), sv.THETAPERIOD)


class RadialLineAxis(DataAxis, LinearAxis, ReversibleAxis):
    def __init__(self, axes):
        super().__init__(axes, sv.R)

    @property
    def title(self):
        return RadialAxisTitle(self)


class SketchAxis(LinearAxis):
    pass


class XYLineAxis(IndexedLineAxis):
    @property
    def reverse(self):
        return self._get_style(bool, sv.ISREVERSED)

    @reverse.setter
    def reverse(self, value):
        self._Set_style(bool(value), sv.ISREVERSED)
