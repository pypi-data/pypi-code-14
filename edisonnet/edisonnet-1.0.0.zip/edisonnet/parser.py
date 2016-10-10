from edision import Edision
import os
import socket
import subprocess
import json

class Parser:
    def __init__(self, callback_ap, callback_dhcp, callback_static):
        self.callback_ap = callback_ap
        self.callback_dhcp = callback_dhcp
        self.callback_static = callback_static
    
    def parse(self, data):
        try:
            d = json.loads(data)
            mode = d["mode"]
            
            if mode == "AP":
                ap_name = d["ap_name"]
                ap_password = d["ap_password"]
                self.callback_ap(ap_name, ap_password)
            
            elif mode == "DHCP":
                ssid_name = d["ssid_name"]
                ssid_password = d["ssid_password"]
                ssid_security = d["ssid_security"]
                ssid_identity = d["ssid_identity"]
                self.callback_dhcp(ssid_name, ssid_password, ssid_security, ssid_identity)
            
            elif mode == "STATIC":
                ip = d["ip"]
                netmask = d["netmask"]
                gateway = d["gateway"]
                dns1 = d["dns1"]
                dns2 = d["dns2"]
                self.callback_static(ip, netmask, gateway, dns1, dns2)
        except Exception, e:
            print "Error: data format is incorrect"
            print str(e)




    




