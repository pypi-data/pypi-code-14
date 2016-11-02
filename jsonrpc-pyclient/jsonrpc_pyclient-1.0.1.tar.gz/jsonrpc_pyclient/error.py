"""json-rpc exceptions."""


class JsonRpcError(Exception):
    """Exception handler for errors coming from a json-rpc server."""

    def __init__(self, error_code, error_message):
        """
        Create JsonRpcError object.

        See http://www.jsonrpc.org/specification#error_object for
        information on standard json-rpc 2.0 error codes.

        usage:
            raise JsonRpcError('-32601', 'method not found')

        args:
            error_code       -- json-rpc error code
            error_message    -- json-rpc error message
        """
        self.error_code = error_code
        self.error_message = error_message
        # create an exception with the json-rpc error code and error message
        super(JsonRpcError, self).__init__('; '.join(['error ' + str(self.error_code), self.error_message]))
