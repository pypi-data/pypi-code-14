import logging
import six
import sys
if six.PY2:
    import Queue as queue
else:
    import queue
import threading
from twisted.internet import defer

from gym_vnc.twisty import reactor

logger = logging.getLogger(__name__)

class ErrorBuffer(object):
    def __init__(self):
        self.queue = queue.Queue()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if value is not None:
            self.record(value)

    def __call__(self, error):
        self.record(error)

    def record(self, error, wrap=True):
        logger.debug('Error in thread %s: %s', threading.current_thread().name, error)
        if wrap:
            error = format_error(error)

        try:
            self.queue.put_nowait(error)
        except queue.Full:
            pass

    def check(self, timeout=None):
        if timeout is None:
            timeout = 0

        try:
            error = self.queue.get(timeout=timeout)
        except queue.Empty:
            return
        else:
            raise error

    def blocking_check(self, timeout=None):
        # TODO: get rid of this method
        if timeout is None:
            while True:
                self.check(timeout=3600)
        else:
            self.check(timeout)


from twisted.python import failure
import traceback
import threading
from gym_vnc import error
def format_error(e):
    # errback automatically wraps everything in a Twisted Failure
    if isinstance(e, failure.Failure):
        e = e.value

    if isinstance(e, str):
        err_string = e
    elif six.PY2:
        err_string = traceback.format_exc(e).rstrip()
    else:
        err_string = ''.join(traceback.format_exception(type(e), e, e.__traceback__)).rstrip()

    if err_string == 'None':
        # Reasonable heuristic for exceptions that were created by hand
        last = traceback.format_stack()[-2]
        err_string = '{}\n  {}'.format(e, last)
    # Quick and dirty hack for now.
    err_string = err_string.replace('Connection to the other side was lost in a non-clean fashion', 'Connection to the other side was lost in a non-clean fashion (HINT: this generally actually means we got a connection refused error. Check that the remote is actually running.)')
    return error.Error(err_string)

def queue_get(local_queue):
    while True:
        try:
            result = local_queue.get(timeout=1000)
        except queue.Empty:
            pass
        else:
            return result

def blockingCallFromThread(f, *a, **kw):
    local_queue = queue.Queue()
    def _callFromThread():
        result = defer.maybeDeferred(f, *a, **kw)
        result.addBoth(local_queue.put)
    reactor.callFromThread(_callFromThread)
    result = queue_get(local_queue)
    if isinstance(result, failure.Failure):
        if result.frames:
            e = error.Error(str(result))
        else:
            e = result.value
        raise e
    return result

from gym import spaces
def repeat_space(space, n):
    return spaces.Tuple([space] * n)

import base64
import uuid
def random_alphanumeric(length=14):
    buf = []
    while len(buf) < length:
        entropy = base64.encodestring(uuid.uuid4().bytes).decode('ascii')
        bytes = [c for c in entropy if c.isalnum()]
        buf += bytes
    return ''.join(buf)[:length]


def best_effort(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except:
        if six.PY2:
            logging.error('Error in %s:', function.__name__)
            traceback.print_exc()
        else:
            logging.error('Error in %s:', function.__name__)
            logger.error(traceback.format_exc())
        return None
