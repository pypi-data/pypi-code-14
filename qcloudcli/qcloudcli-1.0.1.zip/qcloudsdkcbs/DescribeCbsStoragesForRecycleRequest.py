#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeCbsStoragesForRecycleRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cbs', 'qcloudcliV1', 'DescribeCbsStoragesForRecycle', 'cbs.api.qcloud.com')

	def get_storageIds(self):
		return self.get_params().get('storageIds')

	def set_storageIds(self, storageIds):
		self.add_param('storageIds', storageIds)

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

