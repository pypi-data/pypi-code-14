#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class AddPanshiWhiteListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'AddPanshiWhiteList', 'account.api.qcloud.com')

	def get_type(self):
		return self.get_params().get('type')

	def set_type(self, type):
		self.add_param('type', type)

	def get_targetUin(self):
		return self.get_params().get('targetUin')

	def set_targetUin(self, targetUin):
		self.add_param('targetUin', targetUin)

