#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRulesByVipRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeRulesByVip', 'bm.api.qcloud.com')

	def get_vips(self):
		return self.get_params().get('vips')

	def set_vips(self, vips):
		self.add_param('vips', vips)

	def get_vports(self):
		return self.get_params().get('vports')

	def set_vports(self, vports):
		self.add_param('vports', vports)

	def get_pageNum(self):
		return self.get_params().get('pageNum')

	def set_pageNum(self, pageNum):
		self.add_param('pageNum', pageNum)

	def get_pageSize(self):
		return self.get_params().get('pageSize')

	def set_pageSize(self, pageSize):
		self.add_param('pageSize', pageSize)

