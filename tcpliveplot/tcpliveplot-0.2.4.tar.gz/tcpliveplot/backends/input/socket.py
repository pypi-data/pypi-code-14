# -*- coding: utf-8 -*-

import time
import socket
import threading
from ipaddress import ip_address
from collections import deque

from .input_base import InputBase

# to remove --> use optioms
DEFAULT_SOCKETSERVER_PORT = 11337
DEFAULT_SOCKETSERVER_LOCATION = 'localhost:' + str(DEFAULT_SOCKETSERVER_PORT)
LOG_FORMAT = ['time', 'srcIp', 'srcPort', 'dstIp', 'dstPort', 'cwnd', 'rwnd', 'sst', 'rtt', 'bw', 'loss']
#at least time & dstPort required
NUMBER_OF_VALUES = len(LOG_FORMAT)

LOGSERVER_CONNECT_RETRY_TIME = 1 #in s
LOGSERVER_ERROR_TIMEOUT = 0.5 #in s

class SocketInput(InputBase):
    def __init__(self, options, infoRegistry):
        self.options = options
        self.infoRegistry = infoRegistry
        self.__incomeBuffer = deque()
        self.incomeBuffer = deque()
        self.connectionUp = False
        self.socketUp = False
        self.__stopped = threading.Event()

        if(":" not in self.options.logServer): # only ipv4-address or hostname w/o port given
            ip = self.options.logServer
            port = DEFAULT_SOCKETSERVER_PORT
        elif(self.options.logServer.count(":") > 1): # ipv6-address given
            try:
                ip = ip_address(self.options.logServer)
            except ValueError:
                try:
                    ip, separator, port = self.options.logServer.rpartition(':')
                    self.logServerIp = ip_address(ip)
                except ValueError:
                    print("Fatal error (Log-Server location malformatted)... should not have done this...")
            else:
                port = DEFAULT_SOCKETSERVER_PORT
        else: # ipv4-address w/ port given
            ip, separator, port = self.options.logServer.rpartition(':')


        if(port is ''):
            port = DEFAULT_SOCKETSERVER_PORT


        try:
            self.logServerIp = ip_address(ip)
        except ValueError:
             self.logServerIp = ip_address(socket.gethostbyname(ip.strip("[]")))
        else:
            pass

        self.logServerPort = int(port)
        self.dst = str(self.logServerIp) + ":" + str(self.logServerPort)
        if(self.options.debug):
            print(str(self.dst))

    def startupCheck(self):
        pass

    def startUp(self):
        #TODO: eprint + debug..
        self.createSocket()

        while not self.connectToServer():
            if self.__stopped:
                return
            else:
                pass

    def createSocket(self):
        try:
            if(ip_address(self.logServerIp).version is 4):
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        except socket.error:
            print("Failed to create socket")
        else:
            self.socketUp = True
            if(self.options.debug):
                print("Socket created.")

    def connectToServer(self):
        try:
            self.socket.connect((str(self.logServerIp), self.logServerPort))
            self.connectionUp = True
            print("Successfully connected to " + self.dst + "")
            return True
        except socket.error:
            print("Error: Could not connect to " + self.dst + ". Retrying in " + str(LOGSERVER_CONNECT_RETRY_TIME) + "s ...")
            self.__stopped.wait(LOGSERVER_CONNECT_RETRY_TIME)
            return False
        else:
            self.__stopped.wait(LOGSERVER_CONNECT_RETRY_TIME)
            return False

    def reconnectToServer(self):
        if not self.socketUp:
            self.socket.close()
            self.createSocket()

        while not self.connectToServer():
            if self.__stopped:
                return
            else:
                pass

    def tearDown(self):
        self.__stopped.set()
        self.socket.close()
        pass

    def retrieveNewSamples(self):
        """
        Reads data (in blocks) from a socket and adds the received data to an temporaray income buffer.
        """

        self.retrieveDataFromSocket();
        self.processDataFromSocket();

        data = []
        while(True):
            try:
                dataLine = self.incomeBuffer.popleft()
            except IndexError:
                return data
            else:
                data.append(dataLine)


    def retrieveDataFromSocket(self):
        if(self.connectionUp):
            try:
                data = self.socket.recv(4096)
            except socket.timeout:
                print("Connection timeout.")
                self.socket.close()
                self.socketUp = False
                self.connectionUp = False
                return ""
            except IOError:
                print("Error: Could not retrieve data from " + self.dst)
                self.socket.close()
                self.socketUp = False
                self.connectionUp = False
                return ""
            else:
                if(len(data) == 0):
                    print("Connection closed by foreign host.")
                    self.socket.close()
                    self.socketUp = False
                    self.connectionUp = False
                else:
                    self.__incomeBuffer.append(data)
        else:
            self.reconnectToServer()


    def processDataFromSocket(self):
        """Reads data from the income buffer and tries to reassemble splitted data."""
        tmpBuffer = ""
        try:
            line = self.__incomeBuffer.popleft()
            line = line.decode("UTF-8")
            lines = line.split("\n")
        except IndexError:
            time.sleep(0.00001)
        else:
            for i in lines:
                data = i.split(" ")
                if(tmpBuffer != ""):
                    tmpBuffer += i
                    self.incomeBuffer.append(tmpBuffer)
                    tmpBuffer = ""
                    continue

                if(len(data) < NUMBER_OF_VALUES):
                    tmpBuffer += i
                else:
                    self.incomeBuffer.append(i)
