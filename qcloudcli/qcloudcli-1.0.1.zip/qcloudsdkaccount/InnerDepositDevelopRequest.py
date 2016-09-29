#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerDepositDevelopRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InnerDepositDevelop', 'account.api.qcloud.com')

	def get_targetUin(self):
		return self.get_params().get('targetUin')

	def set_targetUin(self, targetUin):
		self.add_param('targetUin', targetUin)

	def get_amount(self):
		return self.get_params().get('amount')

	def set_amount(self, amount):
		self.add_param('amount', amount)

	def get_applyUser(self):
		return self.get_params().get('applyUser')

	def set_applyUser(self, applyUser):
		self.add_param('applyUser', applyUser)

	def get_gameID(self):
		return self.get_params().get('gameID')

	def set_gameID(self, gameID):
		self.add_param('gameID', gameID)

	def get_gameName(self):
		return self.get_params().get('gameName')

	def set_gameName(self, gameName):
		self.add_param('gameName', gameName)

	def get_department(self):
		return self.get_params().get('department')

	def set_department(self, department):
		self.add_param('department', department)

