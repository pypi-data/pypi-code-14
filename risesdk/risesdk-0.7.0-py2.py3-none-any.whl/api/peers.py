from . import helpers

def getList(**kwargs):
    query = ""
    if "state" in kwargs:
        query = helpers.addToQuery(query, "state", kwargs["state"])
    if "os" in kwargs:
        query = helpers.addToQuery(query, "os", kwargs["os"])
    if "version" in kwargs:
        query = helpers.addToQuery(query, "version", kwargs["version"])
    if "limit" in kwargs:
        query = helpers.addToQuery(query, "limit", kwargs["limit"])
    if "offset" in kwargs:
        query = helpers.addToQuery(query, "offset", kwargs["offset"])
    if "orderBy" in kwargs:
        query = helpers.addToQuery(query, "orderBy", kwargs["orderBy"])

    return helpers.send_request("GET", "/api/peers" + query)

def get(ip, port):
    return helpers.send_request("GET", "/api/peers/get?ip=" + ip + "&port=" + str(port))

def version():
    return helpers.send_request("GET", "/api/peers/version")
