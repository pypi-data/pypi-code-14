#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerGetUserAppidRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InnerGetUserAppid', 'account.api.qcloud.com')

	def get_getUin(self):
		return self.get_params().get('getUin')

	def set_getUin(self, getUin):
		self.add_param('getUin', getUin)

