from NetworkConfiguration import NetworkConfiguration
from ConfigParser import SafeConfigParser
import sys
from server import Server
import logging
from parser import Parser
import multiprocessing
import socket
import fcntl
import struct
from edision import Edision
import time
import os
import subprocess
import constant

global nw_config
global server
global parser

def checkNetworkStatus():
    #get mode: AP, Client
    edision = Edision()
    mode = edision.showWiFiMode()

    if mode == "Master":
        print "Working mode: AP"
        return 0
    elif mode == "Managed":
        print "Working mode: Client"
        ip = edision.getIPAddress()
        print "ip " + ip

        # Network error
        if ip == "":
            edision.setAPDefault()
            return 1
        else:
            if edision.isIPReachble(edision.getGateway()):
                print "Client mode ok"
                return 0;
            else:
                print "Client mode can't connect to gate way"
                edision.setAPDefault()
                return 1

######### 3 callbacks receive command from remote ##########
def on_receive_ap_command(ap_name, ap_password):
    global nw_config
    
    print "ap name:" + ap_name
    print "ap pass:" + ap_password
    
    nw_config.setAcessPoint(ap_name, ap_password)
    close_tcp_server()
    time.sleep(5)
    startServer()

def on_receive_dhcp_command(ssid_name, ssid_password, ssid_security, ssid_identity):
    global nw_config
    
    print "ssid name:" + ssid_name
    print "ssid password:" + ssid_password
    print "ssid security:" + ssid_security
    print "ssid identity:" + ssid_identity
    
    nw_config.setDHCP(ssid_name, ssid_password, ssid_security, ssid_identity)
    close_tcp_server()

def on_receive_static_command(ip, netmask, gateway, dns1, dns2):
    global nw_config
    
    print "ip:" + ip
    print "netmask:" + netmask
    print "gateway:" + gateway
    print "dns1:" + dns1
    print "dns2:" + dns2
    
    #close_tcp_server()
    nw_config.setDNS(dns1, dns2)
    nw_config.setStatic(ip, netmask, gateway)

    close_tcp_server()


######### tcp server callback ##########
def on_receive_data(data):
    print "data " + data
    global parser
    
    parser.parse(data)

def close_tcp_server():
    print "close socket"
    global server
    
    for process in multiprocessing.active_children():
        process.terminate()
        process.join()
    
    server.stop()

def startServer():
    global server
    
    checkNetworkStatus()
    
    #### start tcp server
    logging.basicConfig(level=logging.DEBUG)
    p = SafeConfigParser()
    p.read(constant.HOME + '/config.ini')
    
    ip = Edision().getIPAddress()
    
    port = p.getint('TCP', 'port')
    server = Server(ip, port, on_receive_data)
    
    try:
        print "Listening"
        server.start()
    except Exception, e:
        print str(e)
    finally:
        print "Shutting down"
        for process in multiprocessing.active_children():
            print "Shutting down process %r"
            process.terminate()
            process.join()
            print "All done"
        startServer()

def main():
    global parser
    global server
    global nw_config

    time.sleep(10)

    nw_config = NetworkConfiguration()
    parser = Parser(on_receive_ap_command, on_receive_dhcp_command, on_receive_static_command)
    
    startServer()
    
    while (1):
        pass



if __name__ == "__main__":
    main()
