#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetBatchLogUrlRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetBatchLogUrl', 'cdn.api.qcloud.com')

	def get_date(self):
		return self.get_params().get('date')

	def set_date(self, date):
		self.add_param('date', date)

	def get_index(self):
		return self.get_params().get('index')

	def set_index(self, index):
		self.add_param('index', index)

