"""Http json-rpc client transport implementation."""
import requests
import logging

# configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.ERROR)


class HttpClient(object):
    """json-rpc http client transport."""

    def __init__(self, url):
        """
        Create HttpClient object.

        usage:
            HttpClient('http://hostname:port')
            HttpClient('http://127.0.0.1:8080')

        args:
            url     -- server url
        """
        self.url = url

    def send_rpc_message(self, message):
        """
        Send a json-rpc request to a server.

        args:
            message -- json-rpc request string

        returns:
            json-rpc response string (None if an error occurred)
        """
        try:
            response = requests.post(self.url, data=message)
            return response.text
        except requests.exceptions.RequestException as e:
            # If something goes wrong, we'll just log the exception
            # and move on so we don't totally break the client.
            # _logger.exception('http requests error')
            _logger.error('http requests error: %s', e)
            return None
