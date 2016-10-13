# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
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
import mdk_protocol
import mdk_runtime.actors
import quark
import mdk_runtime
import mdk_rtp


class SharedContextInitializer(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def getValue(self):
        return _cast(None, lambda: mdk_protocol.SharedContext)

    def _getClass(self):
        return u"mdk_tracing.SharedContextInitializer"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
SharedContextInitializer.mdk_tracing_SharedContextInitializer_ref = None
class Tracer(_QObject):
    def _init(self):
        self.logger = quark._getLogger(u"MDK Tracer")
        self.lastPoll = 0
        self._context = _TLS(SharedContextInitializer())
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

    def initContext(self):
        (self._context).setValue(mdk_protocol.SharedContext());

    def joinContext(self, context):
        (self._context).setValue((context).start_span());

    def joinEncodedContext(self, encodedContext):
        newContext = mdk_protocol.SharedContext.decode(encodedContext);
        (self).joinContext(newContext);

    def getContext(self):
        return (self._context).getValue()

    def setContext(self, ctx):
        (self._context).setValue(ctx);

    def start_span(self):
        (self._context).setValue(((self).getContext()).start_span());

    def finish_span(self):
        (self._context).setValue(((self).getContext()).finish_span());

    def log(self, procUUID, level, category, text):
        """
        Send a log message to the server.
        """
        ctx = (self).getContext();
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

        if ((name) == (u"_context")):
            return (self)._context

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

        if ((name) == (u"_context")):
            (self)._context = _cast(value, lambda: _TLS)

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
