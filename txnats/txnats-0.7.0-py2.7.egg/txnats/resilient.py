from __future__ import absolute_import

from twisted.internet import defer
from twisted.internet.endpoints import connectProtocol
from twisted.internet import error
from twisted.logger import Logger
log = Logger()

from .protocol import NatsProtocol
from . import actions


def sleep(own_reactor, seconds):
    d = defer.Deferred()
    own_reactor.callLater(seconds, d.callback, seconds)
    return d


@defer.inlineCallbacks
def connect(point, protocol, backoff, max_retries=100):
    while backoff.retries <= max_retries:
        log.debug("tries {}".format(backoff.retries))
        log.debug("connecting..")
        try:
            yield connectProtocol(point, protocol)
            backoff.reset_delay()
            log.debug(".connected")
            defer.returnValue(None)
        except (error.ConnectError, error.DNSLookupError):
            delay = backoff.get_delay()
            log.debug("connection failed, sleep for {}".format(delay))
            log.error()
            yield sleep(protocol.reactor, delay)

def make_reconnector(point, backoff, max_retries=100):
    def reconnector(event):
        if isinstance(event, actions.ConnectionLost):
            if event.protocol.ping_loop.running:
                event.protocol.ping_loop.stop()
            if not event.reason.check(error.ConnectionDone):
                protocol = NatsProtocol(
                    verbose=True, 
                    event_subscribers=event.protocol.event_subscribers, 
                    unsubs=event.protocol.unsubs)
                connect(point, protocol, backoff, max_retries)
    return reconnector