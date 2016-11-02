"""Base class for json-rpc clients."""

from jsonrpc_pyclient import protocolhandler
from jsonrpc_pyclient.batch import BatchResponse


class Client(object):
    """
    Base class for json-rpc clients.

    This class is a proxy for the server-side object
    where the actual processing happens.
    """

    def __init__(self, connector, version='2.0'):
        """
        Create Client object.

        usage:
            Client(connector)
            Client(connector, json-rpc_version)

        args:
            connector   -- transport connector (e.g. HttpClient)
            version     -- json-rpc server version ('1.0', '2.0')
        """
        self._connector = connector
        self._version = version
        self._protocol = protocolhandler.RpcProtocolHandler(version)

    def call_method(self, method, parameters):
        """
        Call method on json-rpc server.

        Sends a json-rpc request to a server, which then executes method
        and sends back the json-rpc response. If we don't get a valid (or any)
        response from the server, None will be returned.

        usage:
            call_method('hello', {'name': 'Bob'})
            call_method('add', [1, 2])
            call_method('noParams', None)

        args:
            method      -- name of method to invoke on server
            parameters  -- method parameters. If present, parameters must be
                           a json structured value ({}, []). If the method
                           doesn't take any parameters, use None.

        returns:
            the result of the remote method (can be None)
        """
        request, request_id = self._protocol.build_request(method, parameters, False)
        response = self._connector.send_rpc_message(request)
        result = self._protocol.handle_response(response)
        return result

    def call_notification(self, method, parameters):
        """
        Call method on json-rpc server.

        Sends a json-rpc request to a server, which then executes method,
        but doesn't send back a response.

        usage:
            call_notification('hello', {'name': 'Bob'})
            call_notification('add', [1, 2])
            call_notification('noParams', None)

        args:
            method      -- name of method to invoke on server
            parameters  -- method parameters. If present, parameters must be
                           a json structured value ({}, []). If the method
                           doesn't take any parameters, use None.
        """
        request, request_id = self._protocol.build_request(method, parameters, True)
        self._connector.send_rpc_message(request)

    def call_procedures(self, calls):
        """
        Send a batch of requests to a json-rpc server.

        The server handles each request, and then sends back a batch response.
        If we don't get a valid (or any) response from the server,
        None will be returned.

        usage:
            call_procedures(batch_call)

        args:
            calls   -- BatchResponse object containing several requests

        returns:
            a BatchResponse object (can be None)
        """
        batch = BatchResponse()
        responses = self._connector.send_rpc_message(calls.format_request())
        batch.process_batch(responses)
        return batch
