#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class QueryLbJobStatusRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'QueryLbJobStatus', 'bm.api.qcloud.com')

	def get_jobId(self):
		return self.get_params().get('jobId')

	def set_jobId(self, jobId):
		self.add_param('jobId', jobId)

