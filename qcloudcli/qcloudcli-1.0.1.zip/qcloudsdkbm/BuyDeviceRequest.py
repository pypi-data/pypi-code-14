#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class BuyDeviceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'BuyDevice', 'bm.api.qcloud.com')

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_deviceClassCode(self):
		return self.get_params().get('deviceClassCode')

	def set_deviceClassCode(self, deviceClassCode):
		self.add_param('deviceClassCode', deviceClassCode)

	def get_osTypeId(self):
		return self.get_params().get('osTypeId')

	def set_osTypeId(self, osTypeId):
		self.add_param('osTypeId', osTypeId)

	def get_raidId(self):
		return self.get_params().get('raidId')

	def set_raidId(self, raidId):
		self.add_param('raidId', raidId)

	def get_timeUnit(self):
		return self.get_params().get('timeUnit')

	def set_timeUnit(self, timeUnit):
		self.add_param('timeUnit', timeUnit)

	def get_timeSpan(self):
		return self.get_params().get('timeSpan')

	def set_timeSpan(self, timeSpan):
		self.add_param('timeSpan', timeSpan)

	def get_goodsNum(self):
		return self.get_params().get('goodsNum')

	def set_goodsNum(self, goodsNum):
		self.add_param('goodsNum', goodsNum)

	def get_needSecurityAgent(self):
		return self.get_params().get('needSecurityAgent')

	def set_needSecurityAgent(self, needSecurityAgent):
		self.add_param('needSecurityAgent', needSecurityAgent)

	def get_needMonitorAgent(self):
		return self.get_params().get('needMonitorAgent')

	def set_needMonitorAgent(self, needMonitorAgent):
		self.add_param('needMonitorAgent', needMonitorAgent)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_hasWanIp(self):
		return self.get_params().get('hasWanIp')

	def set_hasWanIp(self, hasWanIp):
		self.add_param('hasWanIp', hasWanIp)

	def get_alias(self):
		return self.get_params().get('alias')

	def set_alias(self, alias):
		self.add_param('alias', alias)

	def get_aliases(self):
		return self.get_params().get('aliases')

	def set_aliases(self, aliases):
		self.add_param('aliases', aliases)

