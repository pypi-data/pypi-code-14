from . import helpers

def enable(secret, secondSecret, username):
    return helpers.send_request("PUT", "/api/delegates", {"secret" : secret, "secondSecret" : secondSecret, "username" : username})

def getList(**kwargs):
    query = ""
    if "limit" in kwargs:
        query = helpers.addToQuery(query, "limit", kwargs["limit"])
    if "offset" in kwargs:
        query = helpers.addToQuery(query, "offset", kwargs["offset"])
    if "orderBy" in kwargs:
        query = helpers.addToQuery(query, "orderBy", kwargs["orderBy"])

    return helpers.send_request("GET", "/api/delegates" + query)

def getByPublicKey(publicKey):
    return helpers.send_request("GET", "/api/delegates/get?publicKey=" + publicKey)

def getByUsername(username):
    return helpers.send_request("GET", "/api/delegates/get?username=" + username)

def count():
    return helpers.send_request("GET", "/api/delegates/count")

def getVoters(publicKey):
    return helpers.send_request("GET" , "/api/delegates/voters?publicKey=" + publicKey)

def enableForging(secret):
    return helpers.send_request("POST", "/api/delegates/forging/enable", { "secret" : secret })

def disableForging(secret):
    return helpers.send_request("POST", "/api/delegates/forging/disable", { "secret" : secret })

def getForgedByAccount(generatorPublicKey):
    return helpers.send_request("POST", "/api/delegates/forging/getForgedByAccount?generatorPublicKey=" + generatorPublicKey)
