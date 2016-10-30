import json

from multicorn.utils import log_to_postgres, WARNING, ERROR
from pymongo import MongoClient


def getMongoConnection(options):
    host = '127.0.0.1'
    if 'host' in options:
        host = options['host']
    elif 'uri' in options:
        host = options['uri']
    else:
        log_to_postgres('Using default host: %s' % host, WARNING)

    port = 27017
    if 'port' in options:
        port = int(options['port'])
    else:
        log_to_postgres('Using default port: %i' % port, WARNING)

    client = None
    try:
        client = MongoClient(host=host, port=port)
    except Exception as e:
        log_to_postgres('could not connect to mongodb: %s' % str(e), ERROR)
    return client


def convertNestedItemsToJson(rows):
    if not isinstance(rows, dict):
        return
    for k, v in rows.items():
        if isinstance(rows[k], (list, dict)):
            rows[k] = json.dumps(v)
