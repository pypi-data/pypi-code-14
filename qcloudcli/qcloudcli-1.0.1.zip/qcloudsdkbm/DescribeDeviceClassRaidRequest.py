#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeDeviceClassRaidRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeDeviceClassRaid', 'bm.api.qcloud.com')

	def get_deviceClass(self):
		return self.get_params().get('deviceClass')

	def set_deviceClass(self, deviceClass):
		self.add_param('deviceClass', deviceClass)

