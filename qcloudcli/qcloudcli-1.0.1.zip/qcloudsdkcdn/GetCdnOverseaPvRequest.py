#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCdnOverseaPvRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetCdnOverseaPv', 'cdn.api.qcloud.com')

	def get_date(self):
		return self.get_params().get('date')

	def set_date(self, date):
		self.add_param('date', date)

	def get_host(self):
		return self.get_params().get('host')

	def set_host(self, host):
		self.add_param('host', host)

