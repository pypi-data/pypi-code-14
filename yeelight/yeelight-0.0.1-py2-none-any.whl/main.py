import json
import socket


class Bulb(object):
    def __init__(self, ip, port=55443):
        self._ip = ip
        self._port = port
        self.__cmd_id = 0

    @property
    def _cmd_id(self):
        self.__cmd_id += 1
        return self.__cmd_id - 1

    def send_command(self, method, params=None):
        command = {
            "id": self._cmd_id,
            "method": method,
            "params": params,
        }

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))
        sock.send(json.dumps(command) + "\r\n")
        response = json.loads(sock.recv(4096))
        sock.close()
        return response
