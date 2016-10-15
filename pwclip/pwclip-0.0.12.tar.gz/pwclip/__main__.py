#!/usr/bin/env python3

import sys
from os import environ

import pwclip


PWCLIPTIME = 3
if len(sys.argv) > 1:
	PWCLIPTIME = int(sys.argv[1])
elif 'PWCLIPTIME' in environ.keys():
	PWCLIPTIME = int(environ['PWCLIPTIME'])
try:
	pwclip.pwclipper(PWCLIPTIME)
except KeyboardInterrupt:
	print('\naborted by keystroke')
	exit(0)
