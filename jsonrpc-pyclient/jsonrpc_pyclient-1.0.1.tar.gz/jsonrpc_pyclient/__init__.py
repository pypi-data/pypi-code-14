"""
json-rpc client library.

jsonrpc_pyclient is a json-rpc 2.0 and 1.0 client library primarily intended for use with
libjson-rpc-cpp (https://github.com/tvannoy/libjson-rpc-cpp),
but can be used with other json-rpc server implementations.

This library is intended to be used with libjson-rpc-cpp's stubgenerator,
which takes a json-formatted specification file, and can then return server
and client stubs in various languages; the python client stub generator was
created to use this library. For more information on using the stubgenerator,
refer to libjson-rpc-cpp's documentation

This library is transportation agnostic. Currently, tcp socket and http
transport connectors are implemented, but new connectors can be added.

Much of this library's architecture was inspired by libjson-rpc-cpp's
architecture -- many thanks to cinemast (libjson-rpc-cpp's original author).

Basic usage:
    >>> from jsonrpc_pyclient.connectors import socketclient
    >>> import ClientStub #client stub created by libjson-rpc-cpp stubgenerator
    >>> connector = socketclient.TcpSocketClient("127.0.0.1", 8032)
    >>> client = ClientStub(connector)
    >>> result = client.addNumbers(4, 5)
    >>> print(result)
"""
__title__ = 'jsonrpc_pyclient'
__author__ = 'Trevor Vannoy <trevor.vannoy@flukecal.com>'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Fluke Calibration'
__all__ = ('batch', 'client', 'error',
           'protocolhandler', 'connectors')
