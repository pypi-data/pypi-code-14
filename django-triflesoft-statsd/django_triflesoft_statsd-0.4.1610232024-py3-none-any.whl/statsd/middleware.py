class StatsMiddleware(object):
    def _send(self, metric):
        address = self._addresses[self._address_index]
        self._address_index = (self._address_index + 1) % len(address)

        try:
            self._sockets[address[0]].sendto(metric.encode('ascii'), address[1])
        except:
            pass

    def _begin_collect(self, request):
        from time import clock

        request._statsd_clock_from = clock()

    def _end_collect(self, request, event_type, status_code):
        from time import clock

        time_elapsed = int(1000 * (clock() - request._statsd_clock_from))

        for name, pattern in self._urls:
            if pattern.search(request.path):
                if name == '#view_name':
                    self._send('{}.{}.{}.{}.{}:{}|ms'.format(self._prefix, event_type, status_code, request.method, request.resolver_match.view_name, time_elapsed))
                else:
                    self._send('{}.{}.{}.{}.{}:{}|ms'.format(self._prefix, event_type, status_code, request.method, name, time_elapsed))

    def __init__(self, get_response):
        from django.conf import settings
        from re import compile
        from socket import getaddrinfo
        from socket import socket
        from socket import SOCK_DGRAM

        self._get_response = get_response
        self._addresses = []
        self._address_index = 0
        self._sockets = {}
        self._clock_from = 0
        self._prefix = settings.STATSD_PREFIX
        self._urls = []

        for url in settings.STATSD_URLS:
            if hasattr(url, '__iter__'):
                self._urls.append((url[0], compile(url[1]), ))
            else:
                self._urls.append(('#view_name', compile(url), ))

        infos = getaddrinfo(settings.STATSD_HOST, settings.STATSD_PORT, type=SOCK_DGRAM)

        for info in infos:
            family = info[0]
            address = info[4]

            self._addresses.append((family, address,))

            if not family in self._sockets:
                sock = socket(family=family, type=SOCK_DGRAM)
                sock.setblocking(True)
                self._sockets[family] = sock

    def __call__(self, request):
        self._begin_collect(request)
        response = self._get_response(request)
        self._end_collect(request, 'request', response.status_code)

        return response

    def process_exception(self, request, exception):
        self._end_collect(request, 'exception', 500)
