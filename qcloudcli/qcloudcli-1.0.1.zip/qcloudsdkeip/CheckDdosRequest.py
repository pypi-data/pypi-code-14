#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CheckDdosRequest(Request):

	def __init__(self):
		Request.__init__(self, 'eip', 'qcloudcliV1', 'CheckDdos', 'eip.api.qcloud.com')

	def get_viplist(self):
		return self.get_params().get('viplist')

	def set_viplist(self, viplist):
		self.add_param('viplist', viplist)

