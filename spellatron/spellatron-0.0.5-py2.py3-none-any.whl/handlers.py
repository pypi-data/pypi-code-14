import json

import tornado.escape
import tornado.gen
import tornado.web


class ApiHandler(tornado.web.RequestHandler):

    def json_response(self, data, code=200):
        self.set_header('Content-Type', 'application/json')
        data["status"] = code
        self.write(json.dumps(data) + "\n")
        self.set_status(code)

    def error(self, message, code=400):
        self.set_header('Content-Type', 'application/json')
        self.json_response({'message': message}, code)


class CorrectionHandler(ApiHandler):

    def correct(self, word):
        return self.application.correction_service.correction(word)

    @tornado.gen.coroutine
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            if 'word' not in data:
                raise ValueError
        except ValueError:
            self.error(u'Wrong data provided')
        else:
            self.json_response({
                'correction': self.correct(data['word'])
            })
