#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetAppCvmQuotaOverviewRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'GetAppCvmQuotaOverview', 'cvm.api.qcloud.com')

