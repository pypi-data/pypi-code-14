#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetAppCvmOverviewDeviceListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'GetAppCvmOverviewDeviceList', 'cvm.api.qcloud.com')

	def get_deviceType(self):
		return self.get_params().get('deviceType')

	def set_deviceType(self, deviceType):
		self.add_param('deviceType', deviceType)

	def get_startNum(self):
		return self.get_params().get('startNum')

	def set_startNum(self, startNum):
		self.add_param('startNum', startNum)

	def get_endNum(self):
		return self.get_params().get('endNum')

	def set_endNum(self, endNum):
		self.add_param('endNum', endNum)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

