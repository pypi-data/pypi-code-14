#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UploadCertRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'UploadCert', 'account.api.qcloud.com')

	def get_cert(self):
		return self.get_params().get('cert')

	def set_cert(self, cert):
		self.add_param('cert', cert)

	def get_certType(self):
		return self.get_params().get('certType')

	def set_certType(self, certType):
		self.add_param('certType', certType)

	def get_key(self):
		return self.get_params().get('key')

	def set_key(self, key):
		self.add_param('key', key)

	def get_alias(self):
		return self.get_params().get('alias')

	def set_alias(self, alias):
		self.add_param('alias', alias)

