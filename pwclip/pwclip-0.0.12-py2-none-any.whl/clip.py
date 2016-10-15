#!/usr/bin/env python3
"""
clipper - challenge-response to clipboard (mouse coupy/paste buffer)
"""
from sys import argv

from platform import system

from os import environ, \
    name as osname

from time import sleep

from binascii import hexlify

from tkinter import StringVar, Button, Entry, Frame, Label, Tk

from subprocess import Popen, PIPE

from yubico import \
    find_yubikey, yubikey, \
    yubico_exception

def yubikeys(ykser=None, dbg=None):
	"""
	return a list of yubikeys objects
	"""
	keys = {}
	for i in range(0, 255):
		try:
			key = find_yubikey(debug=dbg, skip=i)
		except yubikey.YubiKeyError:
			break
		if ykser and int(ykser) != int(key.serial()):
			continue
		keys[key.serial()] = key
	return keys

def slotchalres(yk, chal, slot):
	"""
	challenge-response function using with given
	challenge (chal) for slot on yubikey found by yubikeys()
	"""
	try:
		return hexlify(yk.challenge_response(
            chal.ljust(64, '\0').encode(), slot=slot)).decode()
	except yubico_exception.YubicoError:
		pass

def chalres(chal, slot=2, ykser=None):
	"""
	challenge-response function using specified slot
	or default (2) as wrapping function for yubikeys() and slotchalres()
	"""
	keys = yubikeys(ykser)
	for (_, key) in keys.items():
		return slotchalres(key, chal, slot)

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
			with Popen(['xsel', '-p', '-i'], stdin=PIPE) as prc:
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


def guipassclipper(wait=3):
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
			__r = chalres(self.pwd.get(), ykser=self.ykser)
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
