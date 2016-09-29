#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteUserAclRequest(Request):

	def __init__(self):
		Request.__init__(self, 'iot', 'qcloudcliV1', 'DeleteUserAcl', 'iot.api.qcloud.com')

	def get_access(self):
		return self.get_params().get('access')

	def set_access(self, access):
		self.add_param('access', access)

	def get_topic(self):
		return self.get_params().get('topic')

	def set_topic(self, topic):
		self.add_param('topic', topic)

	def get_userName(self):
		return self.get_params().get('userName')

	def set_userName(self, userName):
		self.add_param('userName', userName)

