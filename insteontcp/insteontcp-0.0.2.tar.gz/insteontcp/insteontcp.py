'''
Insteon PLM TCP Python Library

https://github.com/heathbar/insteon-hub-2012


Published under the MIT license - See LICENSE file for more details.
'''

 # pylint: disable=missing-docstring
import threading
import time
import queue
import socket
import io
import ipaddress
import struct
from struct import pack
from enum import IntEnum
    
class InsteonTCP():
    STD_MSG = b'\x02\x62'
    MSG_FLAG = b'\x0F'
    CMD_ON = b'\x11'
    CMD_OFF = b'\x13'
    CMD_INFO = b'\x10'
    LEVEL_MAX = b'\xFF'
    ZERO = b'\x00'
    ALL_LINK_CMD = b'\x02\x61'
    
    def __init__(self, host, port=9761, event_callback=print):
        self.__event_callback = event_callback

        self._queue = queue.Queue(maxsize=255)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))

        self._listener = threading.Thread(target=self.__message_listener)
        self._listener.daemon = True
        self._listener.start()

        self._sender = threading.Thread(target=self.__command_sender)
        self._sender.daemon = True
        self._sender.start()

    def info(self, id, callback):
        self.__standard_command(id, self.CMD_INFO)
                
    def turn_on(self, id):
        self.__standard_command(id, self.CMD_ON, self.LEVEL_MAX)
        
    def turn_off(self, id):
        self.__standard_command(id, self.CMD_OFF, self.LEVEL_MAX)

    def activate_scene(self, group_number):
        self.__send_command(self.ALL_LINK_CMD + bytes.fromhex(group_number) + self.CMD_ON + self.ZERO)

    def __standard_command(self, id, cmd1, cmd2=ZERO):
        self.__send_command(self.STD_MSG + bytes.fromhex(id) + self.MSG_FLAG + cmd1 + cmd2)

    def __send_command(self, cmd):
        self._queue.put(cmd)

    def __command_sender(self):
        """ Command sender. """
        sequence = -1

        while True:
            try:
                cmd = self._queue.get()
                self._sock.sendall(cmd)
            except:
                pass
    
    def __message_listener(self):
        """ message listener. """

        while True:
            try:
              # TODO: deal with the possibility that we didn't read an entire message
              data = self._sock.recv(64)
              self.__event_callback(data)
            except e:
                pass


# def echo_it(it):
#     print("%s", it)

# x = InsteonTCP('10.1.1.47', 9761, echo_it)

# x.info('428517')

# time.sleep(4)

# x.activate_scene('06')
# while 1:
#     time.sleep(1)