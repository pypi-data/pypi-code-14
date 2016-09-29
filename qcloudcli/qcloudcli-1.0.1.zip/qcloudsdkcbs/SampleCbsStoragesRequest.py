#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class SampleCbsStoragesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cbs', 'qcloudcliV1', 'SampleCbsStorages', 'cbs.api.qcloud.com')

