#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeInstancesTestRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribeInstancesTest', 'cvm.api.qcloud.com')

	def get_cpu(self):
		return self.get_params().get('cpu')

	def set_cpu(self, cpu):
		self.add_param('cpu', cpu)

	def get_instanceIds(self):
		return self.get_params().get('instanceIds')

	def set_instanceIds(self, instanceIds):
		self.add_param('instanceIds', instanceIds)

