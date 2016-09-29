# -*- coding: utf-8 -*-
import hashlib
from smokesignal.errors import BackendCreationError, ServiceCreationError
from collections import OrderedDict
class Backend:
	def __init__(self, host = None, port = None, **kwargs):

		if not host or not port:
			raise BackendCreationError('No host or port provided!')

		self.host = host
		self.port = port
		self.uuid = hashlib.md5((self.host + str(self.port)).encode('utf-8')).hexdigest()

	def __eq__(self, other):
		if self.host == getattr(other, 'host', None) and self.port == getattr(other, 'port', None):
			return True
		return False

	def dump(self):
		payload = dict(
				host = self.host,
				port = self.port,
				id = self.uuid,
				)

		return payload

	def __repr__(self):
		return '<Backend host:"%s" port:"%s">'%(self.host, self.port)

class Service:
	def __init__(self, name = None, mode = 'http', subdomain = None, uri = None, service_port = None, **kwargs):
		if not name:
			raise ServiceCreationError('You must provide a name')
		self.name = name
		self.mode = mode
		self.uri = uri
		self.subdomain = subdomain

		if mode == 'tcp':
			if not service_port:
				raise ServiceCreationError('You must provide a service_port')
			else:
				self.service_port = service_port
		else:
			self.service_port = None

		self._backends = []
		self._numBackends = 0

		if kwargs.get('backends', False):
			for b in kwargs['backends']:
				self.addBackend(**b)

		self.uuid = hashlib.md5(self.name.encode('utf-8')).hexdigest()

	def addBackend(self, backend = None, host = None, port = None, **kwargs):
		if backend:
			self._backends.append(backend)
		elif host and port:
			self._backends.append(Backend(host, port))
		else:
			return False
		self._numBackends = self._numBackends + 1
		return True

	def __eq__(self, other):
		if self.name == getattr(other, 'name', None):
			return True
		return False

	def __hash__(self):
		return hash(self.name)

	def __repr__(self):
		rep = '<Service name:"%s" mode:"%s" '%(self.name, self.mode)
		if self.uri:
			rep = rep + 'uri: %s'%self.uri
		if self.mode == 'tcp':
			rep = rep + 'service_port:"%s" '%self.service_port
		if self.subdomain:
			rep = rep + 'subdomain:"%s" '%self.subdomain
		return rep+ 'backends:[%s]>'%', '.join([str(x) for x in self._backends])

	@property
	def backends(self):
		for backend in self._backends:
			yield backend

	def dump(self):
		payload = OrderedDict(
			name = self.name,
			mode = self.mode,
			id = self.uuid,
		)
		if self.subdomain:
			payload['subdomain'] = self.subdomain
		if self.uri:
			payload['uri'] = self.uri
		if self.mode == 'tcp' and self.service_port:
			payload['service_port'] = self.service_port
		backends = [x.dump() for x in self._backends]
		payload['backends'] = backends
		return payload
