#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class Md5CheckRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'Md5Check', 'cdn.api.qcloud.com')

	def get_url(self):
		return self.get_params().get('url')

	def set_url(self, url):
		self.add_param('url', url)

