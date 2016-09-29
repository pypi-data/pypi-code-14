#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeVpcLimitRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'DescribeVpcLimit', 'vpc.api.qcloud.com')

	def get_type(self):
		return self.get_params().get('type')

	def set_type(self, type):
		self.add_param('type', type)

