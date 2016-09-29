#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetDeviceOutBandInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'GetDeviceOutBandInfo', 'bm.api.qcloud.com')

	def get_appId(self):
		return self.get_params().get('appId')

	def set_appId(self, appId):
		self.add_param('appId', appId)

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

