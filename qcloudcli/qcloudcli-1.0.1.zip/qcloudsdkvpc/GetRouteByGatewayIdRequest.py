#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetRouteByGatewayIdRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'GetRouteByGatewayId', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_gatewayId(self):
		return self.get_params().get('gatewayId')

	def set_gatewayId(self, gatewayId):
		self.add_param('gatewayId', gatewayId)

