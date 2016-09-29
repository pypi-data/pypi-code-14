#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class QueryDeviceUserRequest(Request):

	def __init__(self):
		Request.__init__(self, 'iot', 'qcloudcliV1', 'QueryDeviceUser', 'iot.api.qcloud.com')

	def get_userName(self):
		return self.get_params().get('userName')

	def set_userName(self, userName):
		self.add_param('userName', userName)

