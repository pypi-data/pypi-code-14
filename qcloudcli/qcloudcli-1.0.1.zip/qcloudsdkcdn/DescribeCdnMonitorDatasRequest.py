#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeCdnMonitorDatasRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'DescribeCdnMonitorDatas', 'cdn.api.qcloud.com')

	def get_domains(self):
		return self.get_params().get('domains')

	def set_domains(self, domains):
		self.add_param('domains', domains)

	def get_startTime(self):
		return self.get_params().get('startTime')

	def set_startTime(self, startTime):
		self.add_param('startTime', startTime)

	def get_endTime(self):
		return self.get_params().get('endTime')

	def set_endTime(self, endTime):
		self.add_param('endTime', endTime)

	def get_format(self):
		return self.get_params().get('format')

	def set_format(self, format):
		self.add_param('format', format)

	def get_keys(self):
		return self.get_params().get('keys')

	def set_keys(self, keys):
		self.add_param('keys', keys)

