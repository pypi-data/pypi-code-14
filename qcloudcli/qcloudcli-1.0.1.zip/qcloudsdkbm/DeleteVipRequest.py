#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteVipRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DeleteVip', 'bm.api.qcloud.com')

	def get_vip(self):
		return self.get_params().get('vip')

	def set_vip(self, vip):
		self.add_param('vip', vip)

