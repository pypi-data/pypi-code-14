#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCertListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'GetCertList', 'account.api.qcloud.com')

	def get_page(self):
		return self.get_params().get('page')

	def set_page(self, page):
		self.add_param('page', page)

	def get_count(self):
		return self.get_params().get('count')

	def set_count(self, count):
		self.add_param('count', count)

	def get_searchKey(self):
		return self.get_params().get('searchKey')

	def set_searchKey(self, searchKey):
		self.add_param('searchKey', searchKey)

	def get_certType(self):
		return self.get_params().get('certType')

	def set_certType(self, certType):
		self.add_param('certType', certType)

	def get_id(self):
		return self.get_params().get('id')

	def set_id(self, id):
		self.add_param('id', id)

	def get_withCert(self):
		return self.get_params().get('withCert')

	def set_withCert(self, withCert):
		self.add_param('withCert', withCert)

