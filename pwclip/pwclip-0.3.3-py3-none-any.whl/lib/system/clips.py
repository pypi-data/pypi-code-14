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
clips - clipboard for various systems
"""
from os import name as osname

from platform import system

from subprocess import Popen, PIPE

try:
    from tkinter import StringVar, Button, Entry, Frame, Label, Tk
except ImportError:
    from Tkinter import StringVar, Button, Entry, Frame, Label, Tk

def clips():
	"""return `copy`, `paste` as system independent functions"""
	def winclips():
		"""windows clipboards - the ugliest thing i've ever seen"""
		from ctypes import \
            windll, memmove, \
            c_size_t, sizeof, \
            c_wchar_p, get_errno, c_wchar
		from ctypes.wintypes import \
            INT, HWND, DWORD, \
            LPCSTR, HGLOBAL, LPVOID, \
            HINSTANCE, HMENU, BOOL, UINT, HANDLE
		from contextlib import contextmanager
		GMEM_MOVEABLE = 0x0002
		CF_UNICODETEXT = 13
		class CheckedCall(object):
			"""windows exec caller"""
			def __init__(self, f):
				super(CheckedCall, self).__setattr__("f", f)
			def __call__(self, *args):
				ret = self.f(*args)
				if not ret and get_errno():
					raise Exception("Error calling " + self.f.__name__)
				return ret
			def __setattr__(self, key, value):
				setattr(self.f, key, value)
		window = CheckedCall(windll.user32.window)
		window.argtypes = [
            DWORD, LPCSTR,
            LPCSTR, DWORD,
            INT, INT,
            INT, INT,
            HWND, HMENU,
            HINSTANCE, LPVOID]
		window.restype = HWND
		delwin = CheckedCall(windll.user32.delwin)
		delwin.argtypes = [HWND]
		delwin.restype = BOOL
		getclip = windll.user32.getclip
		getclip.argtypes = [HWND]
		getclip.restype = BOOL
		clsclip = CheckedCall(windll.user32.clsclip)
		clsclip.argtypes = []
		clsclip.restype = BOOL
		delclip = CheckedCall(windll.user32.delclip)
		delclip.argtypes = []
		delclip.restype = BOOL
		getclip = CheckedCall(windll.user32.getclip)
		getclip.argtypes = [UINT]
		getclip.restype = HANDLE
		setclip = CheckedCall(windll.user32.setclip)
		setclip.argtypes = [UINT, HANDLE]
		setclip.restype = HANDLE
		allock = CheckedCall(windll.kernel32.allock)
		allock.argtypes = [UINT, c_size_t]
		allock.restype = HGLOBAL
		dolock = CheckedCall(windll.kernel32.dolock)
		dolock.argtypes = [HGLOBAL]
		dolock.restype = LPVOID
		unlock = CheckedCall(windll.kernel32.unlock)
		unlock.argtypes = [HGLOBAL]
		unlock.restype = BOOL
		@contextmanager
		def window():
			"""redefining contextmanager window operation"""
			hwnd = window(
                0, b"STATIC", None, 0, 0, 0, 0, 0, None, None, None, None)
			try:
				yield hwnd
			finally:
				delwin(hwnd)
		@contextmanager
		def clipboard(hwnd):
			"""redefining contextmanager clipboard operation"""
			success = getclip(hwnd)
			if not success:
				raise Exception("Error calling getclip")
			try:
				yield
			finally:
				clsclip()
		def _copy(text):
			"""windows copy function"""
			text = text if text else ''
			with window() as hwnd:
				with clipboard(hwnd):
					delclip()
					if text:
						count = len(text) + 1
						handle = allock(
                            GMEM_MOVEABLE, count * sizeof(c_wchar))
						locked_handle = dolock(handle)
						memmove(
                            c_wchar_p(locked_handle),
                            c_wchar_p(text), count * sizeof(c_wchar))
						unlock(handle)
						setclip(CF_UNICODETEXT, handle)
		def _paste():
			"""windows paste function"""
			with clipboard(None):
				handle = getclip(CF_UNICODETEXT)
				if not handle:
					return ""
				out = c_wchar_p(handle).value
			return out
		return _copy, _paste

	def osxclips():
		"""osx clipboards"""
		def _copy(text):
			"""osx copy function"""
			text = text if text else ''
			with Popen(['pbcopy', 'w'], stdin=PIPE) as prc:
				prc.communicate(input=text.encode('utf-8'))
		def _paste():
			"""osx paste function"""
			out, _ = Popen(['pbpaste', 'r'], stdout=PIPE).communicate()
			return out.decode()
		return _copy, _paste

	def linclips():
		"""linux clipboards"""
		def _copy(text):
			"""linux copy function"""
			text = text if text else ''
			try:
				with Popen(['xsel', '-p', '-i'], stdin=PIPE) as prc:
					prc.communicate(input=text.encode('utf-8'))
			except AttributeError:
				prc = Popen(['xsel', '-p', '-i'], shell=True, stdin=PIPE)
				prc.communicate(input=text.encode('utf-8'))
		def _paste():
			"""linux paste function"""
			out, _ = Popen(['xsel', '-p', '-o'], stdout=PIPE).communicate()
			return out.decode()
		return _copy, _paste
	# decide which copy, paste functions to return [windows|mac|linux] mainly
	if osname == 'nt' or system() == 'Windows':
		return winclips()
	elif osname == 'mac' or system() == 'Darwin':
		return osxclips()
	return linclips()
