#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CdnPusherRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'CdnPusher', 'cdn.api.qcloud.com')

	def get_urlInfos(self):
		return self.get_params().get('urlInfos')

	def set_urlInfos(self, urlInfos):
		self.add_param('urlInfos', urlInfos)

	def get_host(self):
		return self.get_params().get('host')

	def set_host(self, host):
		self.add_param('host', host)

	def get_sleep(self):
		return self.get_params().get('sleep')

	def set_sleep(self, sleep):
		self.add_param('sleep', sleep)

	def get_limitRate(self):
		return self.get_params().get('limitRate')

	def set_limitRate(self, limitRate):
		self.add_param('limitRate', limitRate)

