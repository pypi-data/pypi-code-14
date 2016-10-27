# Quark 1.0.452 run at 2016-10-27 18:40:40.198005
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


class LogEvent(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.context = None
        self.timestamp = None
        self.node = None
        self.level = None
        self.category = None
        self.contentType = None
        self.text = None

    def __init__(self):
        super(LogEvent, self).__init__();

    def getTimestamp(self):
        return (self).timestamp

    def toString(self):
        return ((((((((((((((u"<LogEvent ") + (_toString(self.timestamp))) + (u" ")) + ((self.context).toString())) + (u", ")) + (self.node)) + (u", ")) + (self.level)) + (u", ")) + (self.category)) + (u", ")) + (self.contentType)) + (u", ")) + (self.text)) + (u">")

    def _getClass(self):
        return u"mdk_tracing.protocol.LogEvent"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return LogEvent._json_type

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

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            LogEvent._json_type = _cast(value, lambda: unicode)

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


LogEvent._json_type = u"log"
LogEvent.mdk_tracing_protocol_LogEvent_ref = None
class Subscribe(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)

    def __init__(self):
        super(Subscribe, self).__init__();

    def toString(self):
        return u"<Subscribe>"

    def _getClass(self):
        return u"mdk_tracing.protocol.Subscribe"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Subscribe._json_type

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Subscribe._json_type = _cast(value, lambda: unicode)


Subscribe._json_type = u"subscribe"
Subscribe.mdk_tracing_protocol_Subscribe_ref = None
class LogAck(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.sequence = None

    def __init__(self):
        super(LogAck, self).__init__();

    def toString(self):
        return ((u"<LogAck ") + (_toString(self.sequence))) + (u">")

    def _getClass(self):
        return u"mdk_tracing.protocol.LogAck"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return LogAck._json_type

        if ((name) == (u"sequence")):
            return (self).sequence

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            LogAck._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"sequence")):
            (self).sequence = _cast(value, lambda: int)


LogAck._json_type = u"logack"
LogAck.mdk_tracing_protocol_LogAck_ref = None
class TracingClient(_QObject):
    def _init(self):
        self._tracer = None
        self._started = False
        self._mutex = _Lock()
        self._handler = None
        self._dispatcher = None
        self._wsclient = None
        self._sock = None
        self._sendWithAcks = None

    def __init__(self, tracer, wsclient):
        self._init()
        self._tracer = tracer
        self._wsclient = wsclient
        self._sendWithAcks = mdk_protocol.SendWithAcks()
        (wsclient).subscribe(self);

    def subscribe(self, handler):
        """
        Attach a subscriber that will receive results of queries.
        """
        (self._mutex).acquire();
        self._handler = handler
        (self._mutex).release();

    def onStart(self, dispatcher):
        (self)._dispatcher = dispatcher

    def onStop(self):
        pass

    def onMessage(self, origin, message):
        mdk_protocol._subscriberDispatch(self, message);

    def onWSConnected(self, websock):
        (self._mutex).acquire();
        (self)._sock = websock
        ((self)._sendWithAcks).onConnected(self, (self)._dispatcher, websock);
        if ((self._handler) != (None)):
            ((self)._dispatcher).tell(self, (Subscribe()).encode(), (self)._sock);

        (self._mutex).release();

    def onPump(self):
        (self._mutex).acquire();
        ((self)._sendWithAcks).onPump(self, (self)._dispatcher, (self)._sock);
        (self._mutex).release();

    def onMessageFromServer(self, message):
        type = (quark.reflect.Class.get(_getClass(message))).id;
        if ((type) == (u"mdk_tracing.protocol.LogEvent")):
            event = _cast(message, lambda: LogEvent);
            self.onLogEvent(event);
            return

        if ((type) == (u"mdk_tracing.protocol.LogAck")):
            ack = _cast(message, lambda: LogAck);
            (self).onLogAck(ack);
            return

    def onLogEvent(self, evt):
        (self._mutex).acquire();
        if ((self._handler) != (None)):
            (self._handler)(evt) if callable(self._handler) else (self._handler).call(evt);

        (self._mutex).release();

    def onLogAck(self, ack):
        (self._mutex).acquire();
        ((self)._sendWithAcks).onAck((ack).sequence);
        (self._mutex).release();

    def log(self, evt):
        """
        Queue a log message for delivery to the server.
        """
        (self._mutex).acquire();
        ((self)._sendWithAcks).send(LogEvent._json_type, evt);
        (self._mutex).release();

    def _getClass(self):
        return u"mdk_tracing.protocol.TracingClient"

    def _getField(self, name):
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

        if ((name) == (u"_wsclient")):
            return (self)._wsclient

        if ((name) == (u"_sock")):
            return (self)._sock

        if ((name) == (u"_sendWithAcks")):
            return (self)._sendWithAcks

        return None

    def _setField(self, name, value):
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

        if ((name) == (u"_wsclient")):
            (self)._wsclient = _cast(value, lambda: mdk_protocol.WSClient)

        if ((name) == (u"_sock")):
            (self)._sock = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"_sendWithAcks")):
            (self)._sendWithAcks = _cast(value, lambda: mdk_protocol.SendWithAcks)


TracingClient.mdk_tracing_protocol_TracingClient_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_tracing.protocol")
