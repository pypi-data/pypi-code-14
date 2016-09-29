#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribleTaskResultRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribleTaskResult', 'cvm.api.qcloud.com')

	def get_applyUin(self):
		return self.get_params().get('applyUin')

	def set_applyUin(self, applyUin):
		self.add_param('applyUin', applyUin)

	def get_applyAppid(self):
		return self.get_params().get('applyAppid')

	def set_applyAppid(self, applyAppid):
		self.add_param('applyAppid', applyAppid)

	def get_taskId(self):
		return self.get_params().get('taskId')

	def set_taskId(self, taskId):
		self.add_param('taskId', taskId)

