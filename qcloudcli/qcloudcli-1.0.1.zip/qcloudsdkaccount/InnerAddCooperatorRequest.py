#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerAddCooperatorRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InnerAddCooperator', 'account.api.qcloud.com')

	def get_collUin(self):
		return self.get_params().get('collUin')

	def set_collUin(self, collUin):
		self.add_param('collUin', collUin)

	def get_collName(self):
		return self.get_params().get('collName')

	def set_collName(self, collName):
		self.add_param('collName', collName)

	def get_collTel(self):
		return self.get_params().get('collTel')

	def set_collTel(self, collTel):
		self.add_param('collTel', collTel)

	def get_collMail(self):
		return self.get_params().get('collMail')

	def set_collMail(self, collMail):
		self.add_param('collMail', collMail)

	def get_collPermList(self):
		return self.get_params().get('collPermList')

	def set_collPermList(self, collPermList):
		self.add_param('collPermList', collPermList)

	def get_type(self):
		return self.get_params().get('type')

	def set_type(self, type):
		self.add_param('type', type)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

