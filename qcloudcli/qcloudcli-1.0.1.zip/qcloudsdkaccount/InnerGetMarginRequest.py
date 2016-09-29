#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InnerGetMarginRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InnerGetMargin', 'account.api.qcloud.com')

	def get_targetUin(self):
		return self.get_params().get('targetUin')

	def set_targetUin(self, targetUin):
		self.add_param('targetUin', targetUin)

