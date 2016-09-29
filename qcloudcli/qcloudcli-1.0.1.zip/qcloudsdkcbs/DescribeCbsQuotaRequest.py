#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeCbsQuotaRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cbs', 'qcloudcliV1', 'DescribeCbsQuota', 'cbs.api.qcloud.com')

