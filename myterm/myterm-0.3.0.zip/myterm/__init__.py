#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module myterm
"""

import os
import sys
import colorconsole
import colorconsole.terminal

__version_info__ = (0, 3, 0)
__version__ = '.'.join([str(val) for val in  __version_info__])

# MANAGEMENT COLOR DEFAULT
try:
    if os.name == "posix":
        # correction color and add clean
        import colorconsole.ansi

        class Terminal(colorconsole.ansi.Terminal):
            """
                class Terminal ansi with set_color, clean
            """
            colors_fg = {
                0: "30m",  # BLACK
                1: "34m",  # BLUE
                2: "32m",  # GREEN
                3: "36m",  # CYAN
                4: "31m",  # RED
                5: "35m",  # PURPLE
                6: "33m",  # BROWN
                7: "37m",  # LGREY
                8: "1;30m",  # DGRAY
                9: "1;34m",  # LBLUE
                10: "1;32m",  # LGREEN
                11: "1;36m",  # LCYAN
                12: "1;31m",  # LRED
                13: "1;35m",  # LPURPLE
                14: "1;33m",  # YELLOW
                15: "1;37m"  # WHITE
            }
            colors_bk = {
                0: "40m",
                1: "44m",
                2: "42m",
                3: "46m",
                4: "41m",
                5: "45m",
                6: "43m",
                7: "47m",
            }

            def __init__(self, **kw):
                colorconsole.ansi.Terminal.__init__(self, **kw)

            def set_color(self, fg=None, bk=None, stream=sys.stdout):
                if fg is not None:
                    stream.write(Terminal.escape + self.colors_fg[fg])
                if bk is not None:
                    stream.write(Terminal.escape + self.colors_bk[bk])

            def clean(self, stream=sys.stdout):
                """ clean stream"""
                stream.write("\033[0m")

        SCREEN = Terminal()
        FOREGROUND_DEFAULT = None
        BACKGROUND_DEFAULT = None
    else:
        # correction color and add clean
        import colorconsole.win

        class Terminal(colorconsole.win.Terminal):
            """
                class Terminal win with set_color, clean
            """

            def __init__(self, **kw):
                colorconsole.win.Terminal.__init__(self, **kw)

            def set_color(self, fg=None, bk=None, stream=sys.stdout):
                colorconsole.win.Terminal.set_color(self, fg, bk)

            def clean(self, stream=sys.stdout):
                """ clean stream"""
                pass

        SCREEN = Terminal()
        FOREGROUND_DEFAULT = colorconsole.terminal.colors['WHITE']
        BACKGROUND_DEFAULT = colorconsole.terminal.colors['BLACK']
except Exception as ex:
    class Terminal(object):
        """
            class Terminal minimal with set_color, clean
        """

        def __init__(self, **kw):
            pass

        def set_color(self, fg=None, bk=None, stream=sys.stdout):
            """ clean stream"""
            pass

        def clean(self, stream=sys.stdout):
            """ clean stream"""
            pass

    SCREEN = Terminal()
    FOREGROUND_DEFAULT = colorconsole.terminal.colors['WHITE']
    BACKGROUND_DEFAULT = colorconsole.terminal.colors['BLACK']

# MANAGEMENT COLOR CRITICAL
FOREGROUND_CRITICAL = colorconsole.terminal.colors['RED']
BACKGROUND_CRITICAL = BACKGROUND_DEFAULT
# MANAGEMENT COLOR ERROR
FOREGROUND_ERROR = colorconsole.terminal.colors['PURPLE']
BACKGROUND_ERROR = BACKGROUND_DEFAULT
# MANAGEMENT COLOR WARNING
FOREGROUND_WARNING = colorconsole.terminal.colors['BROWN']
BACKGROUND_WARNING = BACKGROUND_DEFAULT
# MANAGEMENT COLOR INFO
FOREGROUND_INFO = colorconsole.terminal.colors['GREEN']
BACKGROUND_INFO = BACKGROUND_DEFAULT
# MANAGEMENT COLOR DEBUG
FOREGROUND_DEBUG = colorconsole.terminal.colors['BLUE']
BACKGROUND_DEBUG = BACKGROUND_DEFAULT
# MANAGEMENT COLOR NOSET
FOREGROUND_NOSET = FOREGROUND_DEFAULT
BACKGROUND_NOSET = BACKGROUND_DEFAULT
# MANAGEMENT COLOR PROMPT
FOREGROUND_PROMPT = colorconsole.terminal.colors['BROWN']
BACKGROUND_PROMPT = BACKGROUND_DEFAULT

