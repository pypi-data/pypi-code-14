#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SetHttpsInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'SetHttpsInfo', 'cdn.api.qcloud.com')

	def get_host(self):
		return self.get_params().get('host')

	def set_host(self, host):
		self.add_param('host', host)

	def get_httpsType(self):
		return self.get_params().get('httpsType')

	def set_httpsType(self, httpsType):
		self.add_param('httpsType', httpsType)

	def get_cert(self):
		return self.get_params().get('cert')

	def set_cert(self, cert):
		self.add_param('cert', cert)

	def get_privateKey(self):
		return self.get_params().get('privateKey')

	def set_privateKey(self, privateKey):
		self.add_param('privateKey', privateKey)

