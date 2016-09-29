#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CheckStrategyNameRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'CheckStrategyName', 'cam.api.qcloud.com')

	def get_strategyName(self):
		return self.get_params().get('strategyName')

	def set_strategyName(self, strategyName):
		self.add_param('strategyName', strategyName)

