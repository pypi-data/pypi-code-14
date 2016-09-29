#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyVpnConnRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'ModifyVpnConn', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_vpnGwId(self):
		return self.get_params().get('vpnGwId')

	def set_vpnGwId(self, vpnGwId):
		self.add_param('vpnGwId', vpnGwId)

	def get_vpnConnId(self):
		return self.get_params().get('vpnConnId')

	def set_vpnConnId(self, vpnConnId):
		self.add_param('vpnConnId', vpnConnId)

	def get_preSharedKey(self):
		return self.get_params().get('preSharedKey')

	def set_preSharedKey(self, preSharedKey):
		self.add_param('preSharedKey', preSharedKey)

	def get_remoteSlaIp(self):
		return self.get_params().get('remoteSlaIp')

	def set_remoteSlaIp(self, remoteSlaIp):
		self.add_param('remoteSlaIp', remoteSlaIp)

	def get_propoEncryAlgorithm(self):
		return self.get_params().get('propoEncryAlgorithm')

	def set_propoEncryAlgorithm(self, propoEncryAlgorithm):
		self.add_param('propoEncryAlgorithm', propoEncryAlgorithm)

	def get_propoAuthenAlgorithm(self):
		return self.get_params().get('propoAuthenAlgorithm')

	def set_propoAuthenAlgorithm(self, propoAuthenAlgorithm):
		self.add_param('propoAuthenAlgorithm', propoAuthenAlgorithm)

	def get_exchangeMode(self):
		return self.get_params().get('exchangeMode')

	def set_exchangeMode(self, exchangeMode):
		self.add_param('exchangeMode', exchangeMode)

	def get_localIdentity(self):
		return self.get_params().get('localIdentity')

	def set_localIdentity(self, localIdentity):
		self.add_param('localIdentity', localIdentity)

	def get_localAddress(self):
		return self.get_params().get('localAddress')

	def set_localAddress(self, localAddress):
		self.add_param('localAddress', localAddress)

	def get_localFqdnName(self):
		return self.get_params().get('localFqdnName')

	def set_localFqdnName(self, localFqdnName):
		self.add_param('localFqdnName', localFqdnName)

	def get_remoteIdentity(self):
		return self.get_params().get('remoteIdentity')

	def set_remoteIdentity(self, remoteIdentity):
		self.add_param('remoteIdentity', remoteIdentity)

	def get_remoteAddress(self):
		return self.get_params().get('remoteAddress')

	def set_remoteAddress(self, remoteAddress):
		self.add_param('remoteAddress', remoteAddress)

	def get_remoteFqdnName(self):
		return self.get_params().get('remoteFqdnName')

	def set_remoteFqdnName(self, remoteFqdnName):
		self.add_param('remoteFqdnName', remoteFqdnName)

	def get_dhGroupName(self):
		return self.get_params().get('dhGroupName')

	def set_dhGroupName(self, dhGroupName):
		self.add_param('dhGroupName', dhGroupName)

	def get_ikeSaLifetimeSeconds(self):
		return self.get_params().get('ikeSaLifetimeSeconds')

	def set_ikeSaLifetimeSeconds(self, ikeSaLifetimeSeconds):
		self.add_param('ikeSaLifetimeSeconds', ikeSaLifetimeSeconds)

	def get_encryptAlgorithm(self):
		return self.get_params().get('encryptAlgorithm')

	def set_encryptAlgorithm(self, encryptAlgorithm):
		self.add_param('encryptAlgorithm', encryptAlgorithm)

	def get_integrityAlgorith(self):
		return self.get_params().get('integrityAlgorith')

	def set_integrityAlgorith(self, integrityAlgorith):
		self.add_param('integrityAlgorith', integrityAlgorith)

	def get_ipsecSaLifetimeSeconds(self):
		return self.get_params().get('ipsecSaLifetimeSeconds')

	def set_ipsecSaLifetimeSeconds(self, ipsecSaLifetimeSeconds):
		self.add_param('ipsecSaLifetimeSeconds', ipsecSaLifetimeSeconds)

	def get_ipsecSaLifetimeTraffic(self):
		return self.get_params().get('ipsecSaLifetimeTraffic')

	def set_ipsecSaLifetimeTraffic(self, ipsecSaLifetimeTraffic):
		self.add_param('ipsecSaLifetimeTraffic', ipsecSaLifetimeTraffic)

	def get_pfsDhGroup(self):
		return self.get_params().get('pfsDhGroup')

	def set_pfsDhGroup(self, pfsDhGroup):
		self.add_param('pfsDhGroup', pfsDhGroup)

	def get_vpnConnName(self):
		return self.get_params().get('vpnConnName')

	def set_vpnConnName(self, vpnConnName):
		self.add_param('vpnConnName', vpnConnName)

	def get_spdAcl(self):
		return self.get_params().get('spdAcl')

	def set_spdAcl(self, spdAcl):
		self.add_param('spdAcl', spdAcl)

	def get_userGwCidrBlock(self):
		return self.get_params().get('userGwCidrBlock')

	def set_userGwCidrBlock(self, userGwCidrBlock):
		self.add_param('userGwCidrBlock', userGwCidrBlock)

