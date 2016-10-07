from builtins import super

from ..tecutil import _tecutil
from ..constant import *
from .. import session
from ..tecutil import log_setattr, sv
from .axis import (Cartesian2DFieldAxis, Cartesian3DFieldAxis,
                   PolarAngleLineAxis, RadialLineAxis, SketchAxis, XYLineAxis)
from .grid import PreciseGrid
from .view import Cartesian2DViewport, ReadOnlyViewport, Viewport


class Axes(session.Style):
    def __init__(self, plot, *svargs):
        self.plot = plot
        kw = dict(uniqueid=plot.frame.uid)
        super().__init__(*svargs, **kw)

    def __eq__(self, that):
        return isinstance(that, type(self)) and (self.plot == that.plot)

    def __ne__(self, that):
        return not (self == that)

    @property
    def grid_area(self):
        return GridArea(self)

    @property
    def preserve_scale(self):
        return self._get_style(bool, sv.PRESERVICEAXISSCALE)

    @preserve_scale.setter
    def preserve_scale(self, value):
        self._set_style(bool(value), sv.PRESERVICEAXISSCALE)

    @property
    def viewport(self):
        return Viewport(self)


class Axes2D(Axes):
    @property
    def precise_grid(self):
        return PreciseGrid(self)


class CartesianAxes(Axes):
    @property
    def auto_adjust_ranges(self):
        return self._get_style(bool, sv.AUTOADJUSTRANGESTONICEVALUES)

    @auto_adjust_ranges.setter
    def auto_adjust_ranges(self, value):
        self._set_style(bool(value), sv.AUTOADJUSTRANGESTONICEVALUES)


class Cartesian2DAxes(CartesianAxes):
    @property
    def xy_ratio(self):
        return self._get_style(float, sv.DEPXTOYRATIO)

    @xy_ratio.setter
    def xy_ratio(self, value):
        self._set_style(float(value), sv.DEPXTOYRATIO)

    @property
    def axis_mode(self):
        """Axis relations regarding functional dependency

        :type: `AxisMode`

        Possible values: `Independent`, `XYDependent`.
        """
        return self._get_style(AxisMode, sv.AXISMODE)

    @axis_mode.setter
    def axis_mode(self, value):
        self._set_style(AxisMode(value), sv.AXISMODE)

    @property
    def viewport(self):
        return Cartesian2DViewport(self)


class Cartesian3DAxes(Cartesian2DAxes):
    @property
    def xz_ratio(self):
        """Axis scaling ratio ``X/Y``.

        :type: `float` in percent

        Example usage::

            >>> plot.axes.xz_ratio = 20
        """
        return self._get_style(float, sv.DEPXTOZRATIO)

    @xz_ratio.setter
    def xz_ratio(self, value):
        self._set_style(float(value), sv.DEPXTOZRATIO)

    @property
    def axis_mode(self):
        """Axis relations regarding functional dependency

        :type: `AxisMode`

        Possible values: `Independent`, `XYZDependent`, `XYDependent`.
        """
        return super().axis_mode

    @axis_mode.setter
    def axis_mode(self, mode):
        super(type(self), self.__class__).axis_mode.fset(self, mode)

    @property
    def aspect_ratio_limit(self):
        """Scale limit of the axes aspect ratio.

        :type: `float`

        This is the limit above which the axes relative scales will be pegged
        to `aspect_ratio_reset`. The following example will set the aspect
        ratio between scales to 1 if they first exceed a ratio of 10::

            >>> plot.axes.aspect_ratio_limit = 10
            >>> plot.axes.aspect_ratio_reset = 1
            >>> plot.axes.reset_scale()
        """
        return self._get_style(float, sv.ASPECTRATIOLIMIT)

    @aspect_ratio_limit.setter
    def aspect_ratio_limit(self, value):
        self._set_style(float(value), sv.ASPECTRATIOLIMIT)

    @property
    def aspect_ratio_reset(self):
        """Axes scale aspect ratio used when `aspect_ratio_limit` is exceeded.

        :type: `float`

        This is the aspect ratio used to scale the axes when the data's aspect
        ratio exceeds the value set to `aspect_ratio_limit`. The following
        example will set the aspect ratio between scales to 10 if they first
        exceed a ratio of 15::

            >>> plot.axes.aspect_ratio_limit = 15
            >>> plot.axes.aspect_ratio_reset = 10
            >>> plot.axes.reset_scale()
        """
        return self._get_style(float, sv.ASPECTRATIORESET)

    @aspect_ratio_reset.setter
    def aspect_ratio_reset(self, value):
        self._set_style(float(value), sv.ASPECTRATIORESET)

    @property
    def range_aspect_ratio_limit(self):
        """Range limit of the axes aspect ratio.

        :type: `float`

        This is the limit above which the axes' relative ranges will be pegged
        to `range_aspect_ratio_reset`. The following example will set the
        aspect ratio between ranges to 1 if they first exceed a ratio of 10::

            >>> plot.axes.range_aspect_ratio_limit = 10
            >>> plot.axes.range_aspect_ratio_reset = 1
            >>> plot.axes.reset_ranges()
        """
        return self._get_style(float, sv.BOXASPECTRATIOLIMIT)

    @range_aspect_ratio_limit.setter
    def range_aspect_ratio_limit(self, value):
        self._set_style(float(value), sv.BOXASPECTRATIOLIMIT)

    @property
    def range_aspect_ratio_reset(self):
        """Axes range aspect ratio used `range_aspect_ratio_limit` is exceeded.

        :type: `float`

        This is the aspect ratio used to set the ranges of the axes when the
        axes' aspect ratios exceed the value of `range_aspect_ratio_limit`. The
        following example will set the aspect ratio between ranges to 10 if
        they first exceed a ratio of 15::

            >>> plot.axes.range_aspect_ratio_limit = 15
            >>> plot.axes.range_aspect_ratio_reset = 10
            >>> plot.axes.reset_ranges()
        """
        return self._get_style(float, sv.BOXASPECTRATIORESET)

    @range_aspect_ratio_reset.setter
    def range_aspect_ratio_reset(self, value):
        self._set_style(float(value), sv.BOXASPECTRATIORESET)

    @property
    def edge_auto_reset(self):
        """Enable automatically choosing which edges to label.

        :type: `bool`

        Example usage::

            >>> plot.axes.edge_auto_reset = True
        """
        return self._get_style(bool, sv.EDGEAUTORESET)

    @edge_auto_reset.setter
    def edge_auto_reset(self, value):
        self._set_style(bool(value), sv.EDGEAUTORESET)

    @property
    def viewport(self):
        """Viewport position and extent control

        :type: `ReadOnlyViewport`

        Example usage::

            >>> print(plot.axes.viewport.bottom)
            5
        """
        return ReadOnlyViewport(self)

    def reset_scale(self):
        """Recalculate the scale factors for each axis.

        Aspect ratio limits are taken into account.
        """
        with plot.frame.activated():
            if not _tecutil.Reset3DScaleFactors():
                raise TecplotSystemError()


class SketchAxes(Cartesian2DAxes, Axes2D):
    def __init__(self, plot):
        super().__init__(plot, sv.SKETCHAXIS)

    @property
    def x_axis(self):
        return SketchAxis(self, sv.X)

    @property
    def y_axis(self):
        return SketchAxis(self, sv.Y)


class Cartesian2DFieldAxes(Cartesian2DAxes, Axes2D):
    def __init__(self, plot):
        super().__init__(plot, sv.TWODAXIS)

    @property
    def x_axis(self):
        return Cartesian2DFieldAxis(self, sv.X)

    @property
    def y_axis(self):
        return Cartesian2DFieldAxis(self, sv.Y)


class Cartesian3DFieldAxes(Cartesian3DAxes):
    def __init__(self, plot):
        super().__init__(plot, sv.THREEDAXIS)

    @property
    def x_axis(self):
        return Cartesian3DFieldAxis(self, sv.X)

    @property
    def y_axis(self):
        return Cartesian3DFieldAxis(self, sv.Y)

    @property
    def z_axis(self):
        return Cartesian3DFieldAxis(self, sv.Z)


class PolarLineAxes(Axes2D):
    def __init__(self, plot):
        super().__init__(plot, sv.POLARAXIS)

    @property
    def r_axis(self):
        return RadialLineAxis(self)

    @property
    def theta_axis(self):
        return PolarAngleLineAxis(self)


class XYLineAxes(Cartesian2DAxes, Axes2D):
    def __init__(self, plot):
        super().__init__(plot, sv.XYLINEAXIS)

    def x_axis(self, index):
        return XYLineAxis(self, sv.X, index)

    def y_axis(self, index):
        return XYLineAxis(self, sv.Y, index)
