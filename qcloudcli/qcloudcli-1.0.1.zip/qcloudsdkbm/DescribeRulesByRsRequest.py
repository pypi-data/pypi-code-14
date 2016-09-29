#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRulesByRsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeRulesByRs', 'bm.api.qcloud.com')

	def get_rsIps(self):
		return self.get_params().get('rsIps')

	def set_rsIps(self, rsIps):
		self.add_param('rsIps', rsIps)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_pageNum(self):
		return self.get_params().get('pageNum')

	def set_pageNum(self, pageNum):
		self.add_param('pageNum', pageNum)

	def get_pageSize(self):
		return self.get_params().get('pageSize')

	def set_pageSize(self, pageSize):
		self.add_param('pageSize', pageSize)

