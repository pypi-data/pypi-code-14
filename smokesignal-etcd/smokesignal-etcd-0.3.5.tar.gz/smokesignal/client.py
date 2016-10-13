# -*- coding: utf-8 -*-

from smokesignal.service import Service, Backend

import etcd
import hashlib
import json
import logging

moduleLogger = logging.getLogger(__name__)
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
		self._services = set()

	def _hash(self, text):
		return hashlib.sha1(text.encode('utf-8')).hexdigest()

	def _push(self):
		for service in self._services:
			path = '/'.join([self._root, self._hash(service.name)])
			data = service.dump()
			self._client.write(path, json.dumps(data), ttl = self._ttl)

	def _pull(self):
		try:
			moduleLogger.debug('pulling services')
			raw = self._client.read(self._root, recursive = True, sorted=True)
		except etcd.EtcdKeyNotFound:
			moduleLogger.error('etcd key not found!')
			return
		rawServices = [x for x in raw.get_subtree() if not x.key == self._root ]
		if rawServices:
			self._services = set()
		for service in rawServices:
			data = json.loads(service.value)
			moduleLogger.debug('adding service %s'%data)
			self._addService(Service(**data))

	def _addService(self, service):
		services = list(self._services)
		services.append(service)
		self._services = set(services)

	def register(self, service = None, name = None, **kwargs):
		if isinstance(service, Service):
			self._addService(service)
			return True
		else:
			for service in self._services:
				if service.name == name:
					service.addBackend(**kwargs)
					return True
		srvc = Service(name, **kwargs)
		srvc.addBackend(**kwargs)
		self._addService(srvc)
		return True

	@property
	def services(self):
		self._pull()
		for service in self._services:
			yield service

	def push(self):
		self._push()
