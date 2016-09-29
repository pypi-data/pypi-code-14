#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetInfoByBucketRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'GetInfoByBucket', 'cdn.api.qcloud.com')

	def get_bucket(self):
		return self.get_params().get('bucket')

	def set_bucket(self, bucket):
		self.add_param('bucket', bucket)

	def get_cosId(self):
		return self.get_params().get('cosId')

	def set_cosId(self, cosId):
		self.add_param('cosId', cosId)

	def get_startRow(self):
		return self.get_params().get('startRow')

	def set_startRow(self, startRow):
		self.add_param('startRow', startRow)

	def get_rowNum(self):
		return self.get_params().get('rowNum')

	def set_rowNum(self, rowNum):
		self.add_param('rowNum', rowNum)

