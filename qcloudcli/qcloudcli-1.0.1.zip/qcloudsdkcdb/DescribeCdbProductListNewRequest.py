#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeCdbProductListNewRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdb', 'qcloudcliV1', 'DescribeCdbProductListNew', 'cdb.api.qcloud.com')

