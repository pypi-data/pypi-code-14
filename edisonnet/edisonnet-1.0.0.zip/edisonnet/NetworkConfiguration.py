from edision import Edision
import os
import socket
import subprocess

#mode: Client, AP
class NetworkConfiguration:
    def __init__(self):
        self.edision = Edision()
    
    def test(self):
        print "ret = %d" % self.edision.checkNetwork()
    
    def setDHCP(self, ssid_name, ssid_password, encrypt_mode, identiy):
        print "set dhcp"
        self.edision.connectNetwork(ssid_name, ssid_password, encrypt_mode, identiy);

    # must use custom image edision
    def setStatic(self, ip_address, netmask, gateway):
        print "set static"

        if (self.edision.is_valid_ipv4_address(ip_address) == False) or (self.edision.is_valid_ipv4_address(netmask) == False) or (self.edision.is_valid_ipv4_address(gateway) == False):
            print "Invalid information"
            return 1
#        
#        if self.edision.isIPReachble(ip_address):
#            print "duplicate"
#            return 2

        self.edision.setStaticAddress(ip_address, netmask, gateway)
        
        return 0
    
    def setDNS(self, server1, server2):
        print "set dns"
        self.edision.setDNS(server1, server2)
    
    # if in AP mode - can't not scan
    def scanSSID(self):
        print "scan ssid"
        self.edision.scanForNetworks()

    # Tools on MAC can't not find
    def setAcessPoint(self, name, password):
        self.edision.setAP(True, name, password)




