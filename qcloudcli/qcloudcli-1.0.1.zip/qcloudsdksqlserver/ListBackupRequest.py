#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ListBackupRequest(Request):

	def __init__(self):
		Request.__init__(self, 'sqlserver', 'qcloudcliV1', 'ListBackup', 'sqlserver.api.qcloud.com')

	def get_resourceId(self):
		return self.get_params().get('resourceId')

	def set_resourceId(self, resourceId):
		self.add_param('resourceId', resourceId)

	def get_startTime(self):
		return self.get_params().get('startTime')

	def set_startTime(self, startTime):
		self.add_param('startTime', startTime)

	def get_endTime(self):
		return self.get_params().get('endTime')

	def set_endTime(self, endTime):
		self.add_param('endTime', endTime)

	def get_pageSize(self):
		return self.get_params().get('pageSize')

	def set_pageSize(self, pageSize):
		self.add_param('pageSize', pageSize)

	def get_pageNo(self):
		return self.get_params().get('pageNo')

	def set_pageNo(self, pageNo):
		self.add_param('pageNo', pageNo)

