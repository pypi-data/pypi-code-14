#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeProjectTestRequest(Request):

	def __init__(self):
		Request.__init__(self, 'account', 'qcloudcliV1', 'DescribeProjectTest', 'account.api.qcloud.com')

