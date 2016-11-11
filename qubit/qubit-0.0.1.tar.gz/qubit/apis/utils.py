import json
from functools import wraps
__all__ = ['jsonize', 'resp_wrapper']


def jsonize(fn):
    @wraps(fn)
    def handler(*args, **kwargs):
        data = fn(*args, **kwargs)
        return json.dumps(data, ensure_ascii=False)
    return handler


def resp_wrapper(fn):
    @wraps(fn)
    def handler(*args, **kwargs):
        resp = fn(*args, **kwargs)
        if not isinstance(resp, dict):
            resp = dict(data=resp)
        return dict(resp, result='ok', status_code='200')
    return handler
