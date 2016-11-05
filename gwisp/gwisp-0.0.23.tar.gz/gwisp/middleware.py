import json
import falcon
import datetime
from json import JSONEncoder
from bson import ObjectId
from urllib.parse import parse_qsl


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if req.content_type is None:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON or form.',
                    href='http://docs.examples.com/api/json')

            if 'application/json' in req.content_type:
                return
            if 'application/x-www-form-urlencoded' in req.content_type:
                return

            raise falcon.HTTPUnsupportedMediaType(
                'This API only supports requests encoded as JSON or form.',
                href='http://docs.examples.com/api/json')


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.timestamp()

        return JSONEncoder.default(self, obj)


class FormTranslator(object):
    def process_request(self, req, res):
        if req.content_type is None:
            return
        if 'application/x-www-form-urlencoded' not in req.content_type:
            return

        body = req.stream.read()
        req.context['body'] = dict(parse_qsl(body.decode('utf-8')))

    def process_response(self, req, res, data):
        return


class JsonTranslator(object):
    def __init__(self):
        self._json_encoder = JsonEncoder()

    def process_request(self, req, res):
        if req.content_type is None:
            return
        if 'application/json' not in req.content_type:
            return

        if req.content_length in (None, 0):
            req.context['body'] = None
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['body'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, res, data):
        res.body = self._json_encoder.encode(res.body)
