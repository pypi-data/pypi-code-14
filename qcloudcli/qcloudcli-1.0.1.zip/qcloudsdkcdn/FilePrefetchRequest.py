#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class FilePrefetchRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'FilePrefetch', 'cdn.api.qcloud.com')

	def get_items(self):
		return self.get_params().get('items')

	def set_items(self, items):
		self.add_param('items', items)

