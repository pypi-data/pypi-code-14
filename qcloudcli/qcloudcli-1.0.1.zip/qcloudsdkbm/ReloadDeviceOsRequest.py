#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ReloadDeviceOsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'ReloadDeviceOs', 'bm.api.qcloud.com')

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

	def get_passwd(self):
		return self.get_params().get('passwd')

	def set_passwd(self, passwd):
		self.add_param('passwd', passwd)

	def get_osTypeId(self):
		return self.get_params().get('osTypeId')

	def set_osTypeId(self, osTypeId):
		self.add_param('osTypeId', osTypeId)

	def get_raidId(self):
		return self.get_params().get('raidId')

	def set_raidId(self, raidId):
		self.add_param('raidId', raidId)

	def get_agentIds(self):
		return self.get_params().get('agentIds')

	def set_agentIds(self, agentIds):
		self.add_param('agentIds', agentIds)

	def get_isZoning(self):
		return self.get_params().get('isZoning')

	def set_isZoning(self, isZoning):
		self.add_param('isZoning', isZoning)

