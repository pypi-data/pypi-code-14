#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetPushLogsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetPushLogs', 'cdn.api.qcloud.com')

	def get_date(self):
		return self.get_params().get('date')

	def set_date(self, date):
		self.add_param('date', date)

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_taskId(self):
		return self.get_params().get('taskId')

	def set_taskId(self, taskId):
		self.add_param('taskId', taskId)

	def get_keyword(self):
		return self.get_params().get('keyword')

	def set_keyword(self, keyword):
		self.add_param('keyword', keyword)

	def get_status(self):
		return self.get_params().get('status')

	def set_status(self, status):
		self.add_param('status', status)

	def get_startDate(self):
		return self.get_params().get('startDate')

	def set_startDate(self, startDate):
		self.add_param('startDate', startDate)

	def get_endDate(self):
		return self.get_params().get('endDate')

	def set_endDate(self, endDate):
		self.add_param('endDate', endDate)

	def get_hosts(self):
		return self.get_params().get('hosts')

	def set_hosts(self, hosts):
		self.add_param('hosts', hosts)

