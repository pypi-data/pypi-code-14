#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCorpUserInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'GetCorpUserInfo', 'account.api.qcloud.com')

