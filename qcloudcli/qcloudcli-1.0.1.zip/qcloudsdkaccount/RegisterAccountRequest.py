#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class RegisterAccountRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'RegisterAccount', 'account.api.qcloud.com')

	def get_accountUin(self):
		return self.get_params().get('accountUin')

	def set_accountUin(self, accountUin):
		self.add_param('accountUin', accountUin)

	def get_accountName(self):
		return self.get_params().get('accountName')

	def set_accountName(self, accountName):
		self.add_param('accountName', accountName)

	def get_accountMail(self):
		return self.get_params().get('accountMail')

	def set_accountMail(self, accountMail):
		self.add_param('accountMail', accountMail)

	def get_accountPhone(self):
		return self.get_params().get('accountPhone')

	def set_accountPhone(self, accountPhone):
		self.add_param('accountPhone', accountPhone)

	def get_accountType(self):
		return self.get_params().get('accountType')

	def set_accountType(self, accountType):
		self.add_param('accountType', accountType)

	def get_accountDept(self):
		return self.get_params().get('accountDept')

	def set_accountDept(self, accountDept):
		self.add_param('accountDept', accountDept)

	def get_accountSource(self):
		return self.get_params().get('accountSource')

	def set_accountSource(self, accountSource):
		self.add_param('accountSource', accountSource)

	def get_accountRemark(self):
		return self.get_params().get('accountRemark')

	def set_accountRemark(self, accountRemark):
		self.add_param('accountRemark', accountRemark)

