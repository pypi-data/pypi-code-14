#!/usr/bin/env python3
"""
gpgtool module
"""
# -*- encoding: utf-8 -*-

# (std)lib imports
from os import \
    X_OK as _XOK, \
    access as _access, \
    getcwd as _getcwd, \
    environ as _environ

from os.path import \
    isfile as _isfile, \
    expanduser as _expanduser

from getpass import \
    getpass as _getpass

from gnupg import \
    GPG as _GPG

# local imports
from colortext import blu, red, yel, bgre, abort, error

class GPGTool(object):
	"""
	gnupg wrapper-wrapper :P
	although the gnupg module is quite handy and the functions are pretty and
	useable i need some modificated easing functions to be able to make the
	main code more easy to understand by wrapping multiple gnupg functions to
	one - also i can prepare some program related stuff in here
	"""
	_dbg = None
	_agt = True
	_homedir = _expanduser('~/.gnupg')
	_binary = '/usr/bin/gpg2'
	if not _isfile(_binary):
		_binary = '/usr/bin/gpg'
	if not _isfile(_binary) or not _access(_binary, _XOK):
		raise RuntimeError('%s needs to be executable'%_binary)
	agentinfo = '%s/S.gpg-agent'%_homedir
	kginput = {}
	def __init__(self, *args, **kwargs):
		for arg in args:
			arg = '_%s'%arg
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key) and not isinstance(val, bool):
				setattr(self, key, val)
		if self.dbg:
			lim = int(max(len(k) for k in GPGTool.__dict__.keys()))+4
			print('%s\n%s\n\n%s\n%s\n'%(
                GPGTool.__mro__,
                '\n'.join('  %s%s=    %s'%(
                    k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(GPGTool.__dict__.items())),
                GPGTool.__init__,
                '\n'.join('  %s%s=    %s'%(k, ' '*int(lim-len(k)), v
                ) for (k, v) in sorted(self.__dict__.items()))))
	@property                # dbg <bool>
	def dbg(self):
		"""bool"""
		return self._dbg
	@dbg.setter
	def dbg(self, val):
		self._dbg = bool(val)

	@property                # agt <bool>
	def agt(self):
		_environ['GPG_AGENT_INFO'] = self.agentinfo
		return self._agt
	@agt.setter
	def agt(self, val):
		self._agt = True if val else False

	@property                # homedir <str>
	def homedir(self):
		return self._homedir
	@homedir.setter
	def homedir(self, val):
		val = val if not val.startswith('~') else _expanduser(val)
		if not val.startswith('/'):
			val = '%s/%s'%(_getcwd(), val)
		self._homedir = val

	@property                # gpgbin <str>
	def binary(self):
		"""string"""
		return self._binary
	@binary.setter
	def binary(self, val):
		if _isfile(val) and _access(val, _XOK):
			self._binary = val

	@property                # keyring <str>
	def keyring(self):
		return '%s/pubring.kbx'%self.homedir \
            if self.binary.endswith('2') else '%s/pubring.kbx'%self.homedir

	@property                # secring <str>
	def secring(self):
		if self.binary.endswith('2') and self.keyring.endswith('gpg'):
			return '%s/secring.gpg'%self.homedir
		elif not self.binary.endswith('2'):
			return '%s/secring.gpg'%self.homedir
		return self.keyring

	@property                # _gpg_ <GPG>
	def _gpg_(self):
		"""object"""
		__g = _GPG(
            gnupghome=self.homedir, gpgbinary=self.binary,
            use_agent=self.agt, verbose=1 if self.dbg else 0,
            options=['--batch', '--pinentry-mode=loopback'],
            keyring=self.keyring, secret_keyring=self.secring)
		__g.encoding = 'utf-8'
		return __g

	@staticmethod
	def _passwd(rpt=False):
		"""
		password questioning function
		"""
		msg = 'enter new passphrase: '
		tru = 'repeat that passphrase: '
		while True:
			try:
				if not rpt:
					return _getpass(msg)
				__pwd = _getpass(msg)
				if __pwd == _getpass(tru):
					return __pwd
				error('passwords did not match')
			except KeyboardInterrupt:
				abort()

	def genkeys(self, **kginput):
		"""
		gpg-key-pair generator method
		"""
		if self.dbg:
			print(bgre(self.genkeys))
		kginput = kginput if kginput != {} else self.kginput
		if not kginput:
			error('no key-gen input received')
			return
		print(
            blu('generating new keys using:\n '),
            '\n  '.join('%s%s=  %s'%(
                blu(k),
                ' '*int(max(len(s) for s in kginput.keys())-len(k)+2),
                yel(v)
            ) for (k, v) in kginput.items()))
		if 'passphrase' in kginput.keys():
			if kginput['passphrase'] == 'nopw':
				del kginput['passphrase']
			elif kginput['passphrase'] == 'stdin':
				kginput['passphrase'] = self.__passwd(rpt=True)
		print(red('generating %s-bit keys - this WILL take some time'%(
            kginput['key_length'])))
		key = self._gpg_.gen_key(self._gpg_.gen_key_input(**kginput))
		if self.dbg:
			print('key has been generated:\n%s'%str(key))
		return key

	def findkey(self, pattern='', **kwargs):
		typ = 'A' if not 'typ' in kwargs.keys() else kwargs['typ']
		secret = False if not 'secret' in kwargs.keys() else kwargs['secret']
		keys = {}
		for key in self._gpg_.list_keys():
			if not [v for kv in key.values() for v in kv if pattern in v]:
				continue
			for (k, v) in key.items():
				#print(k, v)
				if k == 'subkeys':
					#print(k)
					for sub in key[k]:
						#print(sub)
						short, typs, finger = sub
						#print(finger, typs)
						if typ == 'A' or (typ in typs):
							si = key[k].index(sub)
							ki = key[k][si].index(finger)
							kstr = self._gpg_.export_keys(
                                key[k][si][ki], secret=secret)
							#print(kstr)
							keys[finger] = {typs: kstr}
		return keys

	def export(self, *patterns, **kwargs):
		"""
		key-export method
		"""
		if self.dbg:
			print(bgre(self.export))
		typ = 'A' if not 'typ' in kwargs.keys() else kwargs['typ']
		secret = False if not 'secret' in kwargs.keys() else kwargs['secret']
		keys = dict((k, v) for (k, v) in self.findkey(**kwargs).items())
		if patterns:
			keys = dict((k, v) for p in list(patterns) \
                for (k, v) in self.findkey(p, **kwargs).items())
		return keys

	def _encryptwithkeystr(self, message, keystr, output):
		for result in self._gpg_.import_keys(keystr).results:
			finger = result['fingerprint']
			return self._gpg_.encrypt(
                message, finger, always_trust=True, output=output)

	def encrypt(self, message, *args, **kwargs):
		"""
		text encrypting function
		"""
		if self.dbg:
			print(bgre(self.encrypt))
		fingers = [f for f in self.export(typ='e').keys()]
		if 'recipients' in kwargs.keys():
			fingers = [f for f in self.export(
                *kwargs['recipients'], **{typ: 'e'})]
		if 'keystr' in kwargs.keys():
			res = self._gpg_.import_keys(keystr).results[0]
			fingers = [res['fingerprint']]
		output = None if not 'output'in kwargs.keys() else kwargs['output']
		return self._gpg_.encrypt(
            message, fingers, always_trust=True, output=output)

	def decrypt(self, message, output=None):
		"""
		text decrypting function
		"""
		if self.dbg:
			print(bgre('%s\n  trying to decrypt:\n%s'%(self.decrypt, message)))
		return self._gpg_.decrypt(message, always_trust=True, output=output)
