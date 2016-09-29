#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRedisProductListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'redis', 'SDK_PYTHON_1.1', 'DescribeRedisProductList', 'redis.api.qcloud.com')

