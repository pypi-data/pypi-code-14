"""
Client transport connectors for jsonrpc_pyclient.

This package contains connectors for Client objects.
The connectors in this package need to implement send_rpc_message.
"""

__author__ = 'Trevor Vannoy <trevor.vannoy@flukecal.com>'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Fluke Calibration'
__all__ = ('httpclient', 'socketclient')
