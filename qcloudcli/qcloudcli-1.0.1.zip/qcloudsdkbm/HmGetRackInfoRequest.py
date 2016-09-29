#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class HmGetRackInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'HmGetRackInfo', 'bm.api.qcloud.com')

	def get_macAddrs(self):
		return self.get_params().get('macAddrs')

	def set_macAddrs(self, macAddrs):
		self.add_param('macAddrs', macAddrs)

