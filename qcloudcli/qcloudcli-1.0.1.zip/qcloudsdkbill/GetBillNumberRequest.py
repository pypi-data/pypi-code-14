#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetBillNumberRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bill', 'qcloudcliV1', 'GetBillNumber', 'bill.api.qcloud.com')

	def get_openId(self):
		return self.get_params().get('openId')

	def set_openId(self, openId):
		self.add_param('openId', openId)

	def get_operationType(self):
		return self.get_params().get('operationType')

	def set_operationType(self, operationType):
		self.add_param('operationType', operationType)

	def get_amount(self):
		return self.get_params().get('amount')

	def set_amount(self, amount):
		self.add_param('amount', amount)

