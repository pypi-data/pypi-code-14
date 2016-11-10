import json

import falcon
from falcon import status_codes

from pylib import marshmallow


def json_error_serializer(req, exception):
    err = exception.to_dict()
    return ('application/json', json.dumps(err))


class MalformedJSONError(falcon.HTTPError):

    def __init__(self, description, **kwargs):
        super().__init__(status_codes.HTTP_753, 'Malformed JSON', description, **kwargs)


class RequireJSON(object):

    def process_request(self, request, response):
        if not request.client_accepts_json:
            raise falcon.HTTPNotAcceptable('Can only send JSON responses.')

        if request.content_type is None and \
                (request.method != 'GET' and request.method != 'DELETE'):
            raise falcon.HTTPBadRequest('Incorrect header', 'No content type was provided')

        if request.method in ('POST', 'PUT') and \
                'application/json' not in request.content_type:
            raise falcon.HTTPUnsupportedMediaType('Request must be encoded as JSON.')


class JSONTranslator(object):

    def process_request(self, request, response):
        if request.content_length in (None, 0):
            return

        body = request.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body', 'A valid JSON document is required.')

        try:
            request.params.update(json.loads(body.decode('utf-8')))
        except (ValueError, UnicodeDecodeError):
            raise MalformedJSONError('Your request body is incorrect')


def response(response, schema, data, many=False):
    """
    Processes response to any request handler. The many parameter is used
    validating multiple entities at once.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig response :: Response -> Schema -> [a] | a -> Bool -> _
    """
    response.content_type == 'application/json'
    data = marshmallow.dump(schema, data, many=many)
    response.body = json.dumps(data)
