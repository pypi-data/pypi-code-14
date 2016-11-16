import random
import re
import signal
import time

from gym_vnc import error
from gym_vnc.twisty import reactor
from twisted.internet import defer, protocol, task
import twisted.internet.error
import logging

logger = logging.getLogger(__name__)

class ConnectionTimer(protocol.Protocol):
    def connectionMade(self):
        self.transport.loseConnection()

def connection_timer_factory():
    factory = protocol.ClientFactory()
    factory.protocol = ConnectionTimer
    return factory

class StopWatch(object):
    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time

# TODO: clean this up
def start(endpoint, max_attempts=5):
    # Use an object for timing so that we can mutate it within the closure
    stop_watch = StopWatch()
    stop_watch.start()

    factory = connection_timer_factory()
    d = endpoint.connect(factory)
    def success(client):
        return stop_watch.stop()
    d.addCallback(success)
    # d.addErrback(error)

    # def error(failure, attempt):
    #     # websocketpp can fail when connections are lost too quickly
    #     if attempt == max_attempts:
    #         d.errback(error.ConnectionError('Connection timer exceeded {} retries'.format(max_retries)))
    #         return

    #     backoff = 1.5 ** (attempt + 1) + random.randint(42, 100)
    #     logger.error('Connection timer: error connecting to websocket server (retrying in %dms, %d retries remaining): %s', backoff, retry, failure)
    #     d = task.deferLater(reactor, backoff / 1000., go, retry - 1)
    #     return d

    # def go(retry):
    #     stop_watch.start()
    #     factory = connection_timer_factory()
    #     d = endpoint.connect(factory)
    #     d.addCallback(success)
    #     d.addErrback(error, retry)

    return d

def measure_clock_skew(label, host):
    cmd = ['ntpdate', '-q', host]
    logger.info('[%s] Starting network calibration with %s', label, ' '.join(cmd))
    skew = Clockskew(label, cmd)
    # TODO: search PATH for this?
    process = reactor.spawnProcess(skew, '/usr/sbin/ntpdate', cmd, {})
    # process = reactor.spawnProcess(skew, '/bin/sleep', ['sleep', '2'], {})

    def timeout():
        if process.pid:
            logger.info('[%s] %s call timed out; killing the subprocess', ' '.join(cmd), label)
            process.signalProcess(signal.SIGKILL)
            process.reapProcess()
    reactor.callLater(3, timeout)
    return skew.deferred

class Clockskew(protocol.ProcessProtocol):
    def __init__(self, label, cmd):
        self.label = label
        self._cmd = cmd

        protocol.ProcessProtocol.__init__(self)
        self.deferred = defer.Deferred()
        self.out = []
        self.err = []

    def outReceived(self, data):
        self.out.append(data)

    def errReceived(self, data):
        self.err.append(data)

    def processExited(self, reason):
        if isinstance(reason.value, twisted.internet.error.ProcessDone):
            out = b''.join(self.out).decode('utf-8')
            match = re.search('offset ([\d.-]+) sec', out)
            if match is not None:
                offset = float(match.group(1))
                self.deferred.callback(offset)
            else:
                self.deferred.errback(error.Error('Could not parse offset: %s', out))
        else:
            err = b''.join(self.err)
            self.deferred.errback(error.Error('{} failed with status {}: stderr={!r}'.format(self._cmd, reason.value.exitCode, err)))
