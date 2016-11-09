#!/usr/bin/env python

from os import sys, path

if __package__ == '':
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from main import *
else:
    from .main import *

main()
