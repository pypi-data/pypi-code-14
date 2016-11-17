import falcon
import json


class Head(object):
    def process_request(self, req, resp):
        if 'application/json' not in req.content_type:
            raise falcon.HTTPUnsupportedMediaType('111', href='')
            if not req.client_accepts_json:
                raise falcon.HTTPNotAcceptable('222', href='')
        return


class Wrap(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            req.context['doc'] = None
            return
        try:
            body = req.stream.read()
            req.context['doc'] = json.loads(body.decode('utf-8'))
        except:
            raise falcon.HTTPBadRequest('can not decode body', 'bbb')

    def process_response(self, req, resp, resource):
        if 'ret' not in req.context:
            return
        resp.body = json.dumps(req.context['ret'])


class Cors(object):
    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            resp.set_header('access-control-allow-origin', '*')
            resp.append_header('access-control-allow-methods', '*')
            resp.append_header('access-control-allow-credentials', 'true')
        return
