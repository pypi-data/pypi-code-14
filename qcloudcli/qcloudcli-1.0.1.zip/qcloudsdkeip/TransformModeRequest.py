#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class TransformModeRequest(Request):

	def __init__(self):
		Request.__init__(self, 'eip', 'qcloudcliV1', 'TransformMode', 'eip.api.qcloud.com')

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

