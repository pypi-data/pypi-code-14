#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
#
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""
pwclip - password to clipboard (mouse coupy/paste buffer) manager
"""
from sys import argv

from os import environ, fork

from time import sleep

try:
	from tkinter import StringVar, Button, Entry, Frame, Label, Tk
except ImportError:
	from Tkinter import StringVar, Button, Entry, Frame, Label, Tk

from system import clips, inputgui, xnotify
from cypher import ykchalres, passcrypt

def clipgui(mode='yk', wait=3):
	"""gui representing function"""
	copy, paste = clips()
	wait = int(wait)
	oclp = paste()
	__input = inputgui()
	if mode == 'yk':
		__res = ykchalres(__input)
	elif mode == 'pc':
		__res = passcrypt(__input)
		if __res:
			if len(__res) == 2:
				xnotify(__res[1])
			__res = __res[0]
	copy(__res if __res else __input)
	if oclp != paste():
		try:
			sleep(wait)
		finally:
			copy(oclp)
