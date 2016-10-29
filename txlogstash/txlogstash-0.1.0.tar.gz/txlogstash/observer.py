from __future__ import absolute_import, division, print_function

import inspect
import traceback
from datetime import datetime
from sys import stdout

from twisted import logger
from twisted.internet import endpoints, protocol, reactor, task
from twisted.logger import eventAsJSON
from zope import interface


def format_timestamp(time):
    tstamp = datetime.utcfromtimestamp(time)
    return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

FILENAMES_PATHLEN = 3


def stripFilename(filename):
    return "/".join(filename.split("/")[-FILENAMES_PATHLEN:])


def frameAsJSON(frame):
    # having the frames as tuple in the json will make elasticsearch crash
    # as it requires to have same type for every element of a list
    if isinstance(frame[0], basestring):  # failure's frame
        return dict(
            function=frame[0],
            file=stripFilename(frame[1]),
            line=frame[2])
    else:  # inspect's frame
        return dict(
            file=stripFilename(frame[1]),
            line=frame[2],
            code="".join(frame[4]),
            function=frame[3])


def eventAsLogStashJSON(event):
    event['@timestamp'] = format_timestamp(event['log_time'])
    if 'log_logger' in event:
        del event['log_logger']

    if 'log_level' in event and hasattr(event['log_level'], 'name'):
        event['log_level'] = event['log_level'].name

    event['isError'] = bool(event.get('isError'))

    if event.get('log_failure') is not None:
        # twisted default serialization of failure will not work well with elasticsearch
        event['log_brieftraceback'] = event['log_failure'].getBriefTraceback()
        event['log_failure'] = event['log_failure'].__getstate__()
        event['log_failure']['frames'] = map(frameAsJSON, event['log_failure']['frames'])
        event['log_failure']['stack'] = map(frameAsJSON, event['log_failure']['stack'])

    if event.get('log_format') is None:
        if event.get('log_failure') is not None:
            event['log_format'] = "{log_brieftraceback}"
        else:
            event['log_format'] = "{message}"

    if 'log_format' in event and 'message' not in event:
        try:
            event['message'] = logger.formatEvent(event)
        except Exception:
            event['cannot_format'] = True
            event['cannot_format_why'] = traceback.format_exc()

    if 'message' in event and isinstance(event['message'], (list, tuple)):
        event['message'] = " ".join(event['message'])

    return eventAsJSON(event).encode('utf-8')


def findLoggingFrame(stack):
    ret = []
    for frame in stack[1:]:
        filename = frame[1]
        if filename.endswith("/_logger.py"):
            continue
        if filename.endswith("/logger/_observer.py"):
            continue
        if filename.endswith("/logger/_legacy.py"):
            continue
        if filename.endswith("/python/log.py"):
            continue
        return frameAsJSON(frame)
    return ret


class LineLogger(protocol.Protocol):
    noisy = False

    def __init__(self, lines):
        self.lines = lines

    def connectionMade(self):
        for line in self.lines:
            self.transport.write(line + "\n")
        self.transport.loseConnection()


class LogStashFactory(protocol.Factory):
    noisy = False

    def __init__(self):
        self._lines = []

    def appendLine(self, line):
        self._lines.append(line)

    def buildProtocol(self, addr):
        self._lines, lines = [], self._lines
        return LineLogger(lines)


@interface.implementer(logger.ILogObserver)
class TCPJsonLineLogObserver(object):
    def __init__(self, endpoint, formatter=eventAsLogStashJSON):
        self.endpoint = endpoint
        self.formatter = formatter
        self.deferred = None
        self.factory = LogStashFactory()

    def emit(self, event):
        if 'metric' in event:
            return
        try:
            event['log_frame'] = findLoggingFrame(inspect.stack())
        except Exception:
            pass
        try:
            eventline = self.formatter(event)
        except Exception:
            stdout.write("Unable to format log event: " + traceback.format_exc())
            return

        if self.deferred is None:
            self.deferred = task.deferLater(reactor, 0, self._connect, reactor)

            @self.deferred.addCallback
            def cleanup(_):
                self.deferred = None

            @self.deferred.addErrback
            def onRefused(err):
                stdout.write(repr(err) + "\n")
        self.factory.appendLine(eventline)

    __call__ = emit

    def _connect(self, _, _reactor=reactor):
        endpoint = endpoints.clientFromString(_reactor, self.endpoint)
        return endpoint.connect(self.factory)
