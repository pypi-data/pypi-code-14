#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ImportImageRequest(Request):

	def __init__(self):
		Request.__init__(self, 'image', 'qcloudcliV1', 'ImportImage', 'image.api.qcloud.com')

	def get_osType(self):
		return self.get_params().get('osType')

	def set_osType(self, osType):
		self.add_param('osType', osType)

	def get_osVersion(self):
		return self.get_params().get('osVersion')

	def set_osVersion(self, osVersion):
		self.add_param('osVersion', osVersion)

	def get_osBits(self):
		return self.get_params().get('osBits')

	def set_osBits(self, osBits):
		self.add_param('osBits', osBits)

	def get_imgFormat(self):
		return self.get_params().get('imgFormat')

	def set_imgFormat(self, imgFormat):
		self.add_param('imgFormat', imgFormat)

	def get_imgName(self):
		return self.get_params().get('imgName')

	def set_imgName(self, imgName):
		self.add_param('imgName', imgName)

	def get_imgDesc(self):
		return self.get_params().get('imgDesc')

	def set_imgDesc(self, imgDesc):
		self.add_param('imgDesc', imgDesc)

	def get_imgCosUrl(self):
		return self.get_params().get('imgCosUrl')

	def set_imgCosUrl(self, imgCosUrl):
		self.add_param('imgCosUrl', imgCosUrl)

