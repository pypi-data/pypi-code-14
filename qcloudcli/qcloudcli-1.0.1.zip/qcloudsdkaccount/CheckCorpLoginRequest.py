#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CheckCorpLoginRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'CheckCorpLogin', 'account.api.qcloud.com')

