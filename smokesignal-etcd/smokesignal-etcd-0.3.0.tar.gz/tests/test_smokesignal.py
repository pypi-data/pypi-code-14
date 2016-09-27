#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smokesignal
----------------------------------

Tests for `smokesignal` module.
"""

import pytest


from smokesignal import Client, Service, Backend


class TestBackend(object):
	def test_creation(self):
		b = Backend(host = 'example.com', port = 345)
		assert b.host == 'example.com'
		assert b.port == 345

	def test_missing_params(self):
		with pytest.raises(Exception):
			b = Backend(host='example.com')
		with pytest.raises(Exception):
			b = Backend(port=345)

	# def test_dump(self):
	# 	b = Backend(host = 'example.com', port = 345)
	# 	dumped = b.dump()
	# 	assert dumped == {'host': 'example.com', 'port': 345}


class TestService:
	def test_creation_http(self):
		s = Service(name = 'test')
		assert s.name == 'test'
		assert s.mode == 'http'
		s = Service(name = 'test', mode = 'http', subdomain = 'test', service_port=345)
		assert s.name == 'test'
		assert s.mode == 'http'
		assert s.service_port == None

	def test_creation_tcp(self):
		s = Service(name = 'test', mode = 'tcp', subdomain = 'test', service_port=345)
		assert s.name == 'test'
		assert s.mode == 'tcp'
		assert s.subdomain == 'test'
		assert s.service_port == 345

	def test_missing_params_http(self):
		with pytest.raises(Exception):
			s = Service()

	def test_missing_params_tcp(self):
		with pytest.raises(Exception):
			s = Service(name = 'test', mode = 'tcp', subdomain = 'test')

	# def test_dump(self):
	# 	s = Service(name = 'test', mode = 'http', subdomain = 'test', service_port=345)
	# 	assert s.dump() == {'route': 'test', 'mode': 'http'}
	# 	s = Service(name = 'test', mode = 'tcp', subdomain = 'test', service_port=345)
	# 	assert s.dump() == {'route': 'test', 'mode': 'tcp', 'service_port': 345}
	# 	s = Service(name = 'test', mode = 'tcp', service_port=345)
	# 	assert s.dump() == {'route': 'test', 'mode': 'tcp', 'service_port': 345}
	# 	s = Service(name = 'test', mode = 'tcp', subdomain = 'different', service_port=345)
	# 	assert s.dump() == {'route': 'different', 'mode': 'tcp', 'service_port': 345}
