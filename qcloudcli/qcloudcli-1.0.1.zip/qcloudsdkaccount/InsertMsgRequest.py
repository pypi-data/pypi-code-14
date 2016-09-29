#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InsertMsgRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InsertMsg', 'account.api.qcloud.com')

