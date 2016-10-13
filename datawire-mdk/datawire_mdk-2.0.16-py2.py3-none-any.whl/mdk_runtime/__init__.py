# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_runtime")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime.actors
import mdk_runtime.files
import mdk_runtime.promise
import quark.error
import quark.os
import quark
import quark.concurrent


class Dependencies(_QObject):
    """
    Trivial dependency injection setup.
    """
    def _init(self):
        self._services = {}

    def __init__(self): self._init()

    def registerService(self, name, service):
        """
        Register a service object.
        """
        if ((name) in ((self)._services)):
            raise Exception(((u"Can't register service '") + (name)) + (u"' twice."));

        ((self)._services)[name] = (service);

    def getService(self, name):
        """
        Look up a service by name.
        """
        if (not ((name) in ((self)._services))):
            raise Exception(((u"Service '") + (name)) + (u"' not found!"));

        return ((self)._services).get(name)

    def hasService(self, name):
        """
        Return whether the service exists.
        """
        return (name) in ((self)._services)

    def _getClass(self):
        return u"mdk_runtime.Dependencies"

    def _getField(self, name):
        if ((name) == (u"_services")):
            return (self)._services

        return None

    def _setField(self, name, value):
        if ((name) == (u"_services")):
            (self)._services = _cast(value, lambda: _Map)


Dependencies.mdk_runtime_Dependencies_ref = None
class MDKRuntime(_QObject):
    """
    Runtime environment for a particular MDK instance.

    Required registered services:
    - 'time': A provider of mdk_runtime.Time;
    - 'schedule': Implements the mdk_runtime.ScheduleActor actor protocol.
    - 'websockets': A provider of mdk_runtime.WebSockets.

    """
    def _init(self):
        self.dependencies = Dependencies()
        self.dispatcher = mdk_runtime.actors.MessageDispatcher()

    def __init__(self): self._init()

    def getTimeService(self):
        """
        Return Time service.
        """
        return _cast(((self).dependencies).getService(u"time"), lambda: Time)

    def getScheduleService(self):
        """
        Return Schedule service.
        """
        return _cast(((self).dependencies).getService(u"schedule"), lambda: mdk_runtime.actors.Actor)

    def getWebSocketsService(self):
        """
        Return WebSockets service.
        """
        return _cast(((self).dependencies).getService(u"websockets"), lambda: WebSockets)

    def getFileService(self):
        """
        Return File service.
        """
        return _cast(((self).dependencies).getService(u"files"), lambda: mdk_runtime.files.FileActor)

    def getEnvVarsService(self):
        """
        Return EnvironmentVariables service.
        """
        return _cast(((self).dependencies).getService(u"envvar"), lambda: EnvironmentVariables)

    def stop(self):
        """
        Stop all Actors that are started by default (i.e. files, schedule).
        """
        ((self).dispatcher).stopActor(self.getFileService());
        ((self).dispatcher).stopActor((self).getScheduleService());
        ((self).dispatcher).stopActor((self).getWebSocketsService());

    def _getClass(self):
        return u"mdk_runtime.MDKRuntime"

    def _getField(self, name):
        if ((name) == (u"dependencies")):
            return (self).dependencies

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        return None

    def _setField(self, name, value):
        if ((name) == (u"dependencies")):
            (self).dependencies = _cast(value, lambda: Dependencies)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)


MDKRuntime.mdk_runtime_MDKRuntime_ref = None
class Time(object):
    """
    Return current time.

    """

    def time(self):
        """
        Return the current time in seconds since the Unix epoch.

        """
        raise NotImplementedError('`Time.time` is an abstract method')

Time.mdk_runtime_Time_ref = None
class SchedulingActor(object):
    """
    An actor that can schedule events.

    Accepts Schedule messages and send Happening events to originator at the
    appropriate time.

    """
    pass
SchedulingActor.mdk_runtime_SchedulingActor_ref = None
class WebSockets(object):
    """
    Service that can open new WebSocket connections.

    When stopped it should close all connections.

    """

    def connect(self, url, originator):
        """
        The Promise resolves to a WSActor or WSConnectError. The originator will
        receive messages.

        """
        raise NotImplementedError('`WebSockets.connect` is an abstract method')

WebSockets.mdk_runtime_WebSockets_ref = None
class WSConnectError(quark.error.Error):
    """
    Connection failed.
    """
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(WSConnectError, self).__init__(message);

    def toString(self):
        return ((u"<WSConnectionError: ") + (super(WSConnectError, self).toString())) + (u">")

    def _getClass(self):
        return u"mdk_runtime.WSConnectError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


WSConnectError.mdk_runtime_WSConnectError_ref = None
class WSActor(object):
    """
    Actor representing a specific WebSocket connection.

    Accepts String and WSClose messages, sends WSMessage and WSClosed
    messages to the originator of the connection (Actor passed to
    WebSockets.connect()).

    """
    pass
WSActor.mdk_runtime_WSActor_ref = None
class WSMessage(_QObject):
    """
    A message was received from the server.
    """
    def _init(self):
        self.body = None

    def __init__(self, body):
        self._init()
        (self).body = body

    def _getClass(self):
        return u"mdk_runtime.WSMessage"

    def _getField(self, name):
        if ((name) == (u"body")):
            return (self).body

        return None

    def _setField(self, name, value):
        if ((name) == (u"body")):
            (self).body = _cast(value, lambda: unicode)


WSMessage.mdk_runtime_WSMessage_ref = None
class WSClose(_QObject):
    """
    Tell WSActor to close the connection.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def _getClass(self):
        return u"mdk_runtime.WSClose"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
WSClose.mdk_runtime_WSClose_ref = None
class WSClosed(_QObject):
    """
    Notify of WebSocket connection having closed.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def _getClass(self):
        return u"mdk_runtime.WSClosed"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
WSClosed.mdk_runtime_WSClosed_ref = None

def log_to_file(s):
    """
    On Python, log to a per-process file if MDK_LOG_MESSAGES env variable is set.
    """
    if (((quark.os.Environment.getEnvironment())._q__get__(u"MDK_LOG_MESSAGES")) != (None)):
        o = open("/tmp/mdk-messages-pid-%s.log" % __import__("os").getpid(), "a", 1).write(__import__("time").asctime() + ">   " + s + "\n\n");


class QuarkRuntimeWSActor(_QObject):
    """
    WSActor that uses current Quark runtime as temporary expedient.

    State can be 'ERROR', 'CONNECTING', 'CONNECTED', 'DISCONNECTING',
    'DISCONNECTED'.

    """
    def _init(self):
        self.logger = quark._getLogger(u"protocol")
        self.socket = None
        self.factory = None
        self.originator = None
        self.url = None
        self.shortURL = None
        self.dispatcher = None
        self.state = u"CONNECTING"

    def __init__(self, url, originator, factory):
        self._init()
        (self).url = url
        (self).originator = originator
        (self).factory = factory
        pieces = (url).split(u"?");
        (self).shortURL = (pieces)[0]
        if ((len(pieces)) > (1)):
            (self).shortURL = (((self).shortURL) + (u"?")) + (((pieces)[1])[(0):(8)])

    def logTS(self, message):
        if (True):
            return

        now = (quark.concurrent.Context.runtime()).now();
        tenths = (((now)) // (100)) % (100000);
        if ((tenths) < (0)):
            tenths = (tenths) + (100000)

        seconds = float(float(tenths)) / float(10.0);
        (self.logger).debug(((repr(seconds)) + (u" ")) + (message));

    def logPrologue(self, what):
        disMessage = u"";
        if (((self).dispatcher) == (None)):
            disMessage = u", no dispatcher"

        self.logTS(((((((((((what) + (u", current state ")) + ((self).state)) + (u", originator ")) + (_toString((self).originator))) + (u", I am ")) + (_toString(self))) + (u" [")) + ((self).shortURL)) + (u"]")) + (disMessage));

    def onStart(self, dispatcher):
        self.logPrologue(u"ws onStart");
        (self).dispatcher = dispatcher
        (quark.concurrent.Context.runtime()).open((self).url, self);

    def onMessage(self, origin, message):
        self.logPrologue(u"ws onMessage (actor message)");
        self.logTS((u"   message is from ") + (_toString(origin)));
        if ((((quark.reflect.Class.get(_getClass(message))).id) == (u"quark.String")) and (((self).state) == (u"CONNECTED"))):
            self.logTS((u"   send-ish, message is: ") + (_toString(message)));
            log_to_file((u"sending: ") + (_cast(message, lambda: unicode)));
            ((self).socket).send(_cast(message, lambda: unicode));
            return

        if ((((quark.reflect.Class.get(_getClass(message))).id) == (u"mdk_runtime.WSClose")) and (((self).state) == (u"CONNECTED"))):
            self.logTS(u"   close-ish, switching to DISCONNECTING state");
            (self).state = u"DISCONNECTING"
            ((self).socket).close();
            return

        (self.logger).warn((((u"ws onMessage got unhandled message: ") + ((quark.reflect.Class.get(_getClass(message))).id)) + (u" in state ")) + ((self).state));

    def onWSConnected(self, socket):
        self.logPrologue(u"onWSConnected");
        if (((self).state) == (u"ERROR")):
            self.logTS(u"Connection event after error event!");
            return

        (self).state = u"CONNECTED"
        (self).socket = socket
        ((self).factory).resolve(self);

    def onWSError(self, socket, error):
        self.logPrologue(u"onWSError");
        self.logTS((u"onWSError, reason is: ") + ((error).toString()));
        if (((self).state) == (u"CONNECTING")):
            (self.logger).error((u"Error connecting to WebSocket: ") + ((error).toString()));
            (self).state = u"ERROR"
            ((self).factory).reject(WSConnectError((error).toString()));
            return

        (self.logger).error((u"WebSocket error: ") + ((error).toString()));

    def onWSMessage(self, socket, message):
        self.logPrologue(u"onWSMessage");
        self.logTS((u"onWSMessage, message is: ") + (message));
        log_to_file((u"received: ") + (message));
        ((self).dispatcher).tell(self, WSMessage(message), (self).originator);

    def onWSFinal(self, socket):
        self.logPrologue(u"onWSFinal");
        if ((((self).state) == (u"DISCONNECTING")) or (((self).state) == (u"CONNECTED"))):
            (self).state = u"DISCONNECTED"
            (self).socket = _cast(None, lambda: quark.WebSocket)
            ((self).dispatcher).tell(self, WSClosed(), (self).originator);

    def _getClass(self):
        return u"mdk_runtime.QuarkRuntimeWSActor"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"socket")):
            return (self).socket

        if ((name) == (u"factory")):
            return (self).factory

        if ((name) == (u"originator")):
            return (self).originator

        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"shortURL")):
            return (self).shortURL

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"state")):
            return (self).state

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"socket")):
            (self).socket = _cast(value, lambda: quark.WebSocket)

        if ((name) == (u"factory")):
            (self).factory = _cast(value, lambda: mdk_runtime.promise.PromiseResolver)

        if ((name) == (u"originator")):
            (self).originator = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"shortURL")):
            (self).shortURL = _cast(value, lambda: unicode)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"state")):
            (self).state = _cast(value, lambda: unicode)

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass

    def onWSInit(self, socket):
        """
        Called when the WebSocket is first created.
        """
        pass

    def onWSBinary(self, socket, message):
        """
        Called when the WebSocket receives a binary message.
        """
        pass

    def onWSClosed(self, socket):
        """
        Called when the WebSocket disconnects cleanly.
        """
        pass
QuarkRuntimeWSActor.mdk_runtime_QuarkRuntimeWSActor_ref = None
class QuarkRuntimeWebSockets(_QObject):
    """
    WebSocket that uses current Quark runtime as temporary expedient.

    """
    def _init(self):
        self.logger = quark._getLogger(u"protocol")
        self.dispatcher = None
        self.connections = _List([])

    def __init__(self): self._init()

    def connect(self, url, originator):
        (self.logger).debug(((_toString(originator)) + (u"requested connection to ")) + (url));
        factory = mdk_runtime.promise.PromiseResolver((self).dispatcher);
        actor = QuarkRuntimeWSActor(url, originator, factory);
        (self.connections).append(actor);
        ((self).dispatcher).startActor(actor);
        return (factory).promise

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher

    def onMessage(self, origin, message):
        pass

    def onStop(self):
        idx = 0;
        while ((idx) < (len(self.connections))):
            ((self).dispatcher).tell(self, WSClose(), ((self).connections)[idx]);
            idx = (idx) + (1)

    def _getClass(self):
        return u"mdk_runtime.QuarkRuntimeWebSockets"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"connections")):
            return (self).connections

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"connections")):
            (self).connections = _cast(value, lambda: _List)


QuarkRuntimeWebSockets.quark_List_mdk_runtime_WSActor__ref = None
QuarkRuntimeWebSockets.mdk_runtime_QuarkRuntimeWebSockets_ref = None
class FakeWSActor(_QObject):
    """
    WSActor implementation for testing purposes.
    """
    def _init(self):
        self.url = None
        self.resolver = None
        self.resolved = False
        self.dispatcher = None
        self.originator = None
        self.sent = _List([])
        self.state = u"CONNECTING"
        self.expectIdx = 0

    def __init__(self, originator, resolver, url):
        self._init()
        (self).url = url
        (self).originator = originator
        (self).resolver = resolver

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher

    def onMessage(self, origin, message):
        if ((((quark.reflect.Class.get(_getClass(message))).id) == (u"quark.String")) and (((self).state) == (u"CONNECTED"))):
            ((self).sent).append(_cast(message, lambda: unicode));
            return

        if ((((quark.reflect.Class.get(_getClass(message))).id) == (u"mdk_runtime.WSClose")) and (((self).state) == (u"CONNECTED"))):
            (self).close();
            return

    def accept(self):
        """
        Simulate the remote peer accepting the socket connect.

        """
        if (self.resolved):
            (quark.concurrent.Context.runtime()).fail(u"Test bug. already accepted");
        else:
            self.resolved = True
            (self).state = u"CONNECTED"
            ((self).resolver).resolve(self);

    def reject(self):
        """
        Simulate the remote peer rejecting the socket connect.
        """
        if (self.resolved):
            (quark.concurrent.Context.runtime()).fail(u"Test bug. already accepted");
        else:
            self.resolved = True
            ((self).resolver).reject(WSConnectError(u"connection refused"));

    def send(self, message):
        """
        Simulate the remote peer sending a text message to the client.

        """
        if (((self).state) != (u"CONNECTED")):
            (quark.concurrent.Context.runtime()).fail(u"Test bug. Can't send when not connected.");

        ((self).dispatcher).tell(self, WSMessage(message), self.originator);

    def close(self):
        """
        Simulate the remote peer closing the socket.

        """
        if (((self).state) == (u"CONNECTED")):
            (self).state = u"DISCONNECTED"
            ((self).dispatcher).tell(self, WSClosed(), self.originator);
        else:
            (quark.concurrent.Context.runtime()).fail(u"Test bug. Can't close already closed socket.");

    def expectTextMessage(self):
        """
        Check that a message has been sent via this actor.

        """
        if (not (self.resolved)):
            (quark.concurrent.Context.runtime()).fail(u"not connected yet");
            return u"unreachable"

        if ((self.expectIdx) < (len((self).sent))):
            msg = ((self).sent)[self.expectIdx];
            self.expectIdx = (self.expectIdx) + (1)
            return msg

        (quark.concurrent.Context.runtime()).fail(u"no remaining message found");
        return u"unreachable"

    def _getClass(self):
        return u"mdk_runtime.FakeWSActor"

    def _getField(self, name):
        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"resolver")):
            return (self).resolver

        if ((name) == (u"resolved")):
            return (self).resolved

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"originator")):
            return (self).originator

        if ((name) == (u"sent")):
            return (self).sent

        if ((name) == (u"state")):
            return (self).state

        if ((name) == (u"expectIdx")):
            return (self).expectIdx

        return None

    def _setField(self, name, value):
        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"resolver")):
            (self).resolver = _cast(value, lambda: mdk_runtime.promise.PromiseResolver)

        if ((name) == (u"resolved")):
            (self).resolved = _cast(value, lambda: bool)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"originator")):
            (self).originator = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"sent")):
            (self).sent = _cast(value, lambda: _List)

        if ((name) == (u"state")):
            (self).state = _cast(value, lambda: unicode)

        if ((name) == (u"expectIdx")):
            (self).expectIdx = _cast(value, lambda: int)

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass
FakeWSActor.mdk_runtime_FakeWSActor_ref = None
class FakeWebSockets(_QObject):
    """
    WebSocket implementation for testing purposes.

    """
    def _init(self):
        self.dispatcher = None
        self.fakeActors = _List([])

    def __init__(self): self._init()

    def connect(self, url, originator):
        factory = mdk_runtime.promise.PromiseResolver((self).dispatcher);
        actor = FakeWSActor(originator, factory, url);
        ((self).dispatcher).startActor(actor);
        ((self).fakeActors).append(actor);
        return (factory).promise

    def lastConnection(self):
        return ((self).fakeActors)[(len((self).fakeActors)) - (1)]

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher

    def onMessage(self, origin, message):
        pass

    def _getClass(self):
        return u"mdk_runtime.FakeWebSockets"

    def _getField(self, name):
        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"fakeActors")):
            return (self).fakeActors

        return None

    def _setField(self, name, value):
        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"fakeActors")):
            (self).fakeActors = _cast(value, lambda: _List)

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass
FakeWebSockets.quark_List_mdk_runtime_FakeWSActor__ref = None
FakeWebSockets.mdk_runtime_FakeWebSockets_ref = None
class Schedule(_QObject):
    """
    Please send me a Happening message with given event name in given number of
    seconds.

    """
    def _init(self):
        self.event = None
        self.seconds = None

    def __init__(self, event, seconds):
        self._init()
        (self).event = event
        (self).seconds = seconds

    def _getClass(self):
        return u"mdk_runtime.Schedule"

    def _getField(self, name):
        if ((name) == (u"event")):
            return (self).event

        if ((name) == (u"seconds")):
            return (self).seconds

        return None

    def _setField(self, name, value):
        if ((name) == (u"event")):
            (self).event = _cast(value, lambda: unicode)

        if ((name) == (u"seconds")):
            (self).seconds = _cast(value, lambda: float)


Schedule.mdk_runtime_Schedule_ref = None
class Happening(_QObject):
    """
    A scheduled event is now happening.
    """
    def _init(self):
        self.event = None
        self.currentTime = None

    def __init__(self, event, currentTime):
        self._init()
        (self).event = event
        (self).currentTime = currentTime

    def _getClass(self):
        return u"mdk_runtime.Happening"

    def _getField(self, name):
        if ((name) == (u"event")):
            return (self).event

        if ((name) == (u"currentTime")):
            return (self).currentTime

        return None

    def _setField(self, name, value):
        if ((name) == (u"event")):
            (self).event = _cast(value, lambda: unicode)

        if ((name) == (u"currentTime")):
            (self).currentTime = _cast(value, lambda: float)


Happening.mdk_runtime_Happening_ref = None
class _ScheduleTask(_QObject):
    def _init(self):
        self.timeService = None
        self.requester = None
        self.event = None

    def __init__(self, timeService, requester, event):
        self._init()
        (self).timeService = timeService
        (self).requester = requester
        (self).event = event

    def onExecute(self, runtime):
        ((self.timeService).dispatcher).tell((self).timeService, Happening((self).event, ((self).timeService).time()), (self).requester);

    def _getClass(self):
        return u"mdk_runtime._ScheduleTask"

    def _getField(self, name):
        if ((name) == (u"timeService")):
            return (self).timeService

        if ((name) == (u"requester")):
            return (self).requester

        if ((name) == (u"event")):
            return (self).event

        return None

    def _setField(self, name, value):
        if ((name) == (u"timeService")):
            (self).timeService = _cast(value, lambda: QuarkRuntimeTime)

        if ((name) == (u"requester")):
            (self).requester = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"event")):
            (self).event = _cast(value, lambda: unicode)


_ScheduleTask.mdk_runtime__ScheduleTask_ref = None
class QuarkRuntimeTime(_QObject):
    """
    Temporary implementation based on Quark runtime, until we have native
    implementation.

    """
    def _init(self):
        self.dispatcher = None
        self.stopped = False

    def __init__(self): self._init()

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher

    def onStop(self):
        (self).stopped = True

    def onMessage(self, origin, msg):
        if ((self).stopped):
            return

        sched = _cast(msg, lambda: Schedule);
        seconds = (sched).seconds;
        if ((seconds) == (0.0)):
            seconds = 0.1

        (quark.concurrent.Context.runtime()).schedule(_ScheduleTask(self, origin, (sched).event), seconds);

    def time(self):
        milliseconds = float((quark.concurrent.Context.runtime()).now());
        return float(milliseconds) / float(1000.0)

    def _getClass(self):
        return u"mdk_runtime.QuarkRuntimeTime"

    def _getField(self, name):
        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"stopped")):
            return (self).stopped

        return None

    def _setField(self, name, value):
        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"stopped")):
            (self).stopped = _cast(value, lambda: bool)


QuarkRuntimeTime.mdk_runtime_QuarkRuntimeTime_ref = None
class _FakeTimeRequest(_QObject):
    def _init(self):
        self.requester = None
        self.event = None
        self.happensAt = None

    def __init__(self, requester, event, happensAt):
        self._init()
        (self).requester = requester
        (self).event = event
        (self).happensAt = happensAt

    def _getClass(self):
        return u"mdk_runtime._FakeTimeRequest"

    def _getField(self, name):
        if ((name) == (u"requester")):
            return (self).requester

        if ((name) == (u"event")):
            return (self).event

        if ((name) == (u"happensAt")):
            return (self).happensAt

        return None

    def _setField(self, name, value):
        if ((name) == (u"requester")):
            (self).requester = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"event")):
            (self).event = _cast(value, lambda: unicode)

        if ((name) == (u"happensAt")):
            (self).happensAt = _cast(value, lambda: float)


_FakeTimeRequest.mdk_runtime__FakeTimeRequest_ref = None
class FakeTime(_QObject):
    """
    Testing fake.
    """
    def _init(self):
        self._now = 1000.0
        self._scheduled = {}
        self.dispatcher = None

    def __init__(self): self._init()

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher

    def onMessage(self, origin, msg):
        sched = _cast(msg, lambda: Schedule);
        (self._scheduled)[(len(_List(list((self._scheduled).keys()))))] = (_FakeTimeRequest(origin, (sched).event, ((self)._now) + ((sched).seconds)));

    def time(self):
        return (self)._now

    def pump(self):
        """
        Run scheduled events whose time has come.
        """
        idx = 0;
        keys = _List(list(((self)._scheduled).keys()));
        while ((idx) < (len(keys))):
            request = (self._scheduled).get((keys)[idx]);
            if (((request).happensAt) <= ((self)._now)):
                _map_remove(((self)._scheduled), ((keys)[idx]));
                ((self).dispatcher).tell(self, Happening((request).event, self.time()), (request).requester);

            idx = (idx) + (1)

    def advance(self, seconds):
        """
        Move time forward.
        """
        (self)._now = ((self)._now) + (seconds)

    def scheduled(self):
        """
        Number of scheduled events.
        """
        return len(_List(list(((self)._scheduled).keys())))

    def _getClass(self):
        return u"mdk_runtime.FakeTime"

    def _getField(self, name):
        if ((name) == (u"_now")):
            return (self)._now

        if ((name) == (u"_scheduled")):
            return (self)._scheduled

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        return None

    def _setField(self, name, value):
        if ((name) == (u"_now")):
            (self)._now = _cast(value, lambda: float)

        if ((name) == (u"_scheduled")):
            (self)._scheduled = _cast(value, lambda: _Map)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass
FakeTime.quark_List_quark_long__ref = None
FakeTime.quark_Map_quark_long_mdk_runtime__FakeTimeRequest__ref = None
FakeTime.mdk_runtime_FakeTime_ref = None
class EnvironmentVariable(_QObject):
    """
    EnvironmentVariable is a Supplier of Strings that come from the environment.
    """
    def _init(self):
        self.variableName = None
        self._value = None

    def __init__(self, variableName, value):
        self._init()
        (self).variableName = variableName
        (self)._value = value

    def isDefined(self):
        return (self.get()) != (None)

    def get(self):
        return (self)._value

    def orElseGet(self, alternative):
        result = self.get();
        if ((result) != (None)):
            return result
        else:
            return alternative

    def _getClass(self):
        return u"mdk_runtime.EnvironmentVariable"

    def _getField(self, name):
        if ((name) == (u"variableName")):
            return (self).variableName

        if ((name) == (u"_value")):
            return (self)._value

        return None

    def _setField(self, name, value):
        if ((name) == (u"variableName")):
            (self).variableName = _cast(value, lambda: unicode)

        if ((name) == (u"_value")):
            (self)._value = _cast(value, lambda: unicode)


EnvironmentVariable.mdk_runtime_EnvironmentVariable_ref = None
class EnvironmentVariables(object):
    """
    Inspect process environment variables.
    """

    def var(self, name):
        """
        Return an EnvironmentVariable instance for the given var.
        """
        raise NotImplementedError('`EnvironmentVariables.var` is an abstract method')

EnvironmentVariables.mdk_runtime_EnvironmentVariables_ref = None
class RealEnvVars(_QObject):
    """
    Use real environment variables.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def var(self, name):
        return EnvironmentVariable(name, (quark.os.Environment.getEnvironment())._q__get__(name))

    def _getClass(self):
        return u"mdk_runtime.RealEnvVars"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
RealEnvVars.mdk_runtime_RealEnvVars_ref = None
class FakeEnvVars(_QObject):
    """
    Testing fake for EnvironmentVariables.
    """
    def _init(self):
        self.env = {}

    def __init__(self): self._init()

    def set(self, name, value):
        ((self).env)[name] = (value);

    def var(self, name):
        value = _cast(None, lambda: unicode);
        if ((name) in ((self).env)):
            value = ((self).env).get(name)

        return EnvironmentVariable(name, value)

    def _getClass(self):
        return u"mdk_runtime.FakeEnvVars"

    def _getField(self, name):
        if ((name) == (u"env")):
            return (self).env

        return None

    def _setField(self, name, value):
        if ((name) == (u"env")):
            (self).env = _cast(value, lambda: _Map)


FakeEnvVars.mdk_runtime_FakeEnvVars_ref = None

def defaultRuntime():
    """
    Create a MDKRuntime with the default configuration and start its actors.
    """
    runtime = MDKRuntime();
    ((runtime).dependencies).registerService(u"envvar", RealEnvVars());
    timeService = QuarkRuntimeTime();
    websockets = QuarkRuntimeWebSockets();
    ((runtime).dependencies).registerService(u"time", timeService);
    ((runtime).dependencies).registerService(u"schedule", timeService);
    ((runtime).dependencies).registerService(u"websockets", websockets);
    fileActor = mdk_runtime.files.FileActorImpl(runtime);
    ((runtime).dependencies).registerService(u"files", fileActor);
    ((runtime).dispatcher).startActor(timeService);
    ((runtime).dispatcher).startActor(websockets);
    ((runtime).dispatcher).startActor(fileActor);
    return runtime


def fakeRuntime():
    runtime = MDKRuntime();
    ((runtime).dependencies).registerService(u"envvar", FakeEnvVars());
    timeService = FakeTime();
    websockets = FakeWebSockets();
    ((runtime).dependencies).registerService(u"time", timeService);
    ((runtime).dependencies).registerService(u"schedule", timeService);
    ((runtime).dependencies).registerService(u"websockets", websockets);
    fileActor = mdk_runtime.files.FileActorImpl(runtime);
    ((runtime).dependencies).registerService(u"files", fileActor);
    ((runtime).dispatcher).startActor(timeService);
    ((runtime).dispatcher).startActor(websockets);
    ((runtime).dispatcher).startActor(fileActor);
    return runtime





def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_runtime")
