#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateDeviceUserRequest(Request):

	def __init__(self):
		Request.__init__(self, 'iot', 'qcloudcliV1', 'CreateDeviceUser', 'iot.api.qcloud.com')

	def get_userNameFix(self):
		return self.get_params().get('userNameFix')

	def set_userNameFix(self, userNameFix):
		self.add_param('userNameFix', userNameFix)

