#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeInstanceMainInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribeInstanceMainInfo', 'cvm.api.qcloud.com')

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_ips(self):
		return self.get_params().get('ips')

	def set_ips(self, ips):
		self.add_param('ips', ips)

	def get_instanceName(self):
		return self.get_params().get('instanceName')

	def set_instanceName(self, instanceName):
		self.add_param('instanceName', instanceName)

	def get_searchWord(self):
		return self.get_params().get('searchWord')

	def set_searchWord(self, searchWord):
		self.add_param('searchWord', searchWord)

	def get_uInstanceIds(self):
		return self.get_params().get('uInstanceIds')

	def set_uInstanceIds(self, uInstanceIds):
		self.add_param('uInstanceIds', uInstanceIds)

	def get_cvmPayMode(self):
		return self.get_params().get('cvmPayMode')

	def set_cvmPayMode(self, cvmPayMode):
		self.add_param('cvmPayMode', cvmPayMode)

	def get_deviceClass(self):
		return self.get_params().get('deviceClass')

	def set_deviceClass(self, deviceClass):
		self.add_param('deviceClass', deviceClass)

	def get_uHostIds(self):
		return self.get_params().get('uHostIds')

	def set_uHostIds(self, uHostIds):
		self.add_param('uHostIds', uHostIds)

	def get_zoneIdList(self):
		return self.get_params().get('zoneIdList')

	def set_zoneIdList(self, zoneIdList):
		self.add_param('zoneIdList', zoneIdList)

	def get_cvmPayModeList(self):
		return self.get_params().get('cvmPayModeList')

	def set_cvmPayModeList(self, cvmPayModeList):
		self.add_param('cvmPayModeList', cvmPayModeList)

	def get_deviceClassList(self):
		return self.get_params().get('deviceClassList')

	def set_deviceClassList(self, deviceClassList):
		self.add_param('deviceClassList', deviceClassList)

	def get_subnetIds(self):
		return self.get_params().get('subnetIds')

	def set_subnetIds(self, subnetIds):
		self.add_param('subnetIds', subnetIds)

	def get_uuids(self):
		return self.get_params().get('uuids')

	def set_uuids(self, uuids):
		self.add_param('uuids', uuids)

