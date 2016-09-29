#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class RenewInstanceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'SDK_PYTHON_1.1', 'RenewInstance', 'cvm.api.qcloud.com')

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)
		
	def get_period(self):
		return self.get_params().get('period')

	def set_period(self, period):
		self.add_param('period', period)

