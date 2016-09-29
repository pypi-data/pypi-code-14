#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeAccountBalanceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'trade', 'SDK_PYTHON_1.1', 'DescribeAccountBalance', 'trade.api.qcloud.com')


