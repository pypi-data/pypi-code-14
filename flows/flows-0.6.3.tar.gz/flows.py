#!/usr/bin/env python

'''
flows.py
Starter module
--------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
'''

import ast
import re
import sys

from flows import cli

_VERSION_RE = re.compile(r'__version__\s+=\s+(.*)')

with open('flows/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_VERSION_RE.search(
        f.read().decode('utf-8')).group(1)))

__author__ = "Davide Mastromatteo"
__copyright__ = "Copyright 2016, Davide Mastromatteo"
__credits__ = [""]
__license__ = "Apache-2.0"
__version__ = VERSION
__maintainer__ = "Davide Mastromatteo"
__email__ = "dave35@me.com"
__status__ = "Beta"

for arg in sys.argv:
    if arg == "--version":
        print("\nversion " + str(__version__) + "\n")

cli.main(sys.argv)
