#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRedisZoneListRequest(Request):

	def __init__(self):
		Request.__init__(self, 'redis', 'SDK_PYTHON_1.1', 'DescribeRedisZoneList', 'redis.api.qcloud.com')

