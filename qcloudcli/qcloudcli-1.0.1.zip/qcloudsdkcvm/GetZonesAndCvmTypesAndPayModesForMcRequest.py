#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetZonesAndCvmTypesAndPayModesForMcRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cvm', 'qcloudcliV1', 'GetZonesAndCvmTypesAndPayModesForMc', 'cvm.api.qcloud.com')

