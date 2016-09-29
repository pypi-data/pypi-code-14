#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeInstanceCbsInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribeInstanceCbsInfo', 'cvm.api.qcloud.com')

	def get_uInstanceIds(self):
		return self.get_params().get('uInstanceIds')

	def set_uInstanceIds(self, uInstanceIds):
		self.add_param('uInstanceIds', uInstanceIds)

