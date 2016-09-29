#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ReplaceCertRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'ReplaceCert', 'lb.api.qcloud.com')

	def get_oldCertId(self):
		return self.get_params().get('oldCertId')

	def set_oldCertId(self, oldCertId):
		self.add_param('oldCertId', oldCertId)

	def get_newCertId(self):
		return self.get_params().get('newCertId')

	def set_newCertId(self, newCertId):
		self.add_param('newCertId', newCertId)

	def get_newCertContent(self):
		return self.get_params().get('newCertContent')

	def set_newCertContent(self, newCertContent):
		self.add_param('newCertContent', newCertContent)

	def get_newCertName(self):
		return self.get_params().get('newCertName')

	def set_newCertName(self, newCertName):
		self.add_param('newCertName', newCertName)

	def get_newCertKey(self):
		return self.get_params().get('newCertKey')

	def set_newCertKey(self, newCertKey):
		self.add_param('newCertKey', newCertKey)

