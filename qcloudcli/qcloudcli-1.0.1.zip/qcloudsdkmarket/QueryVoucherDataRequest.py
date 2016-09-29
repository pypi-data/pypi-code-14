#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class QueryVoucherDataRequest(Request):

	def __init__(self):
		Request.__init__(self, 'market', 'qcloudcliV1', 'QueryVoucherData', 'market.api.qcloud.com')

	def get_voucherCode(self):
		return self.get_params().get('voucherCode')

	def set_voucherCode(self, voucherCode):
		self.add_param('voucherCode', voucherCode)

