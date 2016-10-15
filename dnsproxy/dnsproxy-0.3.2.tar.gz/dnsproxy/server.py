import falcon
from gevent import socket
from gevent.pywsgi import WSGIServer

from dnsproxy.utils import setup_logging


class DNSResource:
    def on_get(self, req, resp, q):
        resp.content_type = 'text/plain; charset=utf-8'
        try:
            ip = socket.gethostbyname(q)
        except socket.gaierror:
            resp.status = falcon.HTTP_404
            resp.data = b'NXDOMAIN'
        else:
            resp.status = falcon.HTTP_200
            resp.data = ip.encode()


app = falcon.API()
app.add_route('/{q}', DNSResource())


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        '-b', '--bind', default='0.0.0.0:80',
        help='bind address. Default is "0.0.0.0:80"')
    parser.add_argument(
        '-l', '--loglevel', default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR'))
    args = parser.parse_args()

    setup_logging(args.loglevel)
    host, port = args.bind.split(':')
    WSGIServer((host, int(port)), app).serve_forever()


if __name__ == '__main__':
    main()
