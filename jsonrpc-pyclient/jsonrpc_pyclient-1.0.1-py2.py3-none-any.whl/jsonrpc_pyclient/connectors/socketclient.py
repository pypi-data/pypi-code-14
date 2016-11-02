"""Sockets json-rpc client transport implementations."""

import socket
import logging
from abc import ABCMeta
from abc import abstractmethod

# configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.ERROR)


class SocketClient(object):
    """Base class for all socket clients."""

    __metaclass__ = ABCMeta

    def __init__(self, ip, port, buffersize=64):
        """SocketClient can't be instantiated."""
        pass

    def send_rpc_message(self, message):
        """
        Send a json-rpc request to a server.

        args:
            message -- json-rpc request string

        returns:
            json-rpc response string (None if an error occurs)
        """
        self._connect()
        self._send(message)
        response = self._receieve()
        self._socketFd.close()
        return response

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _send(self, message):
        pass

    @abstractmethod
    def _receieve(self):
        pass


class TcpSocketClient(SocketClient):
    """Socket client transport that uses tcp sockets."""

    def __init__(self, ip, port, buffersize=64):
        """
        Create TcpSocketClient object.

        usage:
            TcpSocketClient('127.0.0.1', 6462)
            TcpSocketClient('127.0.0.1', 6462, 1024)

        args:
            ip          -- server's ip address
            port        -- server's port number
            BUFFER_SIZE -- size of receive buffer
        """
        self.ip = ip
        self.port = port
        self.buffersize = buffersize
        self._error = False

    def _connect(self):
        """Connect to the socket at (ip, port)."""
        global _logger

        if not self._error:
            self._socketFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self._socketFd.connect((self.ip, self.port))
            except OSError as e:
                # If something went wrong, let's log it, set an error flag
                # for future function calls, and then move on.
                _logger.error('error connecting to (%s, %d): %s', self.ip, self.port, e)
                self._error = True

    def _send(self, message):
        """Send message to server."""
        global _logger

        if not self._error:
            try:
                self._socketFd.sendall(message.encode())
            except OSError as e:
                # If something went wrong, let's log it, set an error flag
                # for future function calls, and then move on.
                _logger.error('error sending to socket: %s', e)
                self._error = True

    def _receieve(self):
        """Receive response from server."""
        global _logger

        if not self._error:
            result = ''
            try:
                # Receieve response data until we reach
                # the response delimiter ('\n').
                while '\n' not in result:
                    received = self._socketFd.recv(self.buffersize).decode()
                    result += received
            except OSError as e:
                # If something went wrong, let's log it, set an error flag
                # for future function calls, and then move on.
                # Since _receive is supposed to return the server's
                # response, we'll return None to indicate that
                # we couldn't get a response due to some sort of error.
                _logger.error('error receiving from socket: %s', e)
                self._error = True
                return None
            else:
                return result
