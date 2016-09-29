#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeStrategyListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'DescribeStrategyList', 'cam.api.qcloud.com')

	def get_type(self):
		return self.get_params().get('type')

	def set_type(self, type):
		self.add_param('type', type)

	def get_rp(self):
		return self.get_params().get('rp')

	def set_rp(self, rp):
		self.add_param('rp', rp)

	def get_page(self):
		return self.get_params().get('page')

	def set_page(self, page):
		self.add_param('page', page)

	def get_keyword(self):
		return self.get_params().get('keyword')

	def set_keyword(self, keyword):
		self.add_param('keyword', keyword)

	def get_filterInfo(self):
		return self.get_params().get('filterInfo')

	def set_filterInfo(self, filterInfo):
		self.add_param('filterInfo', filterInfo)

