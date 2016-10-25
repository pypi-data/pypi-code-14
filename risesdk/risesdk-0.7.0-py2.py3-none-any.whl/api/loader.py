from . import helpers

def status():
    return helpers.send_request("GET", "/api/loader/status")

def syncStatus():
    return helpers.send_request("GET", "/api/loader/status/sync")
