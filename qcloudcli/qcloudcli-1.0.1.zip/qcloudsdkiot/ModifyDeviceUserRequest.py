#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyDeviceUserRequest(Request):

	def __init__(self):
		Request.__init__(self, 'iot', 'qcloudcliV1', 'ModifyDeviceUser', 'iot.api.qcloud.com')

	def get_userName(self):
		return self.get_params().get('userName')

	def set_userName(self, userName):
		self.add_param('userName', userName)

	def get_password(self):
		return self.get_params().get('password')

	def set_password(self, password):
		self.add_param('password', password)

