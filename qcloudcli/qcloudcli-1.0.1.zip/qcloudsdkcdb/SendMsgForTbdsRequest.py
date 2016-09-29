#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SendMsgForTbdsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdb', 'qcloudcliV1', 'SendMsgForTbds', 'cdb.api.qcloud.com')

	def get_smsContent(self):
		return self.get_params().get('smsContent')

	def set_smsContent(self, smsContent):
		self.add_param('smsContent', smsContent)

