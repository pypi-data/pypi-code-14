#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeLBHealthStatusMcRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'DescribeLBHealthStatusMc', 'lb.api.qcloud.com')

	def get_loadBalanceIds(self):
		return self.get_params().get('loadBalanceIds')

	def set_loadBalanceIds(self, loadBalanceIds):
		self.add_param('loadBalanceIds', loadBalanceIds)

