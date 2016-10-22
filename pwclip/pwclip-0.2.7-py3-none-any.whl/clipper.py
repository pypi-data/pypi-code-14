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

from system import clips
from cypher import ykchalres, passcrypt

def clipgui(mode='yk', wait=3):
	"""gui representing function"""
	copy, paste = clips()
	wait = int(wait)
	oclp = paste()
	class PassClip(Frame):
		"""password clipping class for tkinter.Frame"""
		pwd = ''
		ykser = ''
		if 'YKSERIAL' in environ.keys():
			ykser = environ['YKSERIAL']
		def __init__(self, master):
			Frame.__init__(self, master)
			self.pack()
			self.passwindow()
		def _enterexit(self, _=None):
			"""exit by saving challenge-response for input"""
			if mode == 'yk':
				__r = ykchalres(self.pwd.get(), ykser=self.ykser)
			elif mode == 'pc':
				__r = passcrypt(self.pwd.get())
			copy(__r if __r else self.pwd.get())
			self.quit()
		def _exit(self, _=None):
			"""just exit (for ESC mainly)"""
			self.quit()
		def passwindow(self):
			"""password input window creator"""
			self.lbl = Label(self, text="input will not be displayed")
			self.entry = Entry(self, show="*")
			self.entry.bind("<Return>", self._enterexit)
			self.entry.bind("<Escape>", self._exit)
			self.entry.pack()
			self.entry.focus_set()
			self.pwd = StringVar()
			self.entry["textvariable"] = self.pwd
			self.ok = Button(self)
			self.ok["text"] = "ok"
			self.ok["command"] = self._enterexit
			self.ok.pack(side="left")
			self.cl = Button(self)
			self.cl["text"] = "cancel"
			self.cl["command"] = self.quit
			self.cl.pack(side="right")
	# instanciate Tk and create window
	root = Tk()
	pwc = PassClip(root)
	pwc.lift()
	pwc.mainloop()
	root.destroy()
	if oclp != paste():
		try:
			sleep(wait)
		finally:
			copy(oclp)
