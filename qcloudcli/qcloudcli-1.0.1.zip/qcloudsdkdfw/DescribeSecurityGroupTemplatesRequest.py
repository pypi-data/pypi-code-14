#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeSecurityGroupTemplatesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'dfw', 'qcloudcliV1', 'DescribeSecurityGroupTemplates', 'dfw.api.qcloud.com')

