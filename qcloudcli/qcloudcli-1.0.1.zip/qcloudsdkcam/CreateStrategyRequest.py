#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateStrategyRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'CreateStrategy', 'cam.api.qcloud.com')

	def get_loginUin(self):
		return self.get_params().get('loginUin')

	def set_loginUin(self, loginUin):
		self.add_param('loginUin', loginUin)

	def get_strategyName(self):
		return self.get_params().get('strategyName')

	def set_strategyName(self, strategyName):
		self.add_param('strategyName', strategyName)

	def get_strategyInfo(self):
		return self.get_params().get('strategyInfo')

	def set_strategyInfo(self, strategyInfo):
		self.add_param('strategyInfo', strategyInfo)

	def get_isPreset(self):
		return self.get_params().get('isPreset')

	def set_isPreset(self, isPreset):
		self.add_param('isPreset', isPreset)

	def get_remark(self):
		return self.get_params().get('remark')

	def set_remark(self, remark):
		self.add_param('remark', remark)

