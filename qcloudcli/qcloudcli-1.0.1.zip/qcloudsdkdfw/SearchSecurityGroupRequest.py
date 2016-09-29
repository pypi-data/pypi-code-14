#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SearchSecurityGroupRequest(Request):

	def __init__(self):
		Request.__init__(self, 'dfw', 'qcloudcliV1', 'SearchSecurityGroup', 'dfw.api.qcloud.com')

	def get_searchIndex(self):
		return self.get_params().get('searchIndex')

	def set_searchIndex(self, searchIndex):
		self.add_param('searchIndex', searchIndex)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

