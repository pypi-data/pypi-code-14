from contextlib import contextmanager
import logging
from six import string_types
from numbers import Number

from ..tecutil import (_tecutil, ArgList, IndexSet, StringList,
                       check_arglist_argtypes, lock, log_setattr, sv)

from .. import annotation, constant, plot, session
from ..constant import *
from ..exception import *

log = logging.getLogger(__name__)

@log_setattr
class Frame(object):
    """`Frame` object within a `Page`, holding onto a `Dataset` and a `Plot`.

    Parameters:
        uid (`integer <int>`, optional): This must be a *valid* unique ID
            number pointing internally to a Frame object or `None`. A new
            `Frame` is created if set to `None`. (default: `None`)
        page (`Page`, optional): The destination `Page` of this newly
            created `Frame`. If `None`, the currently active `Page` is used.
            (default: `None`)

    Warning:
        Though it is possible to create a `Frame` object using the
        constructor, it is usually sufficient to obtain a frame through
        `tecplot.active_frame()` or `Page.frame()`. One can also create a
        `Frame` using a `Page` handle with `Page.add_frame()`.

    The concept of the `Frame` is central to understanding the
    |Tecplot Engine|. The `Frame` is what connects a `Dataset` to a `Plot`
    handle from which one manipulates the desired image as well as accessing
    the attached data::

        >>> import tecplot
        >>> frame = tecplot.active_frame()
        >>> frame
        Frame(uid=11, Page(uid=1))
        >>> print(frame)
        Frame 001
    """

    page = None
    """The `Page` containing this Frame.

    This provides access to the parent `Page`::

        >>> frame = tecplot.active_frame()
        >>> page = frame.page
        >>> page.name
        Page 001
    """

    def __init__(self, uid, page):
        log.debug('Frame(uid={uid}, page={page})'.format(uid=uid,
                                                         page=repr(page)))
        self.page = page
        self.uid = uid
        """The internal unique ID number of this Frame."""
        self._sv = [sv.FRAMELAYOUT]

    def __str__(self):
        """Brief string representation.

        Returns:
            `string <str>`: Brief representation of this `Frame`.

        Example::
            >>> import tecplot
            >>> frame = tecplot.active_frame()
            >>> print(frame)
            Frame: "Frame 001"
        """
        return 'Frame: "{name}"'.format(name=self.name)

    def __repr__(self):
        """Executable string representation.

        Returns:
            `string <str>`: Internal representation of this `Frame`.

        The string returned can be executed to generate an identical
        copy of this `Frame` object::

            >>> import tecplot
            >>> frame = tecplot.active_frame()
            >>> frame_copy = None
            >>> print(repr(frame))
            Frame(uid=11, page=Page(uid=1))
            >>> exec('frame_copy = '+repr(frame))
            >>> frame_copy
            Frame(uid=11, page=Page(uid=1))

            >>> # frame_copy is not technically a copy.
            >>> # it is the same object as the original frame:
            >>> frame == frame_copy
            True
        """
        return 'Frame(uid={uid}, page={page})'.format(uid=self.uid,
                                                      page=repr(self.page))

    def __eq__(self, other):
        """Checks for `Frame` equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Frames <Frame>`.

        Example::
            >>> import tecplot
            >>> page = tecplot.active_page()
            >>> frame1 = page.active_frame()
            >>> frame2 = page.add_frame()
            >>> frame1 == frame2
            False
            >>> page.active_frame() == frame2
            True
        """
        return self.uid == other.uid

    def texts(self):
        """Get an iterator for all `Text` objects in the frame.

        Example usage::

        Get an list of all red `Text` objects.

            >>> import tecplot as tp
            >>> all_red_text_objects = [
            >>>    T for T in tp.active_frame().texts() if T.color == Color.Red]

        """
        return annotation.Annotation._Iterator(annotation.Text, self)

    def geometries(self):
        raise TecplotNotImplementedError

    def images(self):
        raise TecplotNotImplementedError

    @contextmanager
    def activated(self):
        """Context for temporarily activating this `Frame`.

        Example::

            >>> import tecplot
            >>> page = tecplot.active_page()
            >>> frame1 = page.active_frame()
            >>> frame2 = page.add_frame()
            >>> print(frame2.active)
            True
            >>> with frame1.activated():
            >>>     print(frame1.active)
            True
            >>> print(frame2.active)
            True
        """
        current_frame = Frame(_tecutil.FrameGetActiveID(), self.page)
        if self == current_frame:
            yield
        else:
            try:
                self.activate()
                yield
            finally:
                current_frame.activate()

    @property
    def name(self):
        """Returns or sets the name.

        :type: `string <str>`

        This is the name used when searching for `Frame` objects in
        `Page.frames` and `Page.frame`. It does not have to be unique,
        even for multiple frames in a single `Page`.

        Example::

            >>> import tecplot
            >>> frame = tecplot.active_frame()
            >>> frame.name = '3D Data View'
            >>> print('this frame:', frame.name)
            this frame: 3D Data View
        """
        with self.activated():
            return _tecutil.FrameGetName()[1]

    @name.setter
    @lock()
    def name(self, name):
        with self.activated():
            _tecutil.FrameSetName(name)

    @property
    def active(self):
        """Checks if this `Frame` is active.

        Returns:
            `bool`: `True` if this `Frame` is the active `Frame`.
        """
        return self.uid == _tecutil.FrameGetActiveID()

    @property
    def current(self):
        return self.uid == _tecutil.FrameGetUniqueID()

    @lock()
    def activate(self):
        """Causes this `Frame` to become active.

        Raises:
            `TecplotSystemError`

        The parent `Page` is implicitly "activated" as a side-effect of this
        operation::

            >>> import tecplot
            >>> page1 = tecplot.active_page()
            >>> frame1 = page1.active_frame()
            >>> page2 = tecplot.add_page()
            >>> frame2 = page2.active_frame()
            >>> frame1.active and page1.active
            False
            >>> frame2.active and page2.active
            True
            >>> frame1.activate()
            >>> frame2.active or page2.active
            False
            >>> frame1.active and page1.active
            True
        """
        if not self.active:
            if self.page is not None:
                self.page.activate()
            if not _tecutil.FrameActivateByUniqueID(self.uid):
                err = 'could not activate frame with uid {0}'.format(self.uid)
                raise TecplotSystemError(err)

    @property
    def plot_type(self):
        """Returns or sets the current plot type.

        :type: `constant.PlotType`

        Raises:
            `TecplotSystemError`

        A `Frame` can have only one active plot type at any given time. The
        types are enumerated by `constant.PlotType`::

            >>> import tecplot
            >>> from tecplot.constant import PlotType

            >>> tecplot.load_layout('mylayout.lay')
            >>> frame = tecplot.active_frame()
            >>> frame.plot_type
            <PlotType.Sketch: 4>
            >>> frame.plot_type = PlotType.Cartesian3D
            >>> frame.plot_type
            <PlotType.Cartesian3D: 1>
        """
        return _tecutil.FrameGetPlotTypeForFrame(self.uid)

    @plot_type.setter
    @lock()
    def plot_type(self, plot_type):
        with self.activated():
            res = SetValueReturnCode(_tecutil.FrameSetPlotType(plot_type.value))
            if res not in [SetValueReturnCode.Ok,
                           SetValueReturnCode.DuplicateValue]:
                if res is SetValueReturnCode.ContextError1:
                    raise TecplotSystemError('no Dataset attached to Frame')
                raise TecplotSystemError(res)

    def plot(self, plot_type=None):
        """Returns a `Plot` style-control object.

        :type:
            `Plot`:
                One of the possible `Plot` classes, depending on the
                ``plot_type`` specified. By default, the active plot
                type, obtained from `Frame.plot_type`, is used.

        The `Plot` object is the handle through which one can manipulate the
        style and visual representation of the `Dataset`. Possible return types
        are: `SketchPlot`, `Cartesian2DFieldPlot`, `Cartesian3DFieldPlot`,
        `PolarLinePlot` and `XYLinePlot`. Each of these have their own specific
        set of attributes and methods.

        Example::

            >>> frame = tecplot.active_frame()
            >>> frame.plot_type
            <PlotType.Cartesian3D: 1>
            >>> plot3d = frame.plot()
            >>> plot3d.show_contour = True
        """
        _dispatch = {
            PlotType.Cartesian2D: plot.Cartesian2DFieldPlot,
            PlotType.Cartesian3D: plot.Cartesian3DFieldPlot,
            PlotType.XYLine: plot.XYLinePlot,
            PlotType.PolarLine: plot.PolarLinePlot,
            PlotType.Sketch: plot.SketchPlot}
        return _dispatch[plot_type or self.plot_type](self)

    @lock()
    def move_to_bottom(self):
        """Moves `Frame` behind all others in `Page`.
        """
        _tecutil.FrameMoveToBottomByUniqueID(self.uid)

    @lock()
    def move_to_top(self):
        """Moves `Frame` in front of all others in `Page`.
        """
        _tecutil.FrameMoveToTopByUniqueID(self.uid)

    @lock()
    def active_zones(self, *zones):
        """Returns or sets the active `Zones <Zone>`.

        Parameters:
            *zones (`Zone` or `list` of `Zones <Zone>`, optional): The `Zone`
                objects, which must be in the `Dataset` attached to this
                `Frame`, that will be activated. All other `Zones <Zone>` will
                be deactivated.

        Yields:
            `Zones <Zone>`:
                This will return a generator of active `Zones <Zone>` in
                this `Frame`.
        """
        with self.activated():
            if zones:
                with IndexSet(*zones) as zoneset:
                    _tecutil.ZoneSetActive(zoneset, AssignOp.Equals.value)
            else:
                err = 'should return generator of active zones'
                raise TecplotNotImplementedError(err)

    @lock()
    def add_text(self, text, position=None, coord_sys=None, font_family=None,
                 bold=None, italic=None, size_units=None, size=None,
                 color=None, angle=None, line_spacing=None, anchor=None,
                 box_type=None, line_thickness=None, box_color=None,
                 fill_color=None, margin=None, zone=None):
        """Adds a `text <annotation.Text>` to a `Frame`.

        Parameters:
            text (`string <str>`): The text to add to the `Frame`.
                The text string must have a non-zero length.
            position (`tuple` of `floats <float>` (x,y), optional): The
                position of the anchor in the specified coordinates. (default:
                (0,0))
            coord_sys (`CoordSys`, optional): Coordinate system used to
                position the anchor of the text object. The possible values
                are: `CoordSys.Grid` or `CoordSys.Frame`. (default:
                `CoordSys.Frame`)
            font_family (`string <str>`, optional): The typeface family name.
                For consistency across various platforms, Tecplot guarantees
                that the following standard typeface family names are
                available: "Helvetica", "Times", "Courier", "Greek", "Math",
                and "User Defined". Other typeface family names may or may
                not be available depending on the TrueType fonts available.
                If the typeface family name or style is not available, a
                suitable replacement will be selected. (default: "Helvetica")
            bold (`boolean <bool>`, optional): Use the bold typeface of the
                specified font family. (default: `True`)
            italic (`boolean <bool>`, optional): Use the italic typeface of
                the specified font family. (default: `False`)
            size_units (`Units`, optional): Text sizing units. Possible
                values are: `Units.Grid`, `Units.Frame` or `Units.Point`.
                (default: `Units.Point`)
            size (`float`, optional): Text height in the specified units.
                (default: 14)
            color (`Color`, optional): Color of the text
                   (default: `Color.Black`)
            angle (`float`, optional): Angle of the text baseline in degrees
                from -360 to 360. (default: 0)
            line_spacing (`float`, optional): Line spacing in units of line
                size. Can take values from 0 to 50. (default: 1)
            anchor (`TextAnchor`, optional): Anchor position with respect to
                the text box. Possible values are: `TextAnchor.Left`,
                `TextAnchor.Center`, `TextAnchor.Right`,
                `TextAnchor.MidLeft`, `TextAnchor.MidCenter`,
                `TextAnchor.MidRight`, `TextAnchor.HeadLeft`,
                `TextAnchor.HeadCenter`, `TextAnchor.HeadRight`,
                `TextAnchor.OnSide` (default: `TextAnchor.Left`)
            box_type (`constant.TextBox`, optional): Type of text box can be one
                of: `TextBox.None_`, `TextBox.Filled` or `TextBox.Hollow`.
                (default: `TextBox.None_`)
            line_thickness (`float`, optional): Text box boarder line
                thickness may be a value in the range from 0.0001 to 100.
                (default: 0.1)
            box_color (`Color`, optional): Text box border line color. See
                `Color` for possible values. (default: `Color.Black`)
            fill_color (`Color`, optional): Text box fill color. See `Color`
                for possible values. (default: `White`)
            margin (`float`, optional): Margin between the text and text
                box. May be in the range from 0 to 2000. (default: 20)
            zone (`Zone`, optional): `Zone` or `XYLinemap` to which the text
                will be attached. (default: None)

        Returns:
            `annotation.Text`: The resulting `text box <annotation.Text>`
            object.

        Example::

            >>> import tecplot
            >>> from tecplot.constant import Color
            >>> frame = tecplot.active_frame()
            >>> frame.add_text('Hello, World!', position=(35, 50),
            ...   bold=True, italic=False, text_color=Color.Blue)
        """
        with self.activated():
            with ArgList() as arglist:
                if __debug__:
                    check_arglist_argtypes(
                        'frame.add_text',
                        ([tuple], [position], ['position']),
                        ([CoordSys], [coord_sys], ['coord_sys']),
                        (string_types, [font_family, text], ['font_family',
                                                             'text']),
                        ([bool], [bold, italic], ['bold', 'italic']),
                        ([Units], [size_units], ['size_units']),
                        ([Number], [size, angle, line_thickness, margin,
                                    line_spacing],
                            ['size', 'angle', 'line_thickness', 'margin',
                             'line_spacing']),
                        ([Color], [color, box_color, fill_color],
                            ['color', 'text_color', 'fill_color']),
                        ([TextAnchor], [anchor], ['anchor']),
                        ([TextBox], [box_type], ['box_type']),
                    )

                if zone is not None:
                    arglist[sv.ATTACHTOZONE] = True
                    arglist[sv.ZONE] = zone.index + 1

                # Note that TecUtil calls SV_TEXTCOLOR the color of the text,
                # and SV_COLOR as the text *box* color. These names correspond
                # to the 'color' and 'box_color' parameters.
                arglist.update(
                    (sv.TEXT, text),
                    (sv.XPOS, position[0] if position is not None else None,
                     float),
                    (sv.YPOS, position[1] if position is not None else None,
                     float),
                    (sv.POSITIONCOORDSYS, coord_sys),
                    (sv.ISBOLD, bold),
                    (sv.ISITALIC, italic),
                    (sv.SIZEUNITS, size_units),
                    (sv.HEIGHT, size, float),
                    (sv.ANGLE, angle, float),
                    (sv.LINETHICKNESS, line_thickness, float),
                    (sv.MARGIN, margin, float),
                    (sv.ANCHOR, anchor),
                    (sv.LINESPACING, line_spacing, float),
                    (sv.COLOR, box_color),
                    (sv.TEXTCOLOR, color),
                    (sv.FILLCOLOR, fill_color),
                    (sv.BOXTYPE, box_type))

                return annotation.Text(_tecutil.TextCreateX(arglist), self)

    @lock()
    def create_dataset(self, name, var_names=None, reset_style=False):
        """Create an empty `Dataset`.

        This will create a new `Dataset` and replace the existing one,
        destroying all data associated with it.

        Parameters:
            name (`string <str>`): Title of the new `Dataset`. This does not
                have to be unique.
            var_names (`list` of `strings <str>`, optional): `Variable`
                names. This only sets the names and not the data type or
                location. See `add_variable`. (default: `None`)
            reset_style (`boolean <bool>`): Reset style of the active `Frame`
                before loading the `Dataset`. (default: `False`)

        Returns:
            `Dataset`: The newly created `Dataset`.

        Raises:
            `TecplotSystemError`
        """
        with self.activated():
            if var_names is not None:
                var_names = StringList(*var_names)
            try:
                if not _tecutil.DataSetCreate(name, var_names, reset_style):
                    raise TecplotSystemError()
            finally:
                if var_names is not None:
                    var_names.dealloc()
            return self.dataset

    def _get_style(self, rettype, *svargs):
        svargs = self._sv + list(svargs)
        return session.get_style(rettype, *svargs, uniqueid=self.uid)

    def _set_style(self, value, *svargs):
        svargs = self._sv + list(svargs)
        session.set_style(value, *svargs, uniqueid=self.uid)

    @property
    def background_color(self):
        """Color of the background.

        :type: `Color`
        """
        return self._get_style(constant.Color, sv.BACKGROUNDCOLOR)

    @background_color.setter
    def background_color(self, value):
        self._set_style(constant.Color(value), sv.BACKGROUNDCOLOR)

    @property
    def border_thickness(self):
        """The border thickness in units of `Frame.size_pos_units`.

        :type: `float`
        """
        return self._get_style(float, sv.BORDERTHICKNESS)

    @border_thickness.setter
    def border_thickness(self, value):
        self._set_style(float(value), sv.BORDERTHICKNESS)

    @property
    def height(self):
        """The height in units of `Frame.size_pos_units`.

        :type: `float`
        """
        return self._get_style(float, sv.HEIGHT)

    @height.setter
    def height(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def show_border(self):
        """Show or hide the `Frame`'s border.

        :type: `bool`
        """
        return self._get_style(bool, sv.SHOWBORDER)

    @show_border.setter
    def show_border(self, value):
        self._set_style(bool(value), sv.SHOWBORDER)

    @property
    def show_header(self):
        """Show or hide the `Frame`'s header in the border.

        :type: `bool`
        """
        return self._get_style(bool, sv.SHOWHEADER)

    @show_header.setter
    def show_header(self, value):
        self._set_style(bool(value), sv.SHOWHEADER)

    @property
    def header_background_color(self):
        """The header's background color.

        :type: `Color`
        """
        return self._get_style(constant.Color, sv.HEADERCOLOR)

    @header_background_color.setter
    def header_background_color(self, value):
        self._set_style(constant.Color(value), sv.HEADERCOLOR)

    @property
    def size_pos_units(self):
        """The units used for size properties.

        :type: `FrameSizePosUnits`

        Possible values: `Paper`, `Workspace <FrameSizePosUnits.Workspace>`.
        """
        return self._get_style(constant.FrameSizePosUnits, sv.FRAMESIZEPOSUNITS)

    @size_pos_units.setter
    def size_pos_units(self, value):
        self._set_style(constant.FrameSizePosUnits(value), sv.FRAMESIZEPOSUNITS)

    @property
    def transparent(self):
        """Use transparency within this `Frame`.

        :type: `bool`
        """
        return self._get_style(bool, sv.ISTRANSPARENT)

    @transparent.setter
    def transparent(self, value):
        self._set_style(bool(value), sv.ISTRANSPARENT)

    @property
    def width(self):
        """The width in units of `Frame.size_pos_units`.

        :type: `float`
        """
        return self._get_style(float, sv.WIDTH)

    @width.setter
    def width(self, value):
        self._set_style(float(value), sv.WIDTH)
