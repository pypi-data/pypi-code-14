#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ProtectHotlinksRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'ProtectHotlinks', 'cdn.api.qcloud.com')

	def get_host(self):
		return self.get_params().get('host')

	def set_host(self, host):
		self.add_param('host', host)

	def get_action(self):
		return self.get_params().get('action')

	def set_action(self, action):
		self.add_param('action', action)

	def get_key(self):
		return self.get_params().get('key')

	def set_key(self, key):
		self.add_param('key', key)

