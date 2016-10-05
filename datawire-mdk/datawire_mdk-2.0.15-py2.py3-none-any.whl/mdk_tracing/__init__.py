# Quark 1.0.443 run at 2016-10-05 18:08:41.189562
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
import quark
import mdk_runtime
import mdk_introspection


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
        self.url = u"wss://tracing.datawire.io/ws/v1"
        self.queryURL = u"https://tracing.datawire.io/api/v1/logs"
        self.token = None
        self.lastPoll = 0
        self._context = _TLS(SharedContextInitializer())
        self._client = None
        self.runtime = None

    def __init__(self, runtime):
        self._init()
        (self).runtime = runtime

    @staticmethod
    def withURLsAndToken(url, queryURL, token):
        newTracer = Tracer(mdk_runtime.defaultRuntime());
        (newTracer).url = url
        if (((queryURL) == (None)) or ((len(queryURL)) == (0))):
            parsedURL = quark.URL.parse(url);
            if (((parsedURL).scheme) == (u"ws")):
                (parsedURL).scheme = u"http"
            else:
                (parsedURL).scheme = u"https"

            (parsedURL).path = u"/api/v1/logs"
            (newTracer).queryURL = (parsedURL).toString()
        else:
            (newTracer).queryURL = queryURL

        (newTracer).token = token
        return newTracer

    def _openIfNeeded(self):
        if ((self._client) == (None)):
            self._client = mdk_tracing.protocol.TracingClient(self, self.runtime)

        if ((self.token) == (None)):
            self.token = mdk_introspection.DatawireToken.getToken((self.runtime).getEnvVarsService())

    def stop(self):
        if ((self._client) != (None)):
            ((self.runtime).dispatcher).stopActor(self._client);

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
        (self)._openIfNeeded();
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

    def poll(self):
        (self)._openIfNeeded();
        (self.logger).trace(u"Polling for logs...");
        rightNow = quark.now();
        result = self.query(self.lastPoll, rightNow);
        self.lastPoll = rightNow
        return (result).andThen(quark._BoundMethod(self, u"deresultify", _List([])))

    def subscribe(self, handler):
        self._openIfNeeded();
        (self._client).subscribe(handler);

    def deresultify(self, result):
        (self.logger).trace(((u"got ") + (_toString(len((result).result)))) + (u" log events"));
        return (result).result

    def query(self, startTimeMillis, endTimeMillis):
        """
        Query the trace logs. startTimeMillis and endTimeMillis are milliseconds since the UNIX epoch.
        """
        args = _List([]);
        reqID = u"Query ";
        if ((startTimeMillis) >= ((0))):
            (args).append((u"startTime=") + (_toString(startTimeMillis)));
            reqID = (reqID) + (_toString(startTimeMillis))

        reqID = (reqID) + (u"-")
        if ((endTimeMillis) >= ((0))):
            (args).append((u"endTime=") + (_toString(endTimeMillis)));
            reqID = (reqID) + (_toString(endTimeMillis))

        url = (self).queryURL;
        if ((len(args)) > (0)):
            url = ((url) + (u"?")) + ((u"&").join(args))

        req = _HTTPRequest(url);
        (req).setMethod(u"GET");
        (req).setHeader(u"Content-Type", u"application/json");
        (req).setHeader(u"Authorization", (u"Bearer ") + ((self).token));
        return (quark.IO.httpRequest(req)).andThen(quark._BoundMethod(self, u"handleQueryResponse", _List([])))

    def handleQueryResponse(self, response):
        code = (response).getCode();
        body = (response).getBody();
        if ((code) == (200)):
            return mdk_tracing.api.GetLogEventsResult.decode(body)
        else:
            error = u"";
            if ((len(body)) > (0)):
                error = body

            if ((len(error)) < (1)):
                error = (u"HTTP response ") + (_toString(code))

            (self.logger).error((u"query failure: ") + (error));
            return quark.HTTPError(error)

    def _getClass(self):
        return u"mdk_tracing.Tracer"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"queryURL")):
            return (self).queryURL

        if ((name) == (u"token")):
            return (self).token

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

        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"queryURL")):
            (self).queryURL = _cast(value, lambda: unicode)

        if ((name) == (u"token")):
            (self).token = _cast(value, lambda: unicode)

        if ((name) == (u"lastPoll")):
            (self).lastPoll = _cast(value, lambda: int)

        if ((name) == (u"_context")):
            (self)._context = _cast(value, lambda: _TLS)

        if ((name) == (u"_client")):
            (self)._client = _cast(value, lambda: mdk_tracing.protocol.TracingClient)

        if ((name) == (u"runtime")):
            (self).runtime = _cast(value, lambda: mdk_runtime.MDKRuntime)


Tracer.quark_List_mdk_tracing_protocol_LogEvent__ref = None
Tracer.mdk_tracing_Tracer_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_tracing")
