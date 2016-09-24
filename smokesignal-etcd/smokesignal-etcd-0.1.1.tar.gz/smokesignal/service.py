# -*- coding: utf-8 -*-

class Backend:
	def __init__(self, host = None, port = None, **kwargs):

		if not host or not port:
			raise Exception('You must provide a host and port!')

		self.host = host
		self.port = port

	def __eq__(self, other):
		if self.host == getattr(other, 'host', None) and self.port == getattr(other, 'port', None):
			return True
		return False

	def dump(self):
		payload = dict(
				host = self.host,
				port = self.port,
				)

		return payload

	def __repr__(self):
		return '<Backend host:"%s" port:"%s">'%(self.host, self.port)

class Service:
	def __init__(self, name = None, mode = 'http', subdomain = None, service_port = None, **kwargs):
		if not name and not kwargs.get('route', False):
			raise Exception('You must provide a name!')
		self.name = name
		self.mode = mode
		if mode == 'tcp':
			if not service_port:
				raise Exception('You must provide a service_port')
			self.subdomain = subdomain
			self.service_port = service_port
		else:
			self.subdomain = None
			self.service_port = None

		self._backends = []

		if kwargs.get('backends', False):
			for b in kwargs['backends']:
				self.addBackend(**b)

		if kwargs.get('route', False):
			self.name = kwargs['route']
			if mode == 'tcp':
				self.subdomain = kwargs['route']

	def addBackend(self, backend = None, host = None, port = None, **kwargs):
		if backend:
			self._backends.append(backend)
		elif host and port:
			self._backends.append(Backend(host, port))
		else:
			return False
		return True

	def __eq__(self, other):
		if self.name == getattr(other, 'name', None):
			return True
		return False

	def __repr__(self):
		begin = '<Service name:"%s" mode:"%s" '%(self.name, self.mode)
		if self.mode == 'http':
			mid = ''
		elif self.mode == 'tcp':
			mid = 'service_port:"%s" '%self.service_port
			if self.subdomain:
				mid = mid + 'subdomain:"%s" '%self.subdomain

		return begin + mid + 'backends:[%s]>'%', '.join([str(x) for x in self._backends])

	@property
	def backends(self):
		for backend in self._backends:
			yield backend

	def dump(self):
		payload = dict(
			route = self.name,
			mode = self.mode,
		)
		if self.subdomain:
			payload['route'] = self.subdomain
		if self.service_port:
			payload['service_port'] = self.service_port
		return payload
