# Quark 1.0.443 run at 2016-10-05 18:08:41.189562
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_tracing.protocol")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_protocol
import mdk_tracing
import quark
import mdk_runtime.actors
import mdk_runtime


class TracingHandler(object):

    def onLogEvent(self, event):
        pass

    def onLogAck(self, ack):
        pass

    def onSubscribe(self, sub):
        pass

TracingHandler.mdk_tracing_protocol_TracingHandler_ref = None
class TracingEvent(mdk_protocol.ProtocolEvent):
    """
    A single event in the stream that Tracing has to manage.
    """
    def _init(self):
        mdk_protocol.ProtocolEvent._init(self)

    def __init__(self):
        super(TracingEvent, self).__init__();

    @staticmethod
    def construct(type):
        result = mdk_protocol.ProtocolEvent.construct(type);
        if ((result) != (None)):
            return result

        if ((LogEvent._discriminator).matches(type)):
            return LogEvent()

        if ((LogAck._discriminator).matches(type)):
            return LogAck()

        if ((Subscribe._discriminator).matches(type)):
            return Subscribe()

        return _cast(None, lambda: mdk_protocol.ProtocolEvent)

    @staticmethod
    def decode(encoded):
        return _cast(mdk_protocol.Serializable.decodeClassName(u"mdk_tracing.protocol.TracingEvent", encoded), lambda: mdk_protocol.ProtocolEvent)

    def dispatch(self, handler):
        self.dispatchTracingEvent(_cast(handler, lambda: TracingHandler));

    def dispatchTracingEvent(self, handler):
        raise NotImplementedError('`TracingEvent.dispatchTracingEvent` is an abstract method')

    def _getClass(self):
        return u"mdk_tracing.protocol.TracingEvent"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
TracingEvent.mdk_tracing_protocol_TracingEvent_ref = None
class LogEvent(TracingEvent):
    def _init(self):
        TracingEvent._init(self)
        self.context = None
        self.timestamp = None
        self.node = None
        self.level = None
        self.category = None
        self.contentType = None
        self.text = None
        self.sequence = None
        self.sync = None

    def __init__(self):
        super(LogEvent, self).__init__();

    def dispatchTracingEvent(self, handler):
        (handler).onLogEvent(self);

    def toString(self):
        return ((((((((((((((((u"<LogEvent ") + (_toString(self.sequence))) + (u" @")) + (_toString(self.timestamp))) + (u" ")) + ((self.context).toString())) + (u", ")) + (self.node)) + (u", ")) + (self.level)) + (u", ")) + (self.category)) + (u", ")) + (self.contentType)) + (u", ")) + (self.text)) + (u">")

    def _getClass(self):
        return u"mdk_tracing.protocol.LogEvent"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return LogEvent._discriminator

        if ((name) == (u"context")):
            return (self).context

        if ((name) == (u"timestamp")):
            return (self).timestamp

        if ((name) == (u"node")):
            return (self).node

        if ((name) == (u"level")):
            return (self).level

        if ((name) == (u"category")):
            return (self).category

        if ((name) == (u"contentType")):
            return (self).contentType

        if ((name) == (u"text")):
            return (self).text

        if ((name) == (u"sequence")):
            return (self).sequence

        if ((name) == (u"sync")):
            return (self).sync

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            LogEvent._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)

        if ((name) == (u"context")):
            (self).context = _cast(value, lambda: mdk_protocol.SharedContext)

        if ((name) == (u"timestamp")):
            (self).timestamp = _cast(value, lambda: int)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: unicode)

        if ((name) == (u"level")):
            (self).level = _cast(value, lambda: unicode)

        if ((name) == (u"category")):
            (self).category = _cast(value, lambda: unicode)

        if ((name) == (u"contentType")):
            (self).contentType = _cast(value, lambda: unicode)

        if ((name) == (u"text")):
            (self).text = _cast(value, lambda: unicode)

        if ((name) == (u"sequence")):
            (self).sequence = _cast(value, lambda: int)

        if ((name) == (u"sync")):
            (self).sync = _cast(value, lambda: int)


LogEvent._discriminator = mdk_protocol.anyof(_List([u"log"]))
LogEvent.mdk_tracing_protocol_LogEvent_ref = None
class Subscribe(TracingEvent):
    def _init(self):
        TracingEvent._init(self)

    def __init__(self):
        super(Subscribe, self).__init__();

    def dispatchTracingEvent(self, handler):
        (handler).onSubscribe(self);

    def toString(self):
        return u"<Subscribe>"

    def _getClass(self):
        return u"mdk_tracing.protocol.Subscribe"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Subscribe._discriminator

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Subscribe._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)


Subscribe._discriminator = mdk_protocol.anyof(_List([u"subscribe"]))
Subscribe.mdk_tracing_protocol_Subscribe_ref = None
class LogAck(TracingEvent):
    def _init(self):
        TracingEvent._init(self)
        self.sequence = None

    def __init__(self):
        super(LogAck, self).__init__();

    def dispatchTracingEvent(self, handler):
        (handler).onLogAck(self);

    def toString(self):
        return ((u"<LogAck ") + (_toString(self.sequence))) + (u">")

    def _getClass(self):
        return u"mdk_tracing.protocol.LogAck"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return LogAck._discriminator

        if ((name) == (u"sequence")):
            return (self).sequence

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            LogAck._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)

        if ((name) == (u"sequence")):
            (self).sequence = _cast(value, lambda: int)


LogAck._discriminator = mdk_protocol.anyof(_List([u"logack", u"mdk_tracing.protocol.LogAckEvent"]))
LogAck.mdk_tracing_protocol_LogAck_ref = None
class TracingClient(mdk_protocol.WSClient):
    def _init(self):
        mdk_protocol.WSClient._init(self)
        self._tracer = None
        self._started = False
        self._mutex = _Lock()
        self._handler = None
        self._dispatcher = None
        self._syncRequestPeriod = 5000
        self._syncInFlightMax = 50
        self._buffered = _List([])
        self._inFlight = _List([])
        self._logged = 0
        self._sent = 0
        self._failedSends = 0
        self._recorded = 0
        self._lastSyncTime = 0
        self._myLog = quark._getLogger(u"TracingClient")

    def __init__(self, tracer, runtime):
        super(TracingClient, self).__init__(runtime);
        (self)._dispatcher = (runtime).dispatcher
        self._tracer = tracer

    def _debug(self, message):
        s = ((((u"[") + (_toString(len(self._buffered)))) + (u" buf, ")) + (_toString(len(self._inFlight)))) + (u" inf] ");
        (self._myLog).debug((s) + (message));

    def url(self):
        return (self._tracer).url

    def token(self):
        return (self._tracer).token

    def isStarted(self):
        (self._mutex).acquire();
        result = ((self._started) or ((len(self._buffered)) > (0))) or ((self._handler) != (None));
        (self._mutex).release();
        return result

    def _startIfNeeded(self):
        if (not (self._started)):
            ((self)._dispatcher).startActor(self);
            self._started = True

    def subscribe(self, handler):
        (self._mutex).acquire();
        self._handler = handler
        self._startIfNeeded();
        (self._mutex).release();

    def onStart(self, dispatcher):
        super(TracingClient, self).onStart(dispatcher);

    def onStop(self):
        self._started = False
        super(TracingClient, self).onStop();

    def startup(self):
        (self._mutex).acquire();
        while ((len(self._inFlight)) > (0)):
            evt = (self._inFlight).pop((len(self._inFlight)) - (1));
            (self._buffered).insert((0), (evt));
            self._failedSends = (self._failedSends) + ((1))
            self._debug((u"no ack for #") + (_toString((evt).sequence)));

        self._debug((u"Starting up! with connection ") + (_toString((self).sock)));
        if ((self._handler) != (None)):
            ((self).dispatcher).tell(self, (Subscribe()).encode(), (self).sock);

        (self._mutex).release();

    def pump(self):
        (self._mutex).acquire();
        while ((len(self._buffered)) > (0)):
            debugSuffix = u"";
            evt = (self._buffered).pop(0);
            (self._inFlight).append(evt);
            if ((((evt).timestamp) > ((self._lastSyncTime) + (self._syncRequestPeriod))) or ((len(self._inFlight)) == (self._syncInFlightMax))):
                (evt).sync = 1
                self._lastSyncTime = (evt).timestamp
                debugSuffix = u" with sync set"

            ((self).dispatcher).tell(self, (evt).encode(), (self).sock);
            (evt).sync = 0
            self._sent = (self._sent) + ((1))
            self._debug(((((u"sent #") + (_toString((evt).sequence))) + (debugSuffix)) + (u" to ")) + (_toString((self).sock)));

        (self._mutex).release();

    def onWSMessage(self, message):
        event = TracingEvent.decode(message);
        if ((event) == (None)):
            return

        (event).dispatch(self);

    def onLogEvent(self, evt):
        (self._mutex).acquire();
        if ((self._handler) != (None)):
            (self._handler)(evt) if callable(self._handler) else (self._handler).call(evt);

        (self._mutex).release();

    def onLogAck(self, ack):
        (self._mutex).acquire();
        while ((len(self._inFlight)) > (0)):
            if ((((self._inFlight)[0]).sequence) <= ((ack).sequence)):
                evt = (self._inFlight).pop(0);
                self._recorded = (self._recorded) + ((1))
                self._debug((((u"ack #") + (_toString((ack).sequence))) + (u", discarding #")) + (_toString((evt).sequence)));
            else:
                break;

        (self._mutex).release();

    def log(self, evt):
        (self._mutex).acquire();
        (evt).sequence = self._logged
        (evt).sync = 0
        self._logged = (self._logged) + ((1))
        (self._buffered).append(evt);
        self._debug((u"logged #") + (_toString((evt).sequence)));
        self._startIfNeeded();
        (self._mutex).release();

    def _getClass(self):
        return u"mdk_tracing.protocol.TracingClient"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"firstDelay")):
            return (self).firstDelay

        if ((name) == (u"maxDelay")):
            return (self).maxDelay

        if ((name) == (u"reconnectDelay")):
            return (self).reconnectDelay

        if ((name) == (u"ttl")):
            return (self).ttl

        if ((name) == (u"tick")):
            return (self).tick

        if ((name) == (u"sock")):
            return (self).sock

        if ((name) == (u"sockUrl")):
            return (self).sockUrl

        if ((name) == (u"lastConnectAttempt")):
            return (self).lastConnectAttempt

        if ((name) == (u"lastHeartbeat")):
            return (self).lastHeartbeat

        if ((name) == (u"timeService")):
            return (self).timeService

        if ((name) == (u"schedulingActor")):
            return (self).schedulingActor

        if ((name) == (u"websockets")):
            return (self).websockets

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"_tracer")):
            return (self)._tracer

        if ((name) == (u"_started")):
            return (self)._started

        if ((name) == (u"_mutex")):
            return (self)._mutex

        if ((name) == (u"_handler")):
            return (self)._handler

        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        if ((name) == (u"_syncRequestPeriod")):
            return (self)._syncRequestPeriod

        if ((name) == (u"_syncInFlightMax")):
            return (self)._syncInFlightMax

        if ((name) == (u"_buffered")):
            return (self)._buffered

        if ((name) == (u"_inFlight")):
            return (self)._inFlight

        if ((name) == (u"_logged")):
            return (self)._logged

        if ((name) == (u"_sent")):
            return (self)._sent

        if ((name) == (u"_failedSends")):
            return (self)._failedSends

        if ((name) == (u"_recorded")):
            return (self)._recorded

        if ((name) == (u"_lastSyncTime")):
            return (self)._lastSyncTime

        if ((name) == (u"_myLog")):
            return (self)._myLog

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"firstDelay")):
            (self).firstDelay = _cast(value, lambda: float)

        if ((name) == (u"maxDelay")):
            (self).maxDelay = _cast(value, lambda: float)

        if ((name) == (u"reconnectDelay")):
            (self).reconnectDelay = _cast(value, lambda: float)

        if ((name) == (u"ttl")):
            (self).ttl = _cast(value, lambda: float)

        if ((name) == (u"tick")):
            (self).tick = _cast(value, lambda: float)

        if ((name) == (u"sock")):
            (self).sock = _cast(value, lambda: mdk_runtime.WSActor)

        if ((name) == (u"sockUrl")):
            (self).sockUrl = _cast(value, lambda: unicode)

        if ((name) == (u"lastConnectAttempt")):
            (self).lastConnectAttempt = _cast(value, lambda: int)

        if ((name) == (u"lastHeartbeat")):
            (self).lastHeartbeat = _cast(value, lambda: int)

        if ((name) == (u"timeService")):
            (self).timeService = _cast(value, lambda: mdk_runtime.Time)

        if ((name) == (u"schedulingActor")):
            (self).schedulingActor = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"websockets")):
            (self).websockets = _cast(value, lambda: mdk_runtime.WebSockets)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_tracer")):
            (self)._tracer = _cast(value, lambda: mdk_tracing.Tracer)

        if ((name) == (u"_started")):
            (self)._started = _cast(value, lambda: bool)

        if ((name) == (u"_mutex")):
            (self)._mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"_handler")):
            (self)._handler = _cast(value, lambda: quark.UnaryCallable)

        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_syncRequestPeriod")):
            (self)._syncRequestPeriod = _cast(value, lambda: int)

        if ((name) == (u"_syncInFlightMax")):
            (self)._syncInFlightMax = _cast(value, lambda: int)

        if ((name) == (u"_buffered")):
            (self)._buffered = _cast(value, lambda: _List)

        if ((name) == (u"_inFlight")):
            (self)._inFlight = _cast(value, lambda: _List)

        if ((name) == (u"_logged")):
            (self)._logged = _cast(value, lambda: int)

        if ((name) == (u"_sent")):
            (self)._sent = _cast(value, lambda: int)

        if ((name) == (u"_failedSends")):
            (self)._failedSends = _cast(value, lambda: int)

        if ((name) == (u"_recorded")):
            (self)._recorded = _cast(value, lambda: int)

        if ((name) == (u"_lastSyncTime")):
            (self)._lastSyncTime = _cast(value, lambda: int)

        if ((name) == (u"_myLog")):
            (self)._myLog = value

    def onSubscribe(self, sub):
        pass
TracingClient.mdk_tracing_protocol_TracingClient_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_tracing.protocol")
