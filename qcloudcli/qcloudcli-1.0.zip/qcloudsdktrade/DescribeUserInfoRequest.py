#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeUserInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'trade', 'SDK_PYTHON_1.1', 'DescribeUserInfo', 'trade.api.qcloud.com')


