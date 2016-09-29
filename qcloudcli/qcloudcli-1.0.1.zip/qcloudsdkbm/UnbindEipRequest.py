#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UnbindEipRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'UnbindEip', 'bm.api.qcloud.com')

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

	def get_eip(self):
		return self.get_params().get('eip')

	def set_eip(self, eip):
		self.add_param('eip', eip)

	def get_opUin(self):
		return self.get_params().get('opUin')

	def set_opUin(self, opUin):
		self.add_param('opUin', opUin)

