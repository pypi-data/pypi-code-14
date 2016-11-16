from functools import wraps

from flask import Flask
from flask import json
from flask.ext import restful
from flask_restful import reqparse

import shinkansen


class Api(restful.Api):
    def handle_error(self, e):
        if isinstance(e, shinkansen.UnrecoverableError):
            return self.make_response({'error': getattr(e, 'message', 'There was an error.')}, 400)
        return super(Api, self).handle_error(e)


app = Flask(__name__)
api = Api(app)


STATUS_CODES = {
    'failed': -1,
    'not_started': 0,
    'queued': 1,
    'in_progress': 2,
    'finished': 3,
    'empty': 4,
    'unknown': 99,
}


def keyed(func):
    @wraps(func)
    def ret(*args, **kwargs):
        result = func(*args, **kwargs)
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, help='the key of the result you want to extract')
        args = parser.parse_args()
        if 'key' in args and args['key'] is not None:
            if args['key'] not in result:
                msg = 'Key not in result'
                response = json.jsonify({'error': msg})
                response.status_code = 400
                return response
            return result[args['key']]
        return result
    return ret
