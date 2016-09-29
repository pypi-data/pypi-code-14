#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeUserGroupByStrategyRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'DescribeUserGroupByStrategy', 'cam.api.qcloud.com')

	def get_strategyId(self):
		return self.get_params().get('strategyId')

	def set_strategyId(self, strategyId):
		self.add_param('strategyId', strategyId)

	def get_rp(self):
		return self.get_params().get('rp')

	def set_rp(self, rp):
		self.add_param('rp', rp)

	def get_page(self):
		return self.get_params().get('page')

	def set_page(self, page):
		self.add_param('page', page)

	def get_relatedType(self):
		return self.get_params().get('relatedType')

	def set_relatedType(self, relatedType):
		self.add_param('relatedType', relatedType)

