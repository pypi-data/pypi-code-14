import json
from threading import Thread

from six.moves import BaseHTTPServer


class FakeServer(object):
    def __init__(self):
        self.requests = []
        self.responses = []

        self.status = 204
        self.body = None

        class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
            def dispatch(handler, method):
                if len(self.responses) > 0:
                    status = self.responses[len(self.requests)].get('status', self.status)
                    body = self.responses[len(self.requests)].get('body', self.body)
                else:
                    status = self.status
                    body = self.body

                self.requests.append({
                    'method': method,
                    'path': handler.path,
                    'headers': handler.headers,
                })

                handler.send_response(status)

                if body is not None:
                    body = json.dumps(body).encode('utf-8')
                    handler.send_header('Content-Length', str(len(body)))
                    handler.send_header('Content-Type', 'application/json')

                handler.end_headers()

                if body is not None:
                    handler.wfile.write(body)

            def do_HEAD(handler):
                handler.dispatch('HEAD')

            def do_GET(handler):
                handler.dispatch('GET')

            def do_PUT(handler):
                handler.dispatch('PUT')

            def do_POST(handler):
                handler.dispatch('POST')

            def do_PATCH(handler):
                handler.dispatch('PATCH')

            def do_DELETE(handler):
                handler.dispatch('DELETE')

            def log_request(self, *args):
                pass  # Disable default logging

        self.server = BaseHTTPServer.HTTPServer(('localhost', 0), Handler)
        self.server.timeout = 0.5
        self.thread = Thread(target=self.server.serve_forever, args=(0.1,))
        self.thread.daemon = True
        self.thread.start()

    @property
    def url(self):
        return 'http://{0}:{1}'.format(*self.server.server_address)

    @property
    def request(self):
        """ Returns the last request """
        return self.requests[-1]

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
