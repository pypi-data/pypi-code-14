from . import helpers

def getList(**kwargs):
    query = ""
    if "blockId" in kwargs:
        query = helpers.addToQuery(query, "blockId", kwargs["blockId"])
    if "senderId" in kwargs:
        query = helpers.addToQuery(query, "senderId", kwargs["senderId"])
    if "recipientId" in kwargs:
        query = helpers.addToQuery(query, "recipientId", kwargs["recipientId"])
    if "limit" in kwargs:
        query = helpers.addToQuery(query, "limit", kwargs["limit"])
    if "offset" in kwargs:
        query = helpers.addToQuery(query, "offset", kwargs["offset"])
    if "orderBy" in kwargs:
        query = helpers.addToQuery(query, "orderBy", kwargs["orderBy"])

    return helpers.send_request("GET", "/api/transactions" + query)

def send(secret, amount, recipientId, publicKey, secondSecret=None):
    options = { "secret" : secret, "amount" : amount, "recipientId" : recipientId, "publicKey" : publicKey}
    if secondSecret:
        options["secondSecret"] = secondSecret
    return helpers.send_request("PUT", "/api/transactions", options)

def get(id):
    return helpers.send_request("GET", "/api/transactions/get?id=" + id)

def getUnconfirmed(id):
    return helpers.send_request("GET", "/api/transactions/unconfirmed/get?id=" + id)

def getUnconfirmedList():
    return helpers.send_request("GET", "/api/transactions/unconfirmed")
