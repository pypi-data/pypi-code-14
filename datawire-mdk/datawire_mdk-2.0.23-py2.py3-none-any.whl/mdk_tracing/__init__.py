# Quark 1.0.452 run at 2016-10-26 12:53:21.596699
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_tracing")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_tracing.api
import mdk_tracing.protocol
import mdk_runtime.actors
import mdk_protocol
import quark
import mdk_runtime
import mdk_rtp


class TracingDestination(object):
    """
    MDK can use this to handle logging on the Session.
    """

    def log(self, ctx, procUUID, level, category, text):
        """
        Send a log message to the server.
        """
        raise NotImplementedError('`TracingDestination.log` is an abstract method')

TracingDestination.mdk_tracing_TracingDestination_ref = None
class FakeTracer(_QObject):
    """
    In-memory testing of logs.
    """
    def _init(self):
        self.messages = _List([])

    def __init__(self): self._init()

    def log(self, ctx, procUUID, level, category, text):
        (self.messages).append({u"level": level, u"category": category, u"text": text, u"context": (ctx).traceId});

    def onStart(self, dispatcher):
        pass

    def onStop(self):
        pass

    def onMessage(self, origin, message):
        pass

    def _getClass(self):
        return u"mdk_tracing.FakeTracer"

    def _getField(self, name):
        if ((name) == (u"messages")):
            return (self).messages

        return None

    def _setField(self, name, value):
        if ((name) == (u"messages")):
            (self).messages = _cast(value, lambda: _List)


FakeTracer.mdk_tracing_FakeTracer_ref = None
class Tracer(_QObject):
    """
    Send log messages to the MCP server.
    """
    def _init(self):
        self.logger = quark._getLogger(u"MDK Tracer")
        self.lastPoll = 0
        self._client = None
        self.runtime = None

    def __init__(self, runtime, wsclient):
        self._init()
        (self).runtime = runtime
        (self)._client = mdk_tracing.protocol.TracingClient(self, wsclient)

    @staticmethod
    def withURLsAndToken(url, queryURL, token):
        """
        Backwards compatibility.
        """
        return Tracer.withURLAndToken(url, token)

    @staticmethod
    def withURLAndToken(url, token):
        runtime = mdk_runtime.defaultRuntime();
        wsclient = mdk_protocol.WSClient(runtime, mdk_rtp.getRTPParser(), url, token);
        ((runtime).dispatcher).startActor(wsclient);
        newTracer = Tracer(runtime, wsclient);
        ((runtime).dispatcher).startActor(newTracer);
        return newTracer

    def onStart(self, dispatcher):
        (dispatcher).startActor(self._client);

    def onStop(self):
        ((self.runtime).dispatcher).stopActor(self._client);

    def onMessage(self, origin, mesage):
        pass

    def log(self, ctx, procUUID, level, category, text):
        """
        Send a log message to the server.
        """
        (ctx).tick();
        (self.logger).trace((u"CTX ") + ((ctx).toString()));
        evt = mdk_tracing.protocol.LogEvent();
        (evt).context = (ctx).copy()
        (evt).timestamp = quark.now()
        (evt).node = procUUID
        (evt).level = level
        (evt).category = category
        (evt).contentType = u"text/plain"
        (evt).text = text
        (self._client).log(evt);

    def subscribe(self, handler):
        (self._client).subscribe(handler);

    def _getClass(self):
        return u"mdk_tracing.Tracer"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"lastPoll")):
            return (self).lastPoll

        if ((name) == (u"_client")):
            return (self)._client

        if ((name) == (u"runtime")):
            return (self).runtime

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"lastPoll")):
            (self).lastPoll = _cast(value, lambda: int)

        if ((name) == (u"_client")):
            (self)._client = _cast(value, lambda: mdk_tracing.protocol.TracingClient)

        if ((name) == (u"runtime")):
            (self).runtime = _cast(value, lambda: mdk_runtime.MDKRuntime)


Tracer.mdk_tracing_Tracer_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_tracing")
