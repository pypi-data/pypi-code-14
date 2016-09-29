#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteDirectConnectGatewayNatRuleRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'DeleteDirectConnectGatewayNatRule', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_directConnectGatewayId(self):
		return self.get_params().get('directConnectGatewayId')

	def set_directConnectGatewayId(self, directConnectGatewayId):
		self.add_param('directConnectGatewayId', directConnectGatewayId)

	def get_natRule(self):
		return self.get_params().get('natRule')

	def set_natRule(self, natRule):
		self.add_param('natRule', natRule)

