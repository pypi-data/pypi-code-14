#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SetOutBandVPNAuthPwdRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'SetOutBandVPNAuthPwd', 'bm.api.qcloud.com')

	def get_appId(self):
		return self.get_params().get('appId')

	def set_appId(self, appId):
		self.add_param('appId', appId)

	def get_password(self):
		return self.get_params().get('password')

	def set_password(self, password):
		self.add_param('password', password)

	def get_createOrUpdate(self):
		return self.get_params().get('createOrUpdate')

	def set_createOrUpdate(self, createOrUpdate):
		self.add_param('createOrUpdate', createOrUpdate)

