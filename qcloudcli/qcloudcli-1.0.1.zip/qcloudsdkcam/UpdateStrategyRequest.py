#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UpdateStrategyRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'UpdateStrategy', 'cam.api.qcloud.com')

	def get_updateType(self):
		return self.get_params().get('updateType')

	def set_updateType(self, updateType):
		self.add_param('updateType', updateType)

	def get_updateInfo(self):
		return self.get_params().get('updateInfo')

	def set_updateInfo(self, updateInfo):
		self.add_param('updateInfo', updateInfo)

	def get_strategyId(self):
		return self.get_params().get('strategyId')

	def set_strategyId(self, strategyId):
		self.add_param('strategyId', strategyId)

