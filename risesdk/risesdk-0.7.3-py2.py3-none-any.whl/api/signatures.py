from . import helpers

def get(id):
    return helpers.send_request("GET", "/api/signatures/get?id=" + id)

def add(secret, secondSecret, publicKey=None):
    options = { "secret" : secret, "secondSecret" : secondSecret}
    if publicKey:
        options["publicKey"] = publicKey
    return helpers.send_request("PUT", "/api/signatures", options)
