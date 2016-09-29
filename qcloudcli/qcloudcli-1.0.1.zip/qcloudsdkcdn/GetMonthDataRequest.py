#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetMonthDataRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetMonthData', 'cdn.api.qcloud.com')

	def get_month(self):
		return self.get_params().get('month')

	def set_month(self, month):
		self.add_param('month', month)

	def get_projects(self):
		return self.get_params().get('projects')

	def set_projects(self, projects):
		self.add_param('projects', projects)

	def get_hosts(self):
		return self.get_params().get('hosts')

	def set_hosts(self, hosts):
		self.add_param('hosts', hosts)

