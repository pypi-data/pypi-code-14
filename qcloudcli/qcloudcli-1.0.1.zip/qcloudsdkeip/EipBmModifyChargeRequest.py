#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class EipBmModifyChargeRequest(Request):

	def __init__(self):
		Request.__init__(self, 'eip', 'qcloudcliV1', 'EipBmModifyCharge', 'eip.api.qcloud.com')

	def get_eipIds(self):
		return self.get_params().get('eipIds')

	def set_eipIds(self, eipIds):
		self.add_param('eipIds', eipIds)

	def get_eips(self):
		return self.get_params().get('eips')

	def set_eips(self, eips):
		self.add_param('eips', eips)

	def get_mode(self):
		return self.get_params().get('mode')

	def set_mode(self, mode):
		self.add_param('mode', mode)

	def get_bandwidth(self):
		return self.get_params().get('bandwidth')

	def set_bandwidth(self, bandwidth):
		self.add_param('bandwidth', bandwidth)

