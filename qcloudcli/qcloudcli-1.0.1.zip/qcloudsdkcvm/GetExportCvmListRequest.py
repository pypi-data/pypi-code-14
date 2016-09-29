#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetExportCvmListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'GetExportCvmList', 'cvm.api.qcloud.com')

	def get_uuidList(self):
		return self.get_params().get('uuidList')

	def set_uuidList(self, uuidList):
		self.add_param('uuidList', uuidList)

	def get_resourceIdList(self):
		return self.get_params().get('resourceIdList')

	def set_resourceIdList(self, resourceIdList):
		self.add_param('resourceIdList', resourceIdList)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

