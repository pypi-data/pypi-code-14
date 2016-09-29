#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetSDKAppIdInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'imyun', 'qcloudcliV1', 'GetSDKAppIdInfo', 'imyun.api.qcloud.com')

