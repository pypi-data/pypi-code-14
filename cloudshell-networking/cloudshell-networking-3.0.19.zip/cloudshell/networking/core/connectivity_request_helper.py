from cloudshell.networking.core.json_request_helper import JsonRequestDeserializer


class ConnectivityRequestDeserializer(JsonRequestDeserializer):
    def __init__(self, d):
        """!!!Deprecated!!! Please use JsonRequestDeserializer instead
        Deserialize json in to complex object with multiple fields
        """

        JsonRequestDeserializer.__init__(self, d)
