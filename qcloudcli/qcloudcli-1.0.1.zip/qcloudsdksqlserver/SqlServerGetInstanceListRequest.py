#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SqlServerGetInstanceListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'sqlserver', 'qcloudcliV1', 'SqlServerGetInstanceList', 'sqlserver.api.qcloud.com')

	def get_instanceIds(self):
		return self.get_params().get('instanceIds')

	def set_instanceIds(self, instanceIds):
		self.add_param('instanceIds', instanceIds)

	def get_resourceIds(self):
		return self.get_params().get('resourceIds')

	def set_resourceIds(self, resourceIds):
		self.add_param('resourceIds', resourceIds)

	def get_regionId(self):
		return self.get_params().get('regionId')

	def set_regionId(self, regionId):
		self.add_param('regionId', regionId)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_status(self):
		return self.get_params().get('status')

	def set_status(self, status):
		self.add_param('status', status)

	def get_pageSize(self):
		return self.get_params().get('pageSize')

	def set_pageSize(self, pageSize):
		self.add_param('pageSize', pageSize)

	def get_pageNo(self):
		return self.get_params().get('pageNo')

	def set_pageNo(self, pageNo):
		self.add_param('pageNo', pageNo)

	def get_orderBy(self):
		return self.get_params().get('orderBy')

	def set_orderBy(self, orderBy):
		self.add_param('orderBy', orderBy)

	def get_orderByType(self):
		return self.get_params().get('orderByType')

	def set_orderByType(self, orderByType):
		self.add_param('orderByType', orderByType)

