#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ZhDeviceAvailableRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'ZhDeviceAvailable', 'bm.api.qcloud.com')

	def get_deviceClassCode(self):
		return self.get_params().get('deviceClassCode')

	def set_deviceClassCode(self, deviceClassCode):
		self.add_param('deviceClassCode', deviceClassCode)

	def get_module(self):
		return self.get_params().get('module')

	def set_module(self, module):
		self.add_param('module', module)

