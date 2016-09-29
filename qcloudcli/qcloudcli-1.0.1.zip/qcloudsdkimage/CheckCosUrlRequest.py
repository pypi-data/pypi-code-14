#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CheckCosUrlRequest(Request):

	def __init__(self):
		Request.__init__(self, 'image', 'qcloudcliV1', 'CheckCosUrl', 'image.api.qcloud.com')

	def get_cosUrl(self):
		return self.get_params().get('cosUrl')

	def set_cosUrl(self, cosUrl):
		self.add_param('cosUrl', cosUrl)

