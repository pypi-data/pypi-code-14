#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CheckLoginRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'CheckLogin', 'account.api.qcloud.com')

	def get_uin(self):
		return self.get_params().get('uin')

	def set_uin(self, uin):
		self.add_param('uin', uin)

	def get_skey(self):
		return self.get_params().get('skey')

	def set_skey(self, skey):
		self.add_param('skey', skey)

