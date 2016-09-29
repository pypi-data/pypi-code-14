#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyUserCvmOverviewRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'ModifyUserCvmOverview', 'cvm.api.qcloud.com')

	def get_cvmOverviews(self):
		return self.get_params().get('cvmOverviews')

	def set_cvmOverviews(self, cvmOverviews):
		self.add_param('cvmOverviews', cvmOverviews)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

