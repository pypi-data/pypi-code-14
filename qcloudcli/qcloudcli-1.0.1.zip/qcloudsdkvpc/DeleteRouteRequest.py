#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteRouteRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'DeleteRoute', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_routeTableId(self):
		return self.get_params().get('routeTableId')

	def set_routeTableId(self, routeTableId):
		self.add_param('routeTableId', routeTableId)

	def get_routeSet(self):
		return self.get_params().get('routeSet')

	def set_routeSet(self, routeSet):
		self.add_param('routeSet', routeSet)

