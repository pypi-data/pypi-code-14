#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerUpgradeBandwidthRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'InnerUpgradeBandwidth', 'cvm.api.qcloud.com')

	def get_applyUin(self):
		return self.get_params().get('applyUin')

	def set_applyUin(self, applyUin):
		self.add_param('applyUin', applyUin)

	def get_applyAppid(self):
		return self.get_params().get('applyAppid')

	def set_applyAppid(self, applyAppid):
		self.add_param('applyAppid', applyAppid)

	def get_curBandwidth(self):
		return self.get_params().get('curBandwidth')

	def set_curBandwidth(self, curBandwidth):
		self.add_param('curBandwidth', curBandwidth)

	def get_newBandwidth(self):
		return self.get_params().get('newBandwidth')

	def set_newBandwidth(self, newBandwidth):
		self.add_param('newBandwidth', newBandwidth)

	def get_startTime(self):
		return self.get_params().get('startTime')

	def set_startTime(self, startTime):
		self.add_param('startTime', startTime)

	def get_endTime(self):
		return self.get_params().get('endTime')

	def set_endTime(self, endTime):
		self.add_param('endTime', endTime)

	def get_dealId(self):
		return self.get_params().get('dealId')

	def set_dealId(self, dealId):
		self.add_param('dealId', dealId)

	def get_dealName(self):
		return self.get_params().get('dealName')

	def set_dealName(self, dealName):
		self.add_param('dealName', dealName)

