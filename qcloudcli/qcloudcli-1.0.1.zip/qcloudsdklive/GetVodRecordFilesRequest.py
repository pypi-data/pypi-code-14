#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetVodRecordFilesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'live', 'qcloudcliV1', 'GetVodRecordFiles', 'live.api.qcloud.com')

	def get_channelId(self):
		return self.get_params().get('channelId')

	def set_channelId(self, channelId):
		self.add_param('channelId', channelId)

	def get_startTime(self):
		return self.get_params().get('startTime')

	def set_startTime(self, startTime):
		self.add_param('startTime', startTime)

	def get_pageNum(self):
		return self.get_params().get('pageNum')

	def set_pageNum(self, pageNum):
		self.add_param('pageNum', pageNum)

	def get_pageSize(self):
		return self.get_params().get('pageSize')

	def set_pageSize(self, pageSize):
		self.add_param('pageSize', pageSize)

