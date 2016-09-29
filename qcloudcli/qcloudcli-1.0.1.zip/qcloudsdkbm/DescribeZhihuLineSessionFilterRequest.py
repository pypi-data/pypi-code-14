#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeZhihuLineSessionFilterRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeZhihuLineSessionFilter', 'bm.api.qcloud.com')

	def get_bandwidth(self):
		return self.get_params().get('bandwidth')

	def set_bandwidth(self, bandwidth):
		self.add_param('bandwidth', bandwidth)

	def get_datetime(self):
		return self.get_params().get('datetime')

	def set_datetime(self, datetime):
		self.add_param('datetime', datetime)

	def get_direction(self):
		return self.get_params().get('direction')

	def set_direction(self, direction):
		self.add_param('direction', direction)

