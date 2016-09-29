#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribleCvmByTempIdRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'DescribleCvmByTempId', 'cvm.api.qcloud.com')

	def get_applyUin(self):
		return self.get_params().get('applyUin')

	def set_applyUin(self, applyUin):
		self.add_param('applyUin', applyUin)

	def get_applyAppid(self):
		return self.get_params().get('applyAppid')

	def set_applyAppid(self, applyAppid):
		self.add_param('applyAppid', applyAppid)

	def get_tempInstanceIds(self):
		return self.get_params().get('tempInstanceIds')

	def set_tempInstanceIds(self, tempInstanceIds):
		self.add_param('tempInstanceIds', tempInstanceIds)

