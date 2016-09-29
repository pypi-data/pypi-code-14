#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class InsertMsgViaUinRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'InsertMsgViaUin', 'account.api.qcloud.com')

