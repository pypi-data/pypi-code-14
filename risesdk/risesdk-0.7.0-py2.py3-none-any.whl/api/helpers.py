try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

global __BASE_URL__

def send_request(type, url, payload={}):
    func = getattr(requests, type.lower())
    fullUrl = urljoin(__BASE_URL__, url)
    return func(fullUrl, json=payload).json()

def addToQuery(query, name, param):
    if len(query) == 0:
        query += "?"
    else:
        query += "&"
    query += name + "=" + str(param)
    return query
