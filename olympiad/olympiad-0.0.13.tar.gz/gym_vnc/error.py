import sys

class Error(Exception):
    pass

class RPCError(Error):
    pass

class ConnectionError(Error):
    pass
