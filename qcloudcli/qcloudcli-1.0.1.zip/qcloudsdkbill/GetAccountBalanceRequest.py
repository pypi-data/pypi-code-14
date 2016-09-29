#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetAccountBalanceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bill', 'qcloudcliV1', 'GetAccountBalance', 'bill.api.qcloud.com')

	def get_openId(self):
		return self.get_params().get('openId')

	def set_openId(self, openId):
		self.add_param('openId', openId)

