#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class OperateStrategyRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'OperateStrategy', 'cam.api.qcloud.com')

	def get_groupId(self):
		return self.get_params().get('groupId')

	def set_groupId(self, groupId):
		self.add_param('groupId', groupId)

	def get_relateUin(self):
		return self.get_params().get('relateUin')

	def set_relateUin(self, relateUin):
		self.add_param('relateUin', relateUin)

	def get_strategyId(self):
		return self.get_params().get('strategyId')

	def set_strategyId(self, strategyId):
		self.add_param('strategyId', strategyId)

	def get_actionType(self):
		return self.get_params().get('actionType')

	def set_actionType(self, actionType):
		self.add_param('actionType', actionType)

