#!/usr/bin/env python
# -*- coding: utf-8 -*-


from cStringIO import StringIO

__author__ = 'bac'


class Chunkit(object):
    def __init__(self, application):
        self.application = application.wsgi_app
        application.wsgi_app = self

    def __call__(self, environ, start_response):

        if environ.get('HTTP_TRANSFER_ENCODING', '0') == 'chunked':
            del environ['HTTP_TRANSFER_ENCODING']

            uwsgi_way = True
            try:
                import uwsgi
            except:
                uwsgi_way = False

            if uwsgi_way:
                body = uwsgi.chunked_read()
                if body:
                    content_length = len(body)
            else:

                input = environ.get('wsgi.input')
                if input:
                    body = ''
                    size = int(input.readline(), 16)
                    while size > 0:
                        body += input.read(size + 2)
                        size = int(input.readline(), 16)
                    content_length = len(body) - 2 if body else 0

            if body:
                environ['body_copy'] = body
                environ["HTTP_CONTENT_LENGTH"] = content_length
                environ["CONTENT_LENGTH"] = content_length
                environ['wsgi.input'] = StringIO(body)

        app_iter = self.application(environ,
                                    self._sr_callback(start_response))
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):
            start_response(status, headers, exc_info)

        return callback
