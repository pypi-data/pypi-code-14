#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UpdateCertAliasRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'UpdateCertAlias', 'account.api.qcloud.com')

	def get_id(self):
		return self.get_params().get('id')

	def set_id(self, id):
		self.add_param('id', id)

	def get_alias(self):
		return self.get_params().get('alias')

	def set_alias(self, alias):
		self.add_param('alias', alias)

