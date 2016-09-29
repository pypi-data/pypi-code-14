#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetOsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'image', 'qcloudcliV1', 'GetOs', 'image.api.qcloud.com')

	def get_whiteSwitch(self):
		return self.get_params().get('whiteSwitch')

	def set_whiteSwitch(self, whiteSwitch):
		self.add_param('whiteSwitch', whiteSwitch)

