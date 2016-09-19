import base64


def configure_basic_authentication(swagger_client, username, password):
    authentication_string = "%s:%s" % (username, password)
    base64_authentication_string = base64.b64encode(bytes(authentication_string))
    header_key = "Authorization"
    header_value = "Basic %s" % (base64_authentication_string, )
    swagger_client.api_client.default_headers[header_key] = header_value
