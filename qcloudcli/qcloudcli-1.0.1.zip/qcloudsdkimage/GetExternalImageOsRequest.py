#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetExternalImageOsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'image', 'qcloudcliV1', 'GetExternalImageOs', 'image.api.qcloud.com')

