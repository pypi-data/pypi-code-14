#!/usr/bin/env python3

import sys
from os import getcwd

try:
	import pwclip
except ImportError:
	sys.path.append(getcwd())
	import pwclip

try:
	pwclip.pwclipper()
except KeyboardInterrupt:
	print('\naborted by keystroke')
	exit(0)
