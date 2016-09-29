#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UseVoucherDataRequest(Request):

	def __init__(self):
		Request.__init__(self, 'market', 'qcloudcliV1', 'UseVoucherData', 'market.api.qcloud.com')

	def get_voucherCode(self):
		return self.get_params().get('voucherCode')

	def set_voucherCode(self, voucherCode):
		self.add_param('voucherCode', voucherCode)

