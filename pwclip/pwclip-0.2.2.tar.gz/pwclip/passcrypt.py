#!/usr/bin/env python3

from os import path, uname, remove

from tarfile import open as taropen

from yaml import load, dump

from time import sleep

from tempfile import NamedTemporaryFile

from .colortext import error, fatal

from .userfind import userfind

from .gpg import GPGTool

class PassCrypt(GPGTool):
	dbg = False
	user = userfind()
	home = userfind(user, 'home')
	plain = '%s/.pwd.yaml'%home
	crypt = '%s/.pwdcrypt'%home
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		self._mergeplain_()
		if self.dbg:
			lim = int(max(len(k) for k in PassCrypt.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                PassCrypt.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(PassCrypt.__dict__.items())),
                PassCrypt.__init__,
                '\n'.join('  %s%s=    %s'%(k[1:], ' '*int(lim-len(k)), v
                    ) for (k, v) in sorted(self.__dict__.items()))))

	def _mergeplain_(self):
		__pws = self._readcrypt()
		if not __pws:
			__pws = {self.user:[{}]}
		if path.exists(self.plain):
			try:
				with open(self.plain, 'r') as pfh:
					__newpws = load(pfh.read())
				remove(self.plain)
			except FileNotFoundError:
				__newpws = {}
			for (k, v) in __newpws.items():
				__pws[k] = v
			self._writecrypt_(__pws)

	def _readcrypt(self):
		if self.dbg:
			print('%s\n  crypt = %s'%(self._readcrypt, self.crypt))
		if path.exists(self.crypt):
			with open(self.crypt, 'r') as vlt:
				crypt = vlt.read()
				return load(str(self.decrypt(crypt)))

	def _writecrypt_(self, plain):
		if self.dbg:
			print('%s\n  weaknez = %s'%(self._writecrypt, weaknez))
		__crypt = str(self.encrypt(dump(plain)))
		with open(self.crypt, 'w+') as vlt:
			vlt.write(__crypt)

	def adpw(self, usr, pwd=None):
		pwd = pwd if pwd else self._passwd()
		com = input('enter a comment: ')
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.adpw, user, pwd))
		try:
			__weak = load(self._readcrypt())
		except (TypeError, AttributeError):
			__weak = self._readcrypt()
		__weak[self.user][usr] = [pwd, com]
		return self._writecrypt(__weak)

	def chpw(self, usr, pwd=None):
		pwd = pwd if pwd else self._passwd()
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.chpw, usr, pwd))
		try:
			__weak = load(self._readcrypt())
		except (TypeError, AttributeError):
			__weak = self._readcrypt()
		__weak[self.user][usr] = pwd
		return self._writecrypt(__weak)

	def rmpw(self, usr):
		if self.dbg:
			print('%s\n  user = %s\n  deluser = %s'%(
                self.rmpw, self.user, usr))
		__weak = self._readcrypt()
		if __weak and usr in __weak.keys():
			del __weak[self.user][usr]
		return self._writecrypt(__weak)

	def lspw(self, usr=None, crypt=None):
		if self.dbg:
			print('%s\n  user = %s\n  getuser = %s'%(
                self.lspw, self.user, usr))
		__weaks = self._readcrypt()
		if __weaks:
			if self.user in __weaks.keys():
				__weaks = __weaks[self.user]
			if not usr:
				return __weaks
			for (u, p) in __weaks.items():
				if usr == u:
					return p

def passcrypt(usr):
	if usr:
		__entry = PassCrypt().lspw(usr)
		if __entry:
			return __entry[0]

if __name__ == '__main__':
    exit(1)
