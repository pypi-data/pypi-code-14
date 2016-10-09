# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from droigotools.rootcmd import rootCmdPath
from droigotools.rootcmd import rootInstance
from droigotools.cmdengine import ExcCMDError
import droigotools.cmdgolangproj

def main():
    try:
        print(rootCmdPath(rootInstance(), sys.argv[1:])())
    except ExcCMDError as e:
        print(str(e))
