#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetImageQuotaRequest(Request):

	def __init__(self):
		Request.__init__(self, 'image', 'qcloudcliV1', 'GetImageQuota', 'image.api.qcloud.com')

