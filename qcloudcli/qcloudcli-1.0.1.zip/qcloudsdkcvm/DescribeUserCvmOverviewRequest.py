#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeUserCvmOverviewRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribeUserCvmOverview', 'cvm.api.qcloud.com')

	def get_regionIds(self):
		return self.get_params().get('regionIds')

	def set_regionIds(self, regionIds):
		self.add_param('regionIds', regionIds)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

