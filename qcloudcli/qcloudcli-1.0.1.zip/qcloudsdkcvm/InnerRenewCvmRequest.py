#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerRenewCvmRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'InnerRenewCvm', 'cvm.api.qcloud.com')

	def get_applyUin(self):
		return self.get_params().get('applyUin')

	def set_applyUin(self, applyUin):
		self.add_param('applyUin', applyUin)

	def get_applyAppid(self):
		return self.get_params().get('applyAppid')

	def set_applyAppid(self, applyAppid):
		self.add_param('applyAppid', applyAppid)

	def get_curDeadline(self):
		return self.get_params().get('curDeadline')

	def set_curDeadline(self, curDeadline):
		self.add_param('curDeadline', curDeadline)

	def get_timeSpan(self):
		return self.get_params().get('timeSpan')

	def set_timeSpan(self, timeSpan):
		self.add_param('timeSpan', timeSpan)

	def get_curBandwidth(self):
		return self.get_params().get('curBandwidth')

	def set_curBandwidth(self, curBandwidth):
		self.add_param('curBandwidth', curBandwidth)

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

	def get_dealId(self):
		return self.get_params().get('dealId')

	def set_dealId(self, dealId):
		self.add_param('dealId', dealId)

	def get_dealName(self):
		return self.get_params().get('dealName')

	def set_dealName(self, dealName):
		self.add_param('dealName', dealName)

