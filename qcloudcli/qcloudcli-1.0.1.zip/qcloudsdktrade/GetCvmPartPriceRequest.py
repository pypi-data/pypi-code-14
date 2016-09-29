#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCvmPartPriceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'trade', 'qcloudcliV1', 'GetCvmPartPrice', 'trade.api.qcloud.com')

	def get_goods(self):
		return self.get_params().get('goods')

	def set_goods(self, goods):
		self.add_param('goods', goods)

