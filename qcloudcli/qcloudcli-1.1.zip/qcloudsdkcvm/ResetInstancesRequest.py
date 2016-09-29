#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ResetInstancesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'ResetInstances', 'cvm.api.qcloud.com')

	def get_instanceId(self):
		return self.get_params().get('instanceId')

	def set_instanceId(self, instanceId):
		self.add_param('instanceId', instanceId)

	def get_imageType(self):
		return self.get_params().get('imageType')

	def set_imageType(self, imageType):
		self.add_param('imageType', imageType)

	def get_imageId(self):
		return self.get_params().get('imageId')

	def set_imageId(self, imageId):
		self.add_param('imageId', imageId)

	def get_password(self):
		return self.get_params().get('password')

	def set_password(self, password):
		self.add_param('password', password)

