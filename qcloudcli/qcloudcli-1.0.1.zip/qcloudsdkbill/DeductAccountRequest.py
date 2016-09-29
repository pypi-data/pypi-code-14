#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeductAccountRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bill', 'qcloudcliV1', 'DeductAccount', 'bill.api.qcloud.com')

	def get_openId(self):
		return self.get_params().get('openId')

	def set_openId(self, openId):
		self.add_param('openId', openId)

	def get_billNumber(self):
		return self.get_params().get('billNumber')

	def set_billNumber(self, billNumber):
		self.add_param('billNumber', billNumber)

	def get_amt(self):
		return self.get_params().get('amt')

	def set_amt(self, amt):
		self.add_param('amt', amt)

	def get_callTimestamp(self):
		return self.get_params().get('callTimestamp')

	def set_callTimestamp(self, callTimestamp):
		self.add_param('callTimestamp', callTimestamp)

	def get_desc(self):
		return self.get_params().get('desc')

	def set_desc(self, desc):
		self.add_param('desc', desc)

