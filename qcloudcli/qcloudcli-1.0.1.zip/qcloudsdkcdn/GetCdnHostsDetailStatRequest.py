#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCdnHostsDetailStatRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetCdnHostsDetailStat', 'cdn.api.qcloud.com')

	def get_date(self):
		return self.get_params().get('date')

	def set_date(self, date):
		self.add_param('date', date)

	def get_projects(self):
		return self.get_params().get('projects')

	def set_projects(self, projects):
		self.add_param('projects', projects)

	def get_hosts(self):
		return self.get_params().get('hosts')

	def set_hosts(self, hosts):
		self.add_param('hosts', hosts)

	def get_sources(self):
		return self.get_params().get('sources')

	def set_sources(self, sources):
		self.add_param('sources', sources)

