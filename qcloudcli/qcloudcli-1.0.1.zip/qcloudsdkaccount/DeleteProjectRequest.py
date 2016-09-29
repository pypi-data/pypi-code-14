#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteProjectRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'DeleteProject', 'account.api.qcloud.com')

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

