#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UnblockAccountBalanceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bill', 'qcloudcliV1', 'UnblockAccountBalance', 'bill.api.qcloud.com')

	def get_openId(self):
		return self.get_params().get('openId')

	def set_openId(self, openId):
		self.add_param('openId', openId)

	def get_billNumber(self):
		return self.get_params().get('billNumber')

	def set_billNumber(self, billNumber):
		self.add_param('billNumber', billNumber)

	def get_tranInfo(self):
		return self.get_params().get('tranInfo')

	def set_tranInfo(self, tranInfo):
		self.add_param('tranInfo', tranInfo)

