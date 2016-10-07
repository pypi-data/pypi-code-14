from __future__ import unicode_literals, with_statement

import os
import re
import collections

from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import unittest
from .. import patch_tecutil
from unittest.mock import patch

import tecplot as tp
import tecplot.plot
from tecplot.exception import *
from tecplot.constant import *
from tecplot.constant import TECUTIL_BAD_ID
from tecplot.tecutil import sv
from tecplot.annotation import Text

from ..sample_data import loaded_sample_data
from .test_page import TestPage

_TECUTIL_VALID_ID = TECUTIL_BAD_ID + 1


class TestFrames(unittest.TestCase):

    def test_activate_frame(self):
        with TestFrame.non_active_frame() as frame:
            self.assertFalse(frame.active)
            frame.activate()
            self.assertTrue(frame.active)

    def test_active_frame(self):
        with TestPage.active_page():
            frame = tp.active_frame()
            self.assertIsInstance(frame, tp.layout.Frame)
            self.assertIsInstance(frame.uid, int)
            self.assertGreater(frame.uid, 0)


class TestFrame(unittest.TestCase):
    @staticmethod
    @contextmanager
    def active_frame():
        with TestPage.active_page() as page:
            yield page.active_frame()

    @staticmethod
    @contextmanager
    def non_active_frame():
        with TestPage.active_page() as page:
            frame = page.active_frame()
            page.add_frame()
            yield frame

    @staticmethod
    @contextmanager
    def frames():
        with TestPage.active_page() as page:
            yield [page.active_frame(), page.add_frame()]

    def test___str__(self):
        with TestFrame.active_frame() as frame:
            frame.name = 'Test'
            self.assertEqual(str(frame), 'Frame: "Test"')

    def test___repr__(self):
        ptrn = re.compile(r'Frame\(uid=\d+, page=Page\(uid=\d+\)\)')
        with TestFrame.active_frame() as frame:
            self.assertRegex(repr(frame), ptrn)

    def test_texts(self):
        with TestFrame.active_frame() as frame:
            frame.add_text('abc')
            text_iterator = frame.texts()
            self.assertIsInstance(text_iterator, collections.Iterable)

    def test_name(self):
        with TestFrame.active_frame() as frame:
            frame.name = 'Test'
            self.assertEqual(frame.name, 'Test')

    def test_aux_data(self):
        """
        with TestFrame.active_frame() as frame:
            frame.aux_data
        """
        pass

    def test_dataset(self):
        with TestFrame.active_frame() as frame:
            self.assertIsInstance(frame.dataset, tp.data.Dataset)

    def test___eq__(self):
        f1a = tp.layout.Frame(1, tp.layout.Page(2))
        f1b = tp.layout.Frame(1, tp.layout.Page(2))
        f2 = tp.layout.Frame(2, tp.layout.Page(2))
        self.assertEqual(f1a, f1b)
        self.assertNotEqual(f1a, f2)

    def test_plot_type(self):
        with TestFrame.active_frame() as frame:
            self.assertIsInstance(frame.plot_type, PlotType)
            with patch_tecutil(
                    'FrameSetPlotType',
                    return_value=SetValueReturnCode.ContextError1.value):
                with self.assertRaises(TecplotSystemError):
                    frame.plot_type = PlotType.Cartesian3D

    def test_move(self):
        with TestFrame.active_frame() as frame:
            self.assertIsNone(frame.move_to_bottom())
            self.assertIsNone(frame.move_to_top())

    def test_background_color(self):
        frame = tp.active_frame()
        for val in [Color.Black, Color.Red]:
            frame.background_color = val
            self.assertEqual(frame.background_color, val)
        with self.assertRaises(ValueError):
            frame.background_color = 0.5

    def test_header_background_color(self):
        frame = tp.active_frame()
        for val in [Color.Black, Color.Red]:
            frame.header_background_color = val
            self.assertEqual(frame.header_background_color, val)
        with self.assertRaises(ValueError):
            frame.header_background_color = 0.5

    def test_border_thickness(self):
        frame = tp.active_frame()
        for val in [0.5, 0.1]:
            frame.border_thickness = val
            self.assertEqual(frame.border_thickness, val)
        with self.assertRaises(ValueError):
            frame.border_thickness = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.border_thickness = 0

    def test_height(self):
        frame = tp.active_frame()
        frame.size_pos_units = FrameSizePosUnits.Paper
        h = frame.height
        for val in [20, h]:
            frame.height = val
            self.assertEqual(frame.height, val)
        with self.assertRaises(ValueError):
            frame.height = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.height = 0

    def test_show_border(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.show_border = val
            self.assertEqual(frame.show_border, val)

    def test_show_header(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.show_header = val
            self.assertEqual(frame.show_header, val)

    def test_size_pos_units(self):
        frame = tp.active_frame()
        for val in [FrameSizePosUnits.Paper,
                    FrameSizePosUnits.Workspace]:
            frame.size_pos_units = val
            self.assertEqual(frame.size_pos_units, val)
        with self.assertRaises(ValueError):
            frame.size_pos_units = 0.5

    def test_transparent(self):
        frame = tp.active_frame()
        for val in [True, False]:
            frame.transparent = val
            self.assertEqual(frame.transparent, val)

    def test_width(self):
        frame = tp.active_frame()
        frame.size_pos_units = FrameSizePosUnits.Paper
        w = frame.width
        for val in [20, w]:
            frame.width = val
            self.assertEqual(frame.width, val)
        with self.assertRaises(ValueError):
            frame.width = 'badtype'
        with self.assertRaises(TecplotSystemError):
            frame.width = 0

    def test_current(self):
        tp.new_layout()
        f1 = tp.active_frame()
        self.assertTrue(f1.current)

    def test_activation_failure(self):
        with patch_tecutil('FrameActivateByUniqueID', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.new_layout()
                f1 = tp.active_frame()
                tp.active_page().add_frame()
                f1.activate()

    def test_plot_type_failure(self):
        with patch_tecutil('FrameSetPlotType',
                           return_value=SetValueReturnCode.ContextError2.value):
            with self.assertRaises(TecplotSystemError):
                fr = tp.active_frame()
                fr.plot_type = PlotType.Cartesian3D

    def test_plot(self):
        tp.new_layout()
        with loaded_sample_data('3x3x3_p'):
            fr = tp.active_frame()
            fr.plot_type = PlotType.Cartesian3D
            self.assertIsInstance(fr.plot(), tp.plot.Cartesian3DFieldPlot)

    def test_active_zones(self):
        tp.new_layout()
        # zones: Rectangular3D, Rectangular2D, Line, Cylinder
        with loaded_sample_data('4zones') as dataset:
            fr = tp.active_frame()
            with self.assertRaises(TecplotNotImplementedError):
                names = [z.name for z in fr.active_zones()]
                self.assertEqual(len(names), 4)
                self.assertEqual(names, ['Rectangular3D', 'Rectangular2D',
                                         'Line', 'Cylinder'])
            fr.active_zones(*dataset.zones('Rectangular*'))
            with self.assertRaises(TecplotNotImplementedError):
                names = [z.name for z in fr.active_zones()]
                self.assertEqual(len(names), 2)
                self.assertEqual(names, ['Rectangular3D', 'Rectangular2D'])


class TestAddText(unittest.TestCase):
    def setUp(self):
        self.frame = tp.active_frame()

    def test_add_text_returns_correct_object(self):
        text = self.frame.add_text('abc')
        self.assertIsInstance(text, Text)

    def test_invalid_arg_types(self):
        if __debug__:
            frame = self.frame
            with self.assertRaises(TecplotTypeError):
                frame.add_text(text=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', position='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', coord_sys=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', font_family=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', bold=0.0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', italic=2.0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', size='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', angle='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', line_thickness='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', size_units='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', margin='a')
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_color=3)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', color=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', fill_color=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_type=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', box_type=False)
            with self.assertRaises(AttributeError):
                frame.add_text('', zone=0)
            with self.assertRaises(TecplotTypeError):
                frame.add_text('', anchor='a')
            with self.assertRaises(AttributeError):
                frame.add_text('', zone=False)

    @patch('tecplot.data.Zone')
    @patch('tecplot.plot.XYLinemap')
    def test_valid_arg_types(self, xy_map, zone):
        if __debug__:
            # Overwrite the auto-created magic mocks for the .index properties
            # with simple int's so they can be correctly incremented.
            zone.index = 0
            xy_map.index = 0
            with patch_tecutil('TextCreateX'):
                try:
                    frame = self.frame
                    frame.add_text(text='a')
                    frame.add_text('', position=(1, 2))
                    frame.add_text('', coord_sys=CoordSys.Grid)
                    frame.add_text('', font_family='a')
                    frame.add_text('', bold=True)
                    frame.add_text('', italic=True)
                    frame.add_text('', size=3)
                    frame.add_text('', angle=1)
                    frame.add_text('', line_thickness=2.0)
                    frame.add_text('', margin=1.3)
                    frame.add_text('', box_color=Color.Custom1)
                    frame.add_text('', color=Color.Custom2)
                    frame.add_text('', fill_color=Color.Custom3)
                    frame.add_text('', box_type=TextBox.Filled)
                    frame.add_text('', anchor=TextAnchor.HeadCenter)
                    frame.add_text('', size_units=Units.Grid)
                    frame.add_text('', zone=zone)
                    frame.add_text('', zone=xy_map)

                except TecplotTypeError:
                    # Should not get an exception here
                    self.assertTrue(False)

    @patch('tecplot.data.Zone')
    def test_args_are_passed_to_tecutil(self, zone):
        position = (1.1, 2.2)
        zone.index = 0
        text = 'abc'
        arg_dict = {
            'coord_sys': (sv.POSITIONCOORDSYS, CoordSys.Grid),
            'bold': (sv.ISBOLD, True),
            'italic': (sv.ISITALIC, True),
            'size_units': (sv.SIZEUNITS, Units.Grid),
            'size': (sv.HEIGHT, 3.14),
            'angle': (sv.ANGLE, .314),
            'line_thickness': (sv.LINETHICKNESS, 1.2),
            'margin': (sv.MARGIN, 1.3),
            'anchor': (sv.ANCHOR, TextAnchor.HeadCenter),
            'line_spacing': (sv.LINESPACING, 1.5),
            'color': (sv.TEXTCOLOR, Color.Custom3),
            'box_color': (sv.COLOR, Color.Custom4),
            'fill_color': (sv.FILLCOLOR, Color.Custom8),
            'box_type': (sv.BOXTYPE, TextBox.Filled),
        }

        def fake_text_create(arglist):
            # Zone should pass through as index 1
            self.assertEqual(arglist[sv.ZONE], 1)
            self.assertTrue(arglist[sv.ATTACHTOZONE])

            # position should pass through as x,y
            self.assertEqual(arglist[sv.XPOS], position[0])
            self.assertEqual(arglist[sv.YPOS], position[1])

            # All others should pass though unchanged
            for value in arg_dict.values():
                sv_name = value[0]
                sv_value = value[1].value if hasattr(value[1], 'value') else value[1]
                self.assertEqual(arglist[sv_name], sv_value)

            return _TECUTIL_VALID_ID

        with patch_tecutil('TextCreateX', side_effect=fake_text_create):
            args = {k: v[1] for k, v in arg_dict.items()}
            # Add zone and position
            args['zone'] = zone
            args['position'] = position
            self.frame.add_text(text, **args)

    def test_default_args(self):
        # noinspection PyStatementEffect
        def fake_text_create(arglist):
            for option in [sv.POSITIONCOORDSYS,
                           sv.ISBOLD,
                           sv.ISITALIC,
                           sv.SIZEUNITS,
                           sv.HEIGHT,
                           sv.ANGLE,
                           sv.LINETHICKNESS,
                           sv.MARGIN,
                           sv.ANCHOR,
                           sv.LINESPACING,
                           sv.COLOR,
                           sv.TEXTCOLOR,
                           sv.FILLCOLOR,
                           sv.BOXTYPE,
                           sv.ZONE,
                           sv.XPOS,
                           sv.YPOS]:
                with self.assertRaises(TypeError):
                    # Accessing the option should raise a TypeError
                    # since that option should not exist in the incoming
                    # arglist.
                    arglist[option]

            return _TECUTIL_VALID_ID

        with patch_tecutil('TextCreateX', side_effect=fake_text_create):
            self.frame.add_text('abc')

    def test_invalid_return_value(self):
        # noinspection PyUnusedLocal
        def fake_text_create(arglist):
            return TECUTIL_BAD_ID

        with patch_tecutil('TextCreateX', side_effect=fake_text_create):
            with self.assertRaises(TecplotLogicError):
                self.frame.add_text('abc')

if __name__ == '__main__':
    from .. import main
    main()
