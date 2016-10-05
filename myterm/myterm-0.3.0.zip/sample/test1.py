#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    test of myterm.parser.OptionParser
"""

import sys, traceback
import colorconsole, colorconsole.terminal
from myterm.parser import OptionParser
import myterm
import os

VERSION="0.1"
PROG="test1"
DESCRIPTION="""test of myterm.OptionParser"""
AUTHOR="Frederic Aoustin"

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(version="%s %s" % (PROG,VERSION), usage=usage)
    parser.description= DESCRIPTION
    parser.epilog = AUTHOR
    parser.add_option("-a","--arg",
        dest = "myarg",
        action = "store_true",
        help = "arg by default False",
        default = False)
    try:
        (options, args) = parser.parse_args()
        if options.myarg:
            parser.error("myarg is True, error ;-)")
        screen = myterm.SCREEN
        for color in colorconsole.terminal.colors:
            screen.set_color(colorconsole.terminal.colors[color], myterm.BACKGROUND_DEFAULT)
            print(colorconsole.terminal.colors[color], color)
        screen.set_color(myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT)
        sys.exit()
    except Exception as e:
        parser.error(e)
        sys.exit(1)
