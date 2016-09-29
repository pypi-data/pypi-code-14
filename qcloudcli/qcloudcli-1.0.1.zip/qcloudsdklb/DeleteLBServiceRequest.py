#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteLBServiceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'DeleteLBService', 'lb.api.qcloud.com')

	def get_loadBalanceId(self):
		return self.get_params().get('loadBalanceId')

	def set_loadBalanceId(self, loadBalanceId):
		self.add_param('loadBalanceId', loadBalanceId)

	def get_device(self):
		return self.get_params().get('device')

	def set_device(self, device):
		self.add_param('device', device)

