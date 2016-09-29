#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UnBindLbRuleRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'UnBindLbRule', 'bm.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_vip(self):
		return self.get_params().get('vip')

	def set_vip(self, vip):
		self.add_param('vip', vip)

	def get_vport(self):
		return self.get_params().get('vport')

	def set_vport(self, vport):
		self.add_param('vport', vport)

	def get_rsIp(self):
		return self.get_params().get('rsIp')

	def set_rsIp(self, rsIp):
		self.add_param('rsIp', rsIp)

	def get_rsPort(self):
		return self.get_params().get('rsPort')

	def set_rsPort(self, rsPort):
		self.add_param('rsPort', rsPort)

