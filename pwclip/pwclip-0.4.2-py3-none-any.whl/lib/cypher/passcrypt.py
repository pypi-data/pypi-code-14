#!/usr/bin/env python3

from os import path, uname, remove, environ

from tarfile import open as taropen

from yaml import load, dump

from time import sleep

from tempfile import NamedTemporaryFile

from colortext import tabd, error, fatal

from system import userfind

from cypher.gpg import GPGTool

from cypher.yubi import ykchalres

class PassCrypt(GPGTool):
	dbg = False
	aal = False
	sho = False
	user = userfind()
	home = userfind(user, 'home')
	plain = '%s/.pwd.yaml'%home
	crypt = '%s/.passcrypt'%home
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		__weaks = self._readcrypt()
		self.__weaks = __weaks if __weaks else {}
		try:
			with open(self.plain, 'r') as pfh:
				__newpws = load(pfh.read())
			remove(self.plain)
		except FileNotFoundError:
			__newpws = {}
		if __weaks and __newpws:
			for (k, v) in __newpws.items():
				__weaks[k] = v
		if __weaks != self.__weaks:
			self.__weaks = __weaks
			self._writecrypt_(__weaks)

	def _findentry(self, pattern, weaks=None):
		__weaks = weaks if weaks else self.__weaks
		for (u, p) in __weaks.items():
			if pattern == u or (
                  len(p) == 2 and len(pattern) > 1 and pattern in p[1]):
				return p

	def _readcrypt(self):
		if self.dbg:
			print('%s\n  crypt = %s'%(self._readcrypt, self.crypt))
		if path.exists(self.crypt):
			with open(self.crypt, 'r') as vlt:
				crypt = vlt.read()
			return load(str(self.decrypt(crypt)))

	def _writecrypt_(self, plain):
		if self.dbg:
			print('%s\n  weaknez = %s'%(self._writecrypt, plain))
		kwargs = {'output': self.crypt}
		if 'GPGKEYS' in environ.keys():
			kwargs['recipients'] = environ['GPGKEYS'].split(' ')
		elif 'GPGKEY' in environ.keys():
			kwargs['recipients'] = [environ['GPGKEY']]
		self.__weaks = plain
		self.encrypt(dump(self.__weaks), **kwargs)

	def adpw(self, usr, pwd=None):
		pwdcom = [pwd if pwd else self._passwd()]
		com = input('enter a comment: ')
		if com:
			pwdcom.append(com)
		if self.dbg:
			print('%s\n adduser = %s addpass = %s'%(
                self.adpw, usr, pwd))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys():
			__weak[self.user][usr] = pwdcom
			self._writecrypt_(__weak)
			return True

	def chpw(self, usr, pwd=None):
		pwdcom = [pwd if pwd else self._passwd()]
		com = input('enter a comment: ')
		if com:
			pwdcom.append(com)
		if self.dbg:
			print('%s\n adduser = %s addpass, comment = %s'%(
                self.chpw, usr, pwdcom))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys() and \
              usr in __weak[self.user].keys():
			__weak[self.user][usr] = pwdcom
			self._writecrypt_(__weak)
			return True

	def rmpw(self, usr):
		if self.dbg:
			print('%s\n  user = %s\n  deluser = %s'%(
                self.rmpw, self.user, usr))
		__weak = self._readcrypt()
		if __weak and self.user in __weak.keys() and \
              usr in __weak[self.user].keys():
			del __weak[self.user][usr]
			self._writecrypt_(__weak)
			return True

	def lspw(self, usr=None, aal=None, display=None):
		if self.dbg:
			print('%s\n  user = %s\n  getuser = %s'%(
                self.lspw, self.user, usr))
		aal = True if aal else self.aal
		sho = True if display else self.sho
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					for (user, entrys) in self.__weaks.items():
						__match = self._findentry(usr, self.__weaks[user])
						if __match:
							__ents = {usr: __match}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr:
					__ents = {usr: self._findentry(usr, __ents)}
			return __ents

def passcrypt(usr):
	if usr:
		return PassCrypt().lspw(usr)

if __name__ == '__main__':
    exit(1)
