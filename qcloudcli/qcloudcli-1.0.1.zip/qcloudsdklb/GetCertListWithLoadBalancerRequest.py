#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetCertListWithLoadBalancerRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'GetCertListWithLoadBalancer', 'lb.api.qcloud.com')

	def get_certIds(self):
		return self.get_params().get('certIds')

	def set_certIds(self, certIds):
		self.add_param('certIds', certIds)

