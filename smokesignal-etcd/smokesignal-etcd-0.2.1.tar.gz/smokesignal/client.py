# -*- coding: utf-8 -*-

from smokesignal.service import Service, Backend
import etcd
import hashlib
import json

class Client:
	def __init__(self, host = None, port = 2379, dns = None, root = '/services', ttl = None):
		if host:
			self._client = etcd.Client(host = host, port = port)
		elif dns:
			self._client = etcd.Client(srv_domain = dns, allow_reconnect = True)
		else:
			raise Exception('You must provide either a host or domain!')

		self._root = root
		self._ttl = ttl
		self._services = []

	def _hash(self, text):
		return hashlib.sha1(text.encode('utf-8')).hexdigest()

	def _push(self):
		for service in self._services:
			path = '/'.join([self._root, self._hash(service.name)])
			data = service.dump()
			self._client.write(path, json.dumps(data), ttl = self._ttl)

	def _pull(self):
		self._services = []
		try:
			raw = self._client.read(self._root, recursive = True, sorted=True)
		except etcd.EtcdKeyNotFound:
			return
		rawServices = [x for x in raw.get_subtree() if not x.key == self._root ]
		for service in rawServices:
			data = json.loads(service.value)
			self._services.append(Service(**data))

	def register(self, name, **kwargs):
		for service in self._services:
			if service.name == name:
				service.addBackend(**kwargs)
				return
		srvc = Service(name, **kwargs)
		self._services.append(srvc)
		srvc.addBackend(**kwargs)

	@property
	def services(self):
		self._pull()
		for service in self._services:
			yield service

	def push(self):
		self._push()
