import json

import mock
from twisted.internet import defer, reactor, task
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.logger import Logger
from twisted.protocols.basic import LineReceiver
from twisted.python.failure import Failure
from twisted.trial.unittest import TestCase
from txlogstash import TCPJsonLineLogObserver


class LineReceiverLogger(LineReceiver):
    delimiter = "\n"

    def __init__(self, factory):
        self.factory = factory

    def lineReceived(self, line):
        self.factory.lineReceived(line)

    def connectionLost(self, reason):
        self.lineReceived(self.clearLineBuffer())


class LineReceiverLoggerFactory(Factory):
    protocol = LineReceiverLogger

    def __init__(self):
        self._lines = []

    def buildProtocol(self, addr):
        return self.protocol(self)

    def lineReceived(self, line):
        if len(line.strip()) == 0:
            return
        decoded = json.loads(line)
        self._lines.append(decoded)


class E2ETests(TestCase):
    def listen(self, endpoint, factory):
        d = endpoint.listen(factory)

        def registerCleanup(listeningPort):
            self.addCleanup(listeningPort.stopListening)
            return listeningPort
        d.addCallback(registerCleanup)
        return self.reportUnhandledErrors(d)

    def reportUnhandledErrors(self, d):
        def cleanup():
            if isinstance(d.result, Failure):
                return d
        self.addCleanup(cleanup)
        return d

    @defer.inlineCallbacks
    def setUp(self):
        self.factory = LineReceiverLoggerFactory()
        port = yield self.listen(TCP4ServerEndpoint(reactor, 0), self.factory)
        self.observer = TCPJsonLineLogObserver("tcp:127.0.0.1:%d" % (port.getHost().port))
        self.log = Logger(observer=self.observer)

    def assertLogged(self, **kwargs):
        for line in self.factory._lines:
            all_found = True
            for k, v in kwargs.items():
                if k not in line or line[k] != v:
                    all_found = False
                    break
            if all_found:
                return line

        def formatForCopyPaste(lines):
            ret = ""
            for item in lines:
                r = ",\n".join([k + "=" + repr(v) for k, v in item.items()])
                ret += "dict({})\n".format(r)
            return ret
        self.fail("Log not found {} in list of logged events:\n {}".format(
            kwargs, formatForCopyPaste(self.factory._lines)))

    @defer.inlineCallbacks
    def waitLogged(self, num_logs):
        # There is no other way to poll, as the log api does not (and shall not) return a defer
        while len(self.factory._lines) < num_logs:
            yield task.deferLater(reactor, .01, lambda: None)

    @defer.inlineCallbacks
    def test_basic(self):
        self.log.debug("bla")
        yield self.waitLogged(1)
        self.assertLogged(
            log_namespace=u'txlogstash.test_observer',
            log_level=u'debug',
            log_filename=u'txlogstash/test_observer.py',
            log_source=None,
            log_format=u'bla',
            log_line=mock.ANY,
            log_function=u'test_basic',
            log_time=mock.ANY,
            message=u'bla')

    @defer.inlineCallbacks
    def test_format(self):
        self.log.debug("bar {data!r}", data={'foo': 'bar'})
        yield self.waitLogged(1)
        self.assertLogged(message=u"bar {'foo': 'bar'}")

    @defer.inlineCallbacks
    def test_lots_log(self):
        NUM_LOGS = 10000
        for i in xrange(NUM_LOGS):
            self.log.debug("bar {data!r}", data={'foo': 'bar'})
        yield self.waitLogged(NUM_LOGS)
        self.assertLogged(message=u"bar {'foo': 'bar'}")

    @defer.inlineCallbacks
    def test_several_logs(self):
        NUM_LOGS = 100
        for i in xrange(NUM_LOGS):
            self.log.debug("bar {data!r}", data={'foo': 'bar'})
            yield task.deferLater(reactor, .02, lambda: None)
        yield self.waitLogged(NUM_LOGS)
        self.assertLogged(message=u"bar {'foo': 'bar'}")

    @defer.inlineCallbacks
    def test_log_failure(self):
        try:
            raise Exception('oh no')
        except Exception:
            self.log.failure(None)
        yield self.waitLogged(1)
        msg = self.assertLogged(log_failure=mock.ANY)
        self.assertIn("Traceback: <type 'exceptions.Exception'>: oh no", msg['message'])
        self.assertIn(__file__.replace(".pyc", ".py"), msg['message'])
