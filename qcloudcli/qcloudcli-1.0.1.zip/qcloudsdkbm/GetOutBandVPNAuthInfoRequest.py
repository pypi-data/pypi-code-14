#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetOutBandVPNAuthInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'GetOutBandVPNAuthInfo', 'bm.api.qcloud.com')

	def get_appId(self):
		return self.get_params().get('appId')

	def set_appId(self, appId):
		self.add_param('appId', appId)

