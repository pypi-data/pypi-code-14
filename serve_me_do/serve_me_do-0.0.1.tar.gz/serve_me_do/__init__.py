#!/usr/bin/env python
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn


DEFAULT_PORT = 8000


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    print("Serving on 0.0.0.0:{}".format(DEFAULT_PORT))
    server_address = ('', DEFAULT_PORT)
    httpd = ThreadingSimpleServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
