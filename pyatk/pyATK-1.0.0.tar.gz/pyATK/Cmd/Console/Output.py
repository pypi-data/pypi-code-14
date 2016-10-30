# -*- coding: utf-8 -*-
from pyATK.Cmd.Helpers.ColorHelper import Color
from pyATK.Cmd.Helpers.ProgressHelper import ProgressBarHelper
from pyATK.Cmd.Helpers.TableHelper import TableHelper


class Output:
    """
    >>> output = Output()
    >>> output.write("Hello World")
    Hello World
    >>> import pyATK
    >>> output.write("Hello World", pyATK.Cmd.Helpers.ColorHelper.Color.FG_RED)
    \x1b[31mHello World\x1b[39m
    """
    IO_HELPER = 0x01
    PROGRESS_HELPER = 0x02
    TABLE_HELPER = 0x04
    helpers = []

    def __init__(self):
        pass

    def write(self, msg, color=None):
        if color is None:
            print(msg)
        else:
            Color.colored(msg, color)

