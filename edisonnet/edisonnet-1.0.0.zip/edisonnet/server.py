import multiprocessing
import socket
import json
from edision import Edision

class Server(object):
    def __init__(self, hostname, port, callback):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.callback = callback
        self.edision = Edision()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def stop(self):
        print "stop"
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def start(self):
        self.logger.debug("listening")
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=self.__handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                                            s.fileno(),
                                            0x8915,  # SIOCGIFADDR
                                            struct.pack('256s', ifname[:15])
                                            )[20:24])
    
    def __handle(self, connection, address):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("process-%r" % (address,))
        try:
            logger.debug("Connected %r at %r", connection, address)
            while True:
                if self.edision.showWiFiMode() == "Master":
                    ssid = self.edision.getAPName()
                    mac = self.edision.getMAC()
                    str = "{mode:\"AP\", ssid=\"" + ssid + "\", mac: \"" + mac + "\"}"
                    connection.sendall(str)
                elif self.edision.showWiFiMode() == "Managed":
                    ip = self.edision.getIPAddress()
                    netmask = self.edision.getNetmask()
                    gateway = self.edision.getGateway()
                    ssid = self.edision.getCurrentSSID()
                    
                    str = "{mode: \"CLIENT\", ip: \"" + ip + "\", netmask: \"" + netmask + "\", gateway: \"" + gateway +"\", ssid: \"" + ssid + "\"}"
                    connection.sendall(str)
                
                data = connection.recv(1024)
                if data == "":
                    logger.debug("Socket closed remotely")
                    break
                self.callback(data)
                    
            logger.debug("Sent data")
        except:
            logger.exception("Problem handling request")
        finally:
            logger.debug("Closing socket")
            connection.close()
