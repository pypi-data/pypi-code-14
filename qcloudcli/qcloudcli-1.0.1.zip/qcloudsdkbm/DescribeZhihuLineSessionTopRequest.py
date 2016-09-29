#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeZhihuLineSessionTopRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeZhihuLineSessionTop', 'bm.api.qcloud.com')

	def get_top(self):
		return self.get_params().get('top')

	def set_top(self, top):
		self.add_param('top', top)

	def get_datetime(self):
		return self.get_params().get('datetime')

	def set_datetime(self, datetime):
		self.add_param('datetime', datetime)

	def get_direction(self):
		return self.get_params().get('direction')

	def set_direction(self, direction):
		self.add_param('direction', direction)

