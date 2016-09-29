#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeOpLogsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'DescribeOpLogs', 'account.api.qcloud.com')

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

	def get_status(self):
		return self.get_params().get('status')

	def set_status(self, status):
		self.add_param('status', status)

	def get_ifNeedDetail(self):
		return self.get_params().get('ifNeedDetail')

	def set_ifNeedDetail(self, ifNeedDetail):
		self.add_param('ifNeedDetail', ifNeedDetail)

	def get_startTime(self):
		return self.get_params().get('startTime')

	def set_startTime(self, startTime):
		self.add_param('startTime', startTime)

	def get_endTime(self):
		return self.get_params().get('endTime')

	def set_endTime(self, endTime):
		self.add_param('endTime', endTime)

	def get_command(self):
		return self.get_params().get('command')

	def set_command(self, command):
		self.add_param('command', command)

	def get_orderBy(self):
		return self.get_params().get('orderBy')

	def set_orderBy(self, orderBy):
		self.add_param('orderBy', orderBy)

	def get_orderType(self):
		return self.get_params().get('orderType')

	def set_orderType(self, orderType):
		self.add_param('orderType', orderType)

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

	def get_instanceType(self):
		return self.get_params().get('instanceType')

	def set_instanceType(self, instanceType):
		self.add_param('instanceType', instanceType)

