#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeDeviceWebRequest(Request):

	def __init__(self):
		Request.__init__(self, 'bm', 'qcloudcliV1', 'DescribeDeviceWeb', 'bm.api.qcloud.com')

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_lanIps(self):
		return self.get_params().get('lanIps')

	def set_lanIps(self, lanIps):
		self.add_param('lanIps', lanIps)

	def get_wanIps(self):
		return self.get_params().get('wanIps')

	def set_wanIps(self, wanIps):
		self.add_param('wanIps', wanIps)

	def get_mgtIps(self):
		return self.get_params().get('mgtIps')

	def set_mgtIps(self, mgtIps):
		self.add_param('mgtIps', mgtIps)

	def get_instanceIds(self):
		return self.get_params().get('instanceIds')

	def set_instanceIds(self, instanceIds):
		self.add_param('instanceIds', instanceIds)

	def get_alias(self):
		return self.get_params().get('alias')

	def set_alias(self, alias):
		self.add_param('alias', alias)

	def get_vagueIp(self):
		return self.get_params().get('vagueIp')

	def set_vagueIp(self, vagueIp):
		self.add_param('vagueIp', vagueIp)

	def get_orderField(self):
		return self.get_params().get('orderField')

	def set_orderField(self, orderField):
		self.add_param('orderField', orderField)

	def get_order(self):
		return self.get_params().get('order')

	def set_order(self, order):
		self.add_param('order', order)

	def get_status(self):
		return self.get_params().get('status')

	def set_status(self, status):
		self.add_param('status', status)

