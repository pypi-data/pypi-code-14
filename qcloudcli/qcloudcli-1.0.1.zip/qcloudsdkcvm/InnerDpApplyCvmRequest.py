#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerDpApplyCvmRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'InnerDpApplyCvm', 'cvm.api.qcloud.com')

	def get_applyUin(self):
		return self.get_params().get('applyUin')

	def set_applyUin(self, applyUin):
		self.add_param('applyUin', applyUin)

	def get_applyAppid(self):
		return self.get_params().get('applyAppid')

	def set_applyAppid(self, applyAppid):
		self.add_param('applyAppid', applyAppid)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_isVpcGateway(self):
		return self.get_params().get('isVpcGateway')

	def set_isVpcGateway(self, isVpcGateway):
		self.add_param('isVpcGateway', isVpcGateway)

	def get_cpu(self):
		return self.get_params().get('cpu')

	def set_cpu(self, cpu):
		self.add_param('cpu', cpu)

	def get_mem(self):
		return self.get_params().get('mem')

	def set_mem(self, mem):
		self.add_param('mem', mem)

	def get_storage(self):
		return self.get_params().get('storage')

	def set_storage(self, storage):
		self.add_param('storage', storage)

	def get_bandwidth(self):
		return self.get_params().get('bandwidth')

	def set_bandwidth(self, bandwidth):
		self.add_param('bandwidth', bandwidth)

	def get_isWanIp(self):
		return self.get_params().get('isWanIp')

	def set_isWanIp(self, isWanIp):
		self.add_param('isWanIp', isWanIp)

	def get_osName(self):
		return self.get_params().get('osName')

	def set_osName(self, osName):
		self.add_param('osName', osName)

	def get_timeSpan(self):
		return self.get_params().get('timeSpan')

	def set_timeSpan(self, timeSpan):
		self.add_param('timeSpan', timeSpan)

	def get_goodNum(self):
		return self.get_params().get('goodNum')

	def set_goodNum(self, goodNum):
		self.add_param('goodNum', goodNum)

	def get_dealId(self):
		return self.get_params().get('dealId')

	def set_dealId(self, dealId):
		self.add_param('dealId', dealId)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_tempInstanceIds(self):
		return self.get_params().get('tempInstanceIds')

	def set_tempInstanceIds(self, tempInstanceIds):
		self.add_param('tempInstanceIds', tempInstanceIds)

	def get_passWd(self):
		return self.get_params().get('passWd')

	def set_passWd(self, passWd):
		self.add_param('passWd', passWd)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_isWindows(self):
		return self.get_params().get('isWindows')

	def set_isWindows(self, isWindows):
		self.add_param('isWindows', isWindows)

	def get_dealName(self):
		return self.get_params().get('dealName')

	def set_dealName(self, dealName):
		self.add_param('dealName', dealName)

