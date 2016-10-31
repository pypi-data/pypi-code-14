from builtins import super

from collections import namedtuple

from ..tecutil import _tecutil
from .. import session
from ..constant import Color
from ..tecutil import lock, log_setattr, sv


@log_setattr
class View(object):
    def __init__(self, plot):
        self.plot = plot

    @lock()
    def fit(self):
        with self.plot.frame.activated():
            return _tecutil.ViewFit()


class Cartesian2DView(View):
    pass


class Cartesian3DView(View):
    pass


class LineView(View):
    pass


class PolarView(View):
    pass

@log_setattr
class ReadOnlyViewport(session.Style):
    def __init__(self, axes):
        kw = dict(uniqueid=axes.plot.frame.uid)
        super().__init__(*axes._sv, **kw)

    @property
    def bottom(self):
        """(`float`) Bottom position of viewport relative to the `Frame`.

        :type: `float` in percentage of frame height from the bottom of the
            frame.

        Example usage::

            >>> print(plot.axes.viewport.bottom)
            10.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.Y1)

    @property
    def left(self):
        """(`float`) Left position of viewport relative to the `Frame`.

        :type: `float` in percentage of frame width from the left of the frame.

        Example usage::

            >>> print(plot.axes.viewport.left)
            10.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.X1)

    @property
    def right(self):
        """(`float`) Right position of viewport relative to the `Frame`.

        :type: `float` in percentage of frame width from the left of the frame.

        Example usage::

            >>> print(plot.axes.viewport.right)
            90.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.X2)

    @property
    def top(self):
        """(`float`) Top position of viewport relative to the `Frame`.

        :type: `float` in percentage of frame height from the bottom of the
            frame.

        Example usage::

            >>> print(plot.axes.viewport.top)
            90.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.Y2)


class Viewport(ReadOnlyViewport):

    bottom = ReadOnlyViewport.bottom
    left   = ReadOnlyViewport.left
    right  = ReadOnlyViewport.right
    top    = ReadOnlyViewport.top

    @bottom.setter
    def bottom(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.Y1)

    @left.setter
    def left(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.X1)

    @right.setter
    def right(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.X2)

    @top.setter
    def top(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.Y2)


class Cartesian2DViewport(Viewport):
    @property
    def nice_fit_buffer(self):
        """Tolerance for viewport/frame fit niceness.

        :type: `float`

        Example usage::

            >>> plot.axes.viewport.nice_fit_buffer = 20
        """
        return self._get_style(float, sv.VIEWPORTNICEFITBUFFER)

    @nice_fit_buffer.setter
    def nice_fit_buffer(self, value):
        self._set_style(float(value), sv.VIEWPORTNICEFITBUFFER)

    @property
    def top_snap_target(self):
        """Target value for top when being adjusted or dragged.

        :type: `float`

        Example usage::

            >>> plot.axes.viewport.top_snap_target = 90
        """
        return self._get_style(float, sv.VIEWPORTTOPSNAPTARGET)

    @top_snap_target.setter
    def top_snap_target(self, value):
        self._set_style(float(value), sv.VIEWPORTTOPSNAPTARGET)

    @property
    def top_snap_tolerance(self):
        """Tolerance for snapping to target value for top.

        :type: `float`

        Example usage::

            >>> plot.axes.viewport.top_snap_tolerance = 8
        """
        return self._get_style(float, sv.VIEWPORTTOPSNAPTOLERANCE)

    @top_snap_tolerance.setter
    def top_snap_tolerance(self, value):
        self._set_style(float(value), sv.VIEWPORTTOPSNAPTOLERANCE)


class PolarViewport(Viewport):
    @property
    def fill_color(self):
        if self._get_style(bool, sv.VIEWPORTSTYLE, sv.ISFILLED):
            return self._get_style(Color, sv.VIEWPORTSTYLE, sv.FILLCOLOR)

    @fill_color.setter
    def fill_color(self, value):
        if value is None:
            self._set_style(False, sv.VIEWPORTSTYLE, sv.ISFILLED)
        else:
            self._set_style(True, sv.VIEWPORTSTYLE, sv.ISFILLED)
            self._set_style(Color(value), sv.VIEWPORTSTYLE, sv.FILLCOLOR)

    @property
    def show_border(self):
        return self._get_style(bool, sv.VIEWPORTSTYLE, sv.DRAWBORDER)

    @show_border.setter
    def show_border(self, value):
        self._set_style(bool(value), sv.VIEWPORTSTYLE, sv.DRAWBORDER)

    @property
    def border_thickness(self):
        return self._get_style(float, sv.VIEWPORTSTYLE, sv.LINETHICKNESS)

    @border_thickness.setter
    def border_thickness(self, value):
        self._set_style(float(value), sv.VIEWPORTSTYLE, sv.LINETHICKNESS)
