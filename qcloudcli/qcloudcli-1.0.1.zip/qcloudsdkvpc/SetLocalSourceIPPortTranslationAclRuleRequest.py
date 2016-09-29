#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SetLocalSourceIPPortTranslationAclRuleRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'SetLocalSourceIPPortTranslationAclRule', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_directConnectGatewayId(self):
		return self.get_params().get('directConnectGatewayId')

	def set_directConnectGatewayId(self, directConnectGatewayId):
		self.add_param('directConnectGatewayId', directConnectGatewayId)

	def get_translationIPPool(self):
		return self.get_params().get('translationIPPool')

	def set_translationIPPool(self, translationIPPool):
		self.add_param('translationIPPool', translationIPPool)

	def get_setData(self):
		return self.get_params().get('setData')

	def set_setData(self, setData):
		self.add_param('setData', setData)

