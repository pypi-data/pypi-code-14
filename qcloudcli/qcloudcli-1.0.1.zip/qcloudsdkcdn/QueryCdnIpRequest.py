#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class QueryCdnIpRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'QueryCdnIp', 'cdn.api.qcloud.com')

	def get_ips(self):
		return self.get_params().get('ips')

	def set_ips(self, ips):
		self.add_param('ips', ips)

