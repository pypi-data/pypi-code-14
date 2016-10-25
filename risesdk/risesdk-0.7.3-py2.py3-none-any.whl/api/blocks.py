from . import helpers

def get(id):
    return helpers.send_request("GET", "/api/blocks/get?id=" + id)

def getList(**kwargs):
    query = ""
    if "generatorPublicKey" in kwargs:
        query = helpers.addToQuery(query, "generatorPublicKey", kwargs["generatorPublicKey"])
    if "totalFee" in kwargs:
        query = helpers.addToQuery(query, "totalFee", kwargs["totalFee"])
    if "totalAmount" in kwargs:
        query = helpers.addToQuery(query, "totalAmount", kwargs["totalAmount"])
    if "previousBlock" in kwargs:
        query = helpers.addToQuery(query, "previousBlock", kwargs["previousBlock"])
    if "height" in kwargs:
        query = helpers.addToQuery(query, "height", kwargs["height"])
    if "limit" in kwargs:
        query = helpers.addToQuery(query, "limit", kwargs["limit"])
    if "offset" in kwargs:
        query = helpers.addToQuery(query, "offset", kwargs["offset"])
    if "orderBy" in kwargs:
        query = helpers.addToQuery(query, "orderBy", kwargs["orderBy"])

    return helpers.send_request("GET", "/api/blocks" + query)

def getFee():
    return helpers.send_request("GET", "/api/blocks/getFee")

def getFeesSchedule():
    return helpers.send_request("GET", "/api/blocks/getFees")

def getReward():
    return helpers.send_request("GET", "/api/blocks/getReward")

def getSupply():
    return helpers.send_request("GET", "/api/blocks/getSupply")

def getHeight():
    return helpers.send_request("GET", "/api/blocks/getHeight")

def getStatus():
    return helpers.send_request("GET", "/api/blocks/getStatus")

def getNethash():
    return helpers.send_request("GET", "/api/blocks/getNethash")

def getMilestone():
    return helpers.send_request("GET", "/api/blocks/getMilestone")
