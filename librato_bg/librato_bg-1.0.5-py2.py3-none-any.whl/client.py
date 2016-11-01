from __future__ import unicode_literals

import logging

from six.moves import queue
from librato_bg.consumer import Consumer


class Client(object):
    """Create a new Librato BG client."""
    log = logging.getLogger('librato_bg')

    def __init__(self, user, token, debug=False, max_queue_size=10000, send=True, on_error=None):
        self.user = user
        self.token = token
        self.queue = queue.Queue(max_queue_size)
        self.consumer = Consumer(self.user, self.token, self.queue, on_error=on_error)
        self.on_error = on_error
        self.debug = debug
        self.send = send

        if debug:
            self.log.setLevel(logging.DEBUG)

        # if we've disabled sending, just don't start the consumer
        if send:
            self.consumer.start()

    def gauge(self, event, value, source):
        msg = {
            'event': event,
            'value': value,
            'source': source
        }

        return self._enqueue(msg)

    def _enqueue(self, msg):
        """Push a new `msg` onto the queue, return `(success, msg)`"""
        self.log.debug('queueing: %s', msg)

        if self.queue.full():
            self.log.warn('librato_bg queue is full')
            return False, msg

        self.queue.put(msg)
        self.log.debug('enqueued %s.', msg)
        return True, msg

    def flush(self):
        """Forces a flush from the internal queue to the server"""
        queue = self.queue
        size = queue.qsize()
        queue.join()
        self.log.debug('successfully flushed %s items.', size)

    def join(self):
        """Ends the consumer thread once the queue is empty. Blocks execution until finished"""
        self.consumer.pause()
        self.consumer.join()


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
        raise AssertionError(msg)
