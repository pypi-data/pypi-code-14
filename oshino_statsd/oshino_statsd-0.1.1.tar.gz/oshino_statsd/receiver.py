import socketserver


class UdpHandler(socketserver.BaseRequestHandler):

    def __init__(self, *args, queue):
        self.q = queue
        super(UdpHandler, self).__init__(*args)

    def handle(self):
        data, _ = self.request
        self.q.put(data)


def run(host, port, q, logger):

    def bind_fn(request, addr, sock):
        return UdpHandler(request, addr, sock, queue=q)

    server = socketserver.UDPServer((host, port), bind_fn)
    logger.info("Starting UDP server on {0}:{1}".format(host, port))
    server.serve_forever()
