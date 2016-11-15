import jsonschema

from ..repo import scheduler

req_body = scheduler.update
req = {'body': req_body}


def validate_put(item):
    jsonschema.validate(item, req_body)
