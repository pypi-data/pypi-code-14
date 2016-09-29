#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InitUploadRequest(Request):

	def __init__(self):
		Request.__init__(self, 'fileserver', 'qcloudcliV1', 'InitUpload', 'fileserver.api.qcloud.com')

	def get_product(self):
		return self.get_params().get('product')

	def set_product(self, product):
		self.add_param('product', product)

	def get_fileName(self):
		return self.get_params().get('fileName')

	def set_fileName(self, fileName):
		self.add_param('fileName', fileName)

	def get_length(self):
		return self.get_params().get('length')

	def set_length(self, length):
		self.add_param('length', length)

	def get_mdfive(self):
		return self.get_params().get('mdfive')

	def set_mdfive(self, mdfive):
		self.add_param('mdfive', mdfive)

