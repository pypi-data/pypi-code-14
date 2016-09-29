#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetPeakUsageByDayRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetPeakUsageByDay', 'cdn.api.qcloud.com')

	def get_domain(self):
		return self.get_params().get('domain')

	def set_domain(self, domain):
		self.add_param('domain', domain)

	def get_time(self):
		return self.get_params().get('time')

	def set_time(self, time):
		self.add_param('time', time)

