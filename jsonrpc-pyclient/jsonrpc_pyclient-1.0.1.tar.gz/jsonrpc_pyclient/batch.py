"""json-rpc batch functionality."""

import json
import logging
import sys

# configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.ERROR)

# get the proper JSONDecodeError exception type
if sys.version < '3.5':
    JSONDecodeError = ValueError
else:
    JSONDecodeError = json.decoder.JSONDecodeError


class BatchRequest(object):
    """json-rpc batch request object."""

    def __init__(self):
        """Create BatchRequest object."""
        self.calls = []
        self._request_id = 0

    def add_call(self, method, parameters, is_notification):
        """
        Add method call to BatchRequest.

        For each new call, the request id is incremented, starting from 0.

        usage:
            add_call('hello', {'name': 'Bob'}, False)
            add_call('add', [1, 2], False)
            add_call('notification', None, True)

        args:
            method          -- name of method to invoke on server
            parameters      -- method parameters. If present, parameters must
                               be a json structured value ({}, []). If the
                               method doesn't take any parameters, use None.
            is_notification  -- whether or not the request is a notification

        returns:
            id of json-rpc request (None for a notification)
        """
        request = {}

        # populate json-rpc request fields
        request['jsonrpc'] = '2.0'
        request['method'] = method
        if parameters:
            request['params'] = parameters
        if not is_notification:
            self._request_id += 1
            return_id = self._request_id
            request['id'] = return_id
        else:
            return_id = None

        # add method call to BatchRequest
        self.calls.append(request)

        return return_id

    def format_request(self):
        """
        Format BatchRequest object into a json string.

        returns:
            json-rpc batch request string
        """
        # in libjson-rpc-cpp, requests and responses are delimited by \n
        return (json.dumps(self.calls) + '\n')

    def __str__(self):
        """Return string representation."""
        return str(self.calls)


class BatchResponse(object):
    """json-rpc batch response object."""

    def __init__(self):
        """Create BatchResponse object."""
        self.results = {}

    def add_result(self, response):
        """
        Add method result to BatchResponse.

        Each result is put into a dictionary with the response's id as the key.

        args:
            response    -- json-rpc response object
        """
        try:
            self.results[response['id']] = response['result']
        except KeyError:
            # there was an error; add the error code and message to results
            self.results[response['id']] = response['error']

    def get_result(self, id_):
        """
        Get method result by id.

        args:
            id_  -- json-rpc id of request/response

        returns:
            method result
        """
        try:
            result = self.results[id_]
        except KeyError:
            # if the id_ is invalid, let's return None and move on.
            result = None
        finally:
            return result

    def __str__(self):
        """Return string representation."""
        return str(self.results)

    def process_batch(self, batch_response):
        """
        Process json-rpc batch response string.

        This method takes a batch response string, loads it into a json array,
        and then adds the result of each response object into results.

        args:
            batch_response   -- json-rpc batch response string
        """
        global _logger

        if batch_response:
            try:
                responses = json.loads(batch_response)
            # XXX: JSONDecodeError doesn't exist in python < 3.4
            except JSONDecodeError as e:
                # The server should practically never return a string
                # that isn't properly json-formatted, but in the case
                # that something does go wrong (e.g. the network garbles
                # the string), we'll log the exception message with
                # the offending string.
                _logger.error('invalid json string - %s: %s', batch_response, e)
            else:
                for response in responses:
                    self.add_result(response)
