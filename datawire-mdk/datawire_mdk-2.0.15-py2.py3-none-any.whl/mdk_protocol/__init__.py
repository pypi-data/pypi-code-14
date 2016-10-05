# Quark 1.0.443 run at 2016-10-05 18:08:41.189562
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_protocol")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent
import mdk_runtime.actors
import mdk_runtime
import quark.error


class Discriminator(_QObject):
    def _init(self):
        self.values = None

    def __init__(self, values):
        self._init()
        (self).values = values

    def matches(self, value):
        idx = 0;
        while ((idx) < (len(self.values))):
            if ((value) == ((self.values)[idx])):
                return True

            idx = (idx) + (1)

        return False

    def _getClass(self):
        return u"mdk_protocol.Discriminator"

    def _getField(self, name):
        if ((name) == (u"values")):
            return (self).values

        return None

    def _setField(self, name, value):
        if ((name) == (u"values")):
            (self).values = _cast(value, lambda: _List)


Discriminator.mdk_protocol_Discriminator_ref = None

def anyof(values):
    return Discriminator(values)

class Serializable(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def decodeClass(clazz, encoded):
        """
        The given class must have a construct() static method that takes the JSON-encoded type,
        or a constructor that takes no arguments.

        """
        json = _JSONObject.parse(encoded);
        type = ((json).getObjectItem(u"type")).getString();
        meth = (clazz).getMethod(u"construct");
        obj = None;
        if ((meth) != (None)):
            obj = _cast((meth).invoke(None, _List([type])), lambda: Serializable)
            if ((obj) == (None)):
                logger = quark._getLogger(u"protocol");
                (logger).warn((((((clazz).getName()) + (u".")) + ((meth).getName())) + (u" could not understand this json: ")) + (encoded));
                return _cast(None, lambda: Serializable)

            clazz = quark.reflect.Class.get(_getClass(obj))
        else:
            obj = _cast((clazz).construct(_List([])), lambda: Serializable)
            if ((obj) == (None)):
                raise Exception((((u"could not construct ") + ((clazz).getName())) + (u" from this json: ")) + (encoded));

        quark.fromJSON(clazz, obj, json);
        return obj

    @staticmethod
    def decodeClassName(name, encoded):
        return Serializable.decodeClass(quark.reflect.Class.get(name), encoded)

    def encode(self):
        clazz = quark.reflect.Class.get(_getClass(self));
        json = quark.toJSON(self, clazz);
        desc = _cast((self)._getField(u"_discriminator"), lambda: Discriminator);
        if ((desc) != (None)):
            (json).setObjectItem((u"type"), ((_JSONObject()).setString(((desc).values)[0])));

        encoded = (json).toString();
        return encoded

    def _getClass(self):
        return u"mdk_protocol.Serializable"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
Serializable.mdk_protocol_Serializable_ref = None
class LamportClock(Serializable):
    """
    A Lamport Clock is a logical structure meant to allow partial causal ordering. Ours is a list of
    integers such that adding an integer implies adding a new level to the causality tree.

    Within a level, time is indicated by incrementing the clock, so

    [1,2,3] comes before [1,2,4] which comes before [1,2,5]

    Adding an element to the clock implies causality, so [1,2,4,1-N] is _by definition_ a sequence that was
    _caused by_ the sequence of [1,2,1-3].

    Note that LamportClock is lowish-level support. SharedContext puts some more structure around this, too.

    """
    def _init(self):
        Serializable._init(self)
        self._mutex = _Lock()
        self.clocks = _List([])

    def __init__(self):
        super(LamportClock, self).__init__();

    @staticmethod
    def decode(encoded):
        return _cast(Serializable.decodeClassName(u"mdk_protocol.LamportClock", encoded), lambda: LamportClock)

    def key(self):
        """
        Return a neatly-formatted list of all of our clock elements (e.g. 1,2,4,1) for use as a name or
        a key.

        """
        (self._mutex).acquire();
        tmp = _List([]);
        i = 0;
        while ((i) < (len((self).clocks))):
            (tmp).append(_toString(((self).clocks)[i]));
            i = (i) + (1)

        str = (u",").join(tmp);
        (self._mutex).release();
        return str

    def toString(self):
        (self._mutex).acquire();
        str = ((u"<LamportClock ") + ((self).key())) + (u">");
        (self._mutex).release();
        return str

    def enter(self):
        """
        Enter a new level of causality. Returns the value to pass to later pass to leave to get back to the
        current level of causality.

        """
        (self._mutex).acquire();
        current = -(1);
        ((self).clocks).append(0);
        current = len((self).clocks)
        (self._mutex).release();
        return current

    def leave(self, popTo):
        """
        Leave deeper levels of causality. popTo should be the value returned when you enter()d this level.

        """
        (self._mutex).acquire();
        current = -(1);
        (self).clocks = (quark.ListUtil()).slice((self).clocks, 0, popTo)
        current = len((self).clocks)
        (self._mutex).release();
        return current

    def tick(self):
        """
        Increment the clock for our current level of causality (which is always the last element in the list).
        If there are no elements in our clock, do nothing.

        """
        (self._mutex).acquire();
        current = len((self).clocks);
        if ((current) > (0)):
            ((self).clocks)[(current) - (1)] = ((((self).clocks)[(current) - (1)]) + (1));

        (self._mutex).release();

    def _getClass(self):
        return u"mdk_protocol.LamportClock"

    def _getField(self, name):
        if ((name) == (u"_mutex")):
            return (self)._mutex

        if ((name) == (u"clocks")):
            return (self).clocks

        return None

    def _setField(self, name, value):
        if ((name) == (u"_mutex")):
            (self)._mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"clocks")):
            (self).clocks = _cast(value, lambda: _List)


LamportClock.quark_List_quark_int__ref = None
LamportClock.mdk_protocol_LamportClock_ref = None
class SharedContext(Serializable):
    def _init(self):
        Serializable._init(self)
        self.traceId = (quark.concurrent.Context.runtime()).uuid()
        self.clock = LamportClock()
        self.properties = {}
        self._lastEntry = 0

    def __init__(self):
        super(SharedContext, self).__init__();
        (self)._lastEntry = ((self).clock).enter()

    def withTraceId(self, traceId):
        """
        Set the traceId for this SharedContext.
        """
        (self).traceId = traceId
        return self

    @staticmethod
    def decode(encoded):
        return _cast(Serializable.decodeClassName(u"mdk_protocol.SharedContext", encoded), lambda: SharedContext)

    def clockStr(self, pfx):
        cs = u"";
        if (((self).clock) != (None)):
            cs = (pfx) + (((self).clock).key())

        return cs

    def key(self):
        return ((self).traceId) + ((self).clockStr(u":"))

    def toString(self):
        return (((u"<SCTX t:") + ((self).traceId)) + ((self).clockStr(u" c:"))) + (u">")

    def tick(self):
        """
        Tick the clock at our current causality level.

        """
        ((self).clock).tick();

    def start_span(self):
        """
        Return a SharedContext one level deeper in causality.

        NOTE WELL: THIS RETURNS A NEW SharedContext RATHER THAN MODIFYING THIS ONE. It is NOT SUPPORTED
        to modify the causality level of a SharedContext in place.

        """
        (self).tick();
        newContext = SharedContext.decode((self).encode());
        (newContext)._lastEntry = ((newContext).clock).enter()
        return newContext

    def finish_span(self):
        """
        Return a SharedContext one level higher in causality. In practice, most callers should probably stop
        using this context, and the new one, after calling this method.

        NOTE WELL: THIS RETURNS A NEW SharedContext RATHER THAN MODIFYING THIS ONE. It is NOT SUPPORTED
        to modify the causality level of a SharedContext in place.

        """
        newContext = SharedContext.decode((self).encode());
        (newContext)._lastEntry = ((newContext).clock).leave((newContext)._lastEntry)
        return newContext

    def copy(self):
        """
        Return a copy of a SharedContext.
        """
        return SharedContext.decode((self).encode())

    def _getClass(self):
        return u"mdk_protocol.SharedContext"

    def _getField(self, name):
        if ((name) == (u"traceId")):
            return (self).traceId

        if ((name) == (u"clock")):
            return (self).clock

        if ((name) == (u"properties")):
            return (self).properties

        if ((name) == (u"_lastEntry")):
            return (self)._lastEntry

        return None

    def _setField(self, name, value):
        if ((name) == (u"traceId")):
            (self).traceId = _cast(value, lambda: unicode)

        if ((name) == (u"clock")):
            (self).clock = _cast(value, lambda: LamportClock)

        if ((name) == (u"properties")):
            (self).properties = _cast(value, lambda: _Map)

        if ((name) == (u"_lastEntry")):
            (self)._lastEntry = _cast(value, lambda: int)


SharedContext.mdk_protocol_SharedContext_ref = None
class ProtocolHandler(object):

    def onOpen(self, open):
        raise NotImplementedError('`ProtocolHandler.onOpen` is an abstract method')

    def onClose(self, close):
        raise NotImplementedError('`ProtocolHandler.onClose` is an abstract method')

ProtocolHandler.mdk_protocol_ProtocolHandler_ref = None
class ProtocolEvent(Serializable):
    def _init(self):
        Serializable._init(self)

    def __init__(self):
        super(ProtocolEvent, self).__init__();

    @staticmethod
    def construct(type):
        if ((Open._discriminator).matches(type)):
            return Open()

        if ((Close._discriminator).matches(type)):
            return Close()

        return _cast(None, lambda: ProtocolEvent)

    def dispatch(self, handler):
        raise NotImplementedError('`ProtocolEvent.dispatch` is an abstract method')

    def _getClass(self):
        return u"mdk_protocol.ProtocolEvent"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
ProtocolEvent.mdk_protocol_ProtocolEvent_ref = None
class Open(ProtocolEvent):
    def _init(self):
        ProtocolEvent._init(self)
        self.version = u"2.0.0"
        self.properties = {}

    def __init__(self):
        super(Open, self).__init__();

    def dispatch(self, handler):
        (handler).onOpen(self);

    def _getClass(self):
        return u"mdk_protocol.Open"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Open._discriminator

        if ((name) == (u"version")):
            return (self).version

        if ((name) == (u"properties")):
            return (self).properties

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Open._discriminator = _cast(value, lambda: Discriminator)

        if ((name) == (u"version")):
            (self).version = _cast(value, lambda: unicode)

        if ((name) == (u"properties")):
            (self).properties = _cast(value, lambda: _Map)


Open._discriminator = anyof(_List([u"open", u"mdk.protocol.Open", u"discovery.protocol.Open"]))
Open.mdk_protocol_Open_ref = None
class ProtocolError(_QObject):
    """
    A value class for sending error informationto a remote peer.
    """
    def _init(self):
        self.code = None
        self.title = None
        self.detail = None
        self.id = None

    def __init__(self): self._init()

    def _getClass(self):
        return u"mdk_protocol.ProtocolError"

    def _getField(self, name):
        if ((name) == (u"code")):
            return (self).code

        if ((name) == (u"title")):
            return (self).title

        if ((name) == (u"detail")):
            return (self).detail

        if ((name) == (u"id")):
            return (self).id

        return None

    def _setField(self, name, value):
        if ((name) == (u"code")):
            (self).code = _cast(value, lambda: unicode)

        if ((name) == (u"title")):
            (self).title = _cast(value, lambda: unicode)

        if ((name) == (u"detail")):
            (self).detail = _cast(value, lambda: unicode)

        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)


ProtocolError.mdk_protocol_ProtocolError_ref = None
class Close(ProtocolEvent):
    """
    Close the event stream.
    """
    def _init(self):
        ProtocolEvent._init(self)
        self.error = None

    def __init__(self):
        super(Close, self).__init__();

    def dispatch(self, handler):
        (handler).onClose(self);

    def _getClass(self):
        return u"mdk_protocol.Close"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Close._discriminator

        if ((name) == (u"error")):
            return (self).error

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Close._discriminator = _cast(value, lambda: Discriminator)

        if ((name) == (u"error")):
            (self).error = _cast(value, lambda: ProtocolError)


Close._discriminator = anyof(_List([u"close", u"mdk.protocol.Close", u"discovery.protocol.Close"]))
Close.mdk_protocol_Close_ref = None
class WSClient(_QObject):
    """
    Common protocol machinery for web socket based protocol clients.
    """
    def _init(self):
        self.logger = quark._getLogger(u"protocol")
        self.firstDelay = 1.0
        self.maxDelay = 16.0
        self.reconnectDelay = self.firstDelay
        self.ttl = 30.0
        self.tick = 1.0
        self.sock = None
        self.sockUrl = None
        self.lastConnectAttempt = 0
        self.lastHeartbeat = 0
        self.timeService = None
        self.schedulingActor = None
        self.websockets = None
        self.dispatcher = None

    def __init__(self, runtime):
        self._init()
        (self).dispatcher = (runtime).dispatcher
        (self).timeService = (runtime).getTimeService()
        (self).schedulingActor = (runtime).getScheduleService()
        (self).websockets = (runtime).getWebSocketsService()

    def url(self):
        raise NotImplementedError('`WSClient.url` is an abstract method')

    def token(self):
        raise NotImplementedError('`WSClient.token` is an abstract method')

    def isStarted(self):
        raise NotImplementedError('`WSClient.isStarted` is an abstract method')

    def isConnected(self):
        return (self.sock) != (None)

    def schedule(self, time):
        ((self).dispatcher).tell(self, mdk_runtime.Schedule(u"wakeup", time), (self).schedulingActor);

    def scheduleReconnect(self):
        self.schedule(self.reconnectDelay);

    def onOpen(self, open):
        pass

    def doBackoff(self):
        self.reconnectDelay = (2.0) * (self.reconnectDelay)
        if ((self.reconnectDelay) > (self.maxDelay)):
            self.reconnectDelay = self.maxDelay

        (self.logger).info(((u"backing off, reconnecting in ") + (repr(self.reconnectDelay))) + (u" seconds"));

    def onClose(self, close):
        (self.logger).info((u"close: ") + (_toString(close)));
        if (((close).error) == (None)):
            self.reconnectDelay = self.firstDelay
        else:
            self.doBackoff();

    def onStart(self, dispatcher):
        self.schedule(0.0);

    def onStop(self):
        if (self.isConnected()):
            self.shutdown();
            ((self).dispatcher).tell(self, mdk_runtime.WSClose(), self.sock);
            self.sock = _cast(None, lambda: mdk_runtime.WSActor)

    def onMessage(self, origin, message):
        typeId = (quark.reflect.Class.get(_getClass(message))).id;
        if ((typeId) == (u"mdk_runtime.Happening")):
            (self).onScheduledEvent();
            return

        if ((typeId) == (u"mdk_runtime.WSClosed")):
            (self).onWSClosed();
            return

        if ((typeId) == (u"mdk_runtime.WSMessage")):
            wsmessage = _cast(message, lambda: mdk_runtime.WSMessage);
            (self).onWSMessage((wsmessage).body);
            return

    def onScheduledEvent(self):
        rightNow = int(round((((self).timeService).time()) * (1000.0)));
        heartbeatInterval = int(round((float(self.ttl) / float(2.0)) * (1000.0)));
        reconnectInterval = int(round((self.reconnectDelay) * (1000.0)));
        if (self.isConnected()):
            if (self.isStarted()):
                self.pump();
                if (((rightNow) - (self.lastHeartbeat)) >= (heartbeatInterval)):
                    self.doHeartbeat();

        else:
            if ((self.isStarted()) and (((rightNow) - (self.lastConnectAttempt)) >= (reconnectInterval))):
                self.doOpen();

        if (self.isStarted()):
            self.schedule(self.tick);

    def doOpen(self):
        self.open(self.url());
        self.lastConnectAttempt = int(round((((self).timeService).time()) * (1000.0)))

    def doHeartbeat(self):
        self.heartbeat();
        self.lastHeartbeat = int(round((((self).timeService).time()) * (1000.0)))

    def open(self, url):
        self.sockUrl = url
        tok = self.token();
        if ((tok) != (None)):
            url = ((url) + (u"?token=")) + (tok)

        (self.logger).info((u"opening ") + (self.sockUrl));
        (((self).websockets).connect(url, self)).andEither(quark._BoundMethod(self, u"onWSConnected", _List([])), quark._BoundMethod(self, u"onWSError", _List([])));

    def startup(self):
        pass

    def pump(self):
        pass

    def heartbeat(self):
        pass

    def shutdown(self):
        pass

    def onWSMessage(self, message):
        pass

    def onWSConnected(self, socket):
        (self.logger).info((((u"connected to ") + (self.sockUrl)) + (u" via ")) + (_toString(socket)));
        self.reconnectDelay = self.firstDelay
        self.sock = socket
        ((self).dispatcher).tell(self, (Open()).encode(), self.sock);
        self.startup();
        self.pump();

    def onWSError(self, error):
        (self.logger).error((u"onWSError in protocol! ") + ((error).toString()));
        self.doBackoff();

    def onWSClosed(self):
        (self.logger).info((u"closed ") + (self.sockUrl));
        self.sock = _cast(None, lambda: mdk_runtime.WSActor)

    def _getClass(self):
        return u"mdk_protocol.WSClient"

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


WSClient.mdk_protocol_WSClient_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_protocol")
