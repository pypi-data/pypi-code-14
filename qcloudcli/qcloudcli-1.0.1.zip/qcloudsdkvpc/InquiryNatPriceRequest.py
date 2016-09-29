#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InquiryNatPriceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'InquiryNatPrice', 'vpc.api.qcloud.com')

	def get_maxConcurrent(self):
		return self.get_params().get('maxConcurrent')

	def set_maxConcurrent(self, maxConcurrent):
		self.add_param('maxConcurrent', maxConcurrent)

