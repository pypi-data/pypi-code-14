#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyNetworkInterfaceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'ModifyNetworkInterface', 'vpc.api.qcloud.com')

	def get_networkInterfaceId(self):
		return self.get_params().get('networkInterfaceId')

	def set_networkInterfaceId(self, networkInterfaceId):
		self.add_param('networkInterfaceId', networkInterfaceId)

	def get_eniName(self):
		return self.get_params().get('eniName')

	def set_eniName(self, eniName):
		self.add_param('eniName', eniName)

	def get_eniDescription(self):
		return self.get_params().get('eniDescription')

	def set_eniDescription(self, eniDescription):
		self.add_param('eniDescription', eniDescription)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

