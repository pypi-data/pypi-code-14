#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SendMsgRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'SendMsg', 'account.api.qcloud.com')

