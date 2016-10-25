from . import helpers

def open(secret):
    return helpers.send_request("POST", "/api/accounts/open", { "secret" : secret })

def getBalance(address):
    return helpers.send_request("GET", "/api/accounts/getBalance?address=" + address)

def getPublicKey(address):
    return helpers.send_request("GET", "/api/accounts/getPublicKey?address=" + address)

def generatePublicKey(secret):
    return helpers.send_request("POST", "/api/accounts/generatePublicKey", { "secret" : secret })

def getAccount(address):
    return helpers.send_request("GET", "/api/accounts?address=" + address)

def getDelegates(address):
    return helpers.send_request("GET", "/api/accounts/delegates?address=" + address)

def putDelegates(secret, publicKey, delegates, secondSecret=None):
    options = { "secret" : secret, "publicKey" : publicKey, "delegates" : delegates }
    if secondSecret:
        options["secondSecret"] = secondSecret
    return helpers.send_request("PUT", "/api/accounts/delegates", options)
