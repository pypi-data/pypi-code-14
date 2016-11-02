"""json-rpc protocol handler."""

import json
import logging
import sys

from jsonrpc_pyclient.error import JsonRpcError

# configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.ERROR)

# get the proper JSONDecodeError exception type
if sys.version < '3.5':
    JSONDecodeError = ValueError
else:
    JSONDecodeError = json.decoder.JSONDecodeError


class RpcProtocolHandler(object):
    """json-rpc protocol handler."""

    request_id = 0

    def __init__(self, version='2.0'):
        """
        Create RpcProtocolHandler object.

        args:
            version -- json-rpc server version ('1.0', '2.0')
        """
        self._version = version

    def build_request(self, method, parameters, is_notification):
        """
        Build json-rpc request string.

        usage:
            build_request('hello', {'name': 'Bob'}, False)
            build_request('add', [1, 2], False)
            build_request('notification', None, True)

        args:
            method          -- name of method to invoke on server
            parameters      -- method parameters. If present, parameters must
                               be a json structured value ({}, []). If the
                               method doesn't take any parameters, use None.
            is_notification  -- whether or not the request is a notification

        returns:
            a tuple of:
                json-rpc request string
                json-rpc request id (None for notifications)
        """
        request = {}

        # populate json-rpc request fields
        request['method'] = method
        if parameters:
            request['params'] = parameters

        if self._version == '2.0':
            request['jsonrpc'] = self._version

        if not is_notification:
            RpcProtocolHandler.request_id += 1
            req_id = RpcProtocolHandler.request_id
            request['id'] = req_id
        elif self._version == '1.0':
            req_id = None
            request['id'] = req_id
        else:
            req_id = None

        # convert json object into a string with a linefeed delimiter
        request = (json.dumps(request) + '\n')

        return request, req_id

    def handle_response(self, in_response):
        """
        Handle json-rpc response string.

        args:
            in_response  -- json-rpc response string

        returns:
            json-rpc result field (None if input string isn't valid json)
        """
        global _logger

        if in_response:
            try:
                response = json.loads(in_response)
            except JSONDecodeError as e:
                # The server should practically never return a string
                # that isn't properly json-formatted, but in the case
                # that something does go wrong (e.g. the network garbles
                # the string), we'll log the exception and move on.
                _logger.error('invalid json string - %s: %s', in_response, e)
                return None
            else:
                if 'result' in response:
                    return response['result']
                else:
                    # if there's no result field, that means an error
                    # occurred, so let's raise an exception.
                    raise JsonRpcError(response['error']['code'],
                                       response['error']['message'])
