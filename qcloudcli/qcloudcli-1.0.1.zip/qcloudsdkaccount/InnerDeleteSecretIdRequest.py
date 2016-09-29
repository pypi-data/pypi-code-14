#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerDeleteSecretIdRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InnerDeleteSecretId', 'account.api.qcloud.com')

	def get_deleteSecretId(self):
		return self.get_params().get('deleteSecretId')

	def set_deleteSecretId(self, deleteSecretId):
		self.add_param('deleteSecretId', deleteSecretId)

	def get_targetUin(self):
		return self.get_params().get('targetUin')

	def set_targetUin(self, targetUin):
		self.add_param('targetUin', targetUin)

