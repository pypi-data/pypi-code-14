#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeStrategyDetailRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'DescribeStrategyDetail', 'cam.api.qcloud.com')

	def get_strategyId(self):
		return self.get_params().get('strategyId')

	def set_strategyId(self, strategyId):
		self.add_param('strategyId', strategyId)

	def get_ownerUin(self):
		return self.get_params().get('ownerUin')

	def set_ownerUin(self, ownerUin):
		self.add_param('ownerUin', ownerUin)

