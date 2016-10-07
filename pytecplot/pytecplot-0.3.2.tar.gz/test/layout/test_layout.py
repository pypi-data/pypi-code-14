from __future__ import unicode_literals, with_statement

import os
import re

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

from ..sample_data import loaded_sample_data

_TECUTIL_VALID_ID = TECUTIL_BAD_ID + 1

class TestLayouts(unittest.TestCase):
    def test_new_layout(self):
        self.assertIsNone(tp.new_layout())

    def test_load_layout(self):
        with NamedTemporaryFile(delete=False) as f:
            f.write(b'#!MC 1410\n')
            f.close()
            self.assertIsNone(tp.load_layout(f.name))
            os.remove(f.name)
        self.assertRaises(OSError, tp.load_layout,
                          '/nonexistent/path/to/layout/file.lay')

    def test_save_layout_default_arguments(self):
        def fake_save_layout(arglist):
            for option in [sv.INCLUDEDATA, sv.INCLUDEPREVIEW,
                           sv.USERELATIVEPATHS, sv.POSTLAYOUTCOMMANDS,
                           sv.PAGELIST]:

                with self.assertRaises(TypeError):
                    # Accessing the arglist option should raise a TypeError
                    # since that option should not exist in the incoming
                    # arglist.

                    # noinspection PyStatementEffect
                    arglist[option]

            return True

        with patch_tecutil('SaveLayoutX', side_effect=fake_save_layout):
            tp.save_layout(filename='filename')

    def test_save_layout_arguments(self):
        filename = 'filename'
        include_data = True
        include_preview = True
        use_relative_paths = True
        post_layout_commands = 'post_layout_commands'
        page_list = [tp.active_page()]

        def fake_save_layout(arglist):
            self.assertEqual(arglist[sv.FNAME], filename)
            self.assertTrue(arglist[sv.INCLUDEDATA])
            self.assertTrue(arglist[sv.INCLUDEPREVIEW])
            self.assertTrue(arglist[sv.USERELATIVEPATHS])
            self.assertEqual(arglist[sv.POSTLAYOUTCOMMANDS], post_layout_commands)

            pages = [P for P in arglist[sv.PAGELIST]]
            self.assertListEqual([0], pages)
            return True

        with patch_tecutil('SaveLayoutX', side_effect=fake_save_layout):
            tp.save_layout(filename=filename, include_data=include_data,
                           include_preview=include_preview,
                           use_relative_paths=use_relative_paths,
                           post_layout_commands=post_layout_commands,
                           pages=page_list)

    def test_save_layout_parameter_types(self):
        if __debug__:
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename=1)
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename='a', include_data=3)
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename='a', include_preview=3)
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename='a', use_relative_paths=3)
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename='a', post_layout_commands=3)
            with self.assertRaises(TecplotTypeError):
                tp.save_layout(filename='a', pages=3)

    def test_save_layout(self):
        tp.new_layout()
        with NamedTemporaryFile(suffix='.lay', delete=False) as f:
            f.close()
            self.assertIsNone(tp.save_layout(f.name))
            os.remove(f.name)

    def test_save_layout_return_value(self):
        # noinspection PyUnusedLocal
        def fake_save_layout(arglist):
            return False

        with patch_tecutil('SaveLayoutX', side_effect=fake_save_layout):
            with self.assertRaises(TecplotSystemError):
                tp.save_layout(filename='filename')

if __name__ == '__main__':
    from .. import main
    main()
