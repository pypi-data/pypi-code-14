# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.mock")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent
import quark.test


class MockEvent(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def getType(self):
        raise NotImplementedError('`MockEvent.getType` is an abstract method')

    def getArgs(self):
        raise NotImplementedError('`MockEvent.getArgs` is an abstract method')

    def toString(self):
        return (self.getType()) + (_toString(self.getArgs()))

    def _getClass(self):
        return u"quark.mock.MockEvent"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
MockEvent.quark_mock_MockEvent_ref = None
class SocketEvent(MockEvent):
    def _init(self):
        MockEvent._init(self)
        self.url = None
        self.handler = None
        self.sock = None
        self.expectIdx = 0

    def __init__(self, url, handler):
        super(SocketEvent, self).__init__();
        (self).url = url
        (self).handler = handler

    def getType(self):
        return u"socket"

    def getArgs(self):
        return _List([self.url, self.handler])

    def accept(self):
        if ((self.sock) != (None)):
            (quark.concurrent.Context.runtime()).fail(u"already accepted");
        else:
            self.sock = MockSocket(self.handler)

    def send(self, message):
        (self.handler).onWSMessage(self.sock, message);

    def close(self):
        ((self).sock).close();

    def expectMessage(self):
        if ((self.sock) == (None)):
            (quark.concurrent.Context.runtime()).fail(u"not accepted");

        if (quark.test.check((self.expectIdx) < (len((self.sock).messages)), u"expected a message")):
            msg = ((self.sock).messages)[self.expectIdx];
            self.expectIdx = (self.expectIdx) + (1)
            return msg

        return _cast(None, lambda: MockMessage)

    def expectTextMessage(self):
        msg = self.expectMessage();
        if (((msg) != (None)) and ((msg).isText())):
            return _cast(msg, lambda: TextMessage)
        else:
            return _cast(None, lambda: TextMessage)

    def expectBinaryMessage(self):
        msg = self.expectMessage();
        if (((msg) != (None)) and ((msg).isBinary())):
            return _cast(msg, lambda: BinaryMessage)
        else:
            return _cast(None, lambda: BinaryMessage)

    def _getClass(self):
        return u"quark.mock.SocketEvent"

    def _getField(self, name):
        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"handler")):
            return (self).handler

        if ((name) == (u"sock")):
            return (self).sock

        if ((name) == (u"expectIdx")):
            return (self).expectIdx

        return None

    def _setField(self, name, value):
        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"handler")):
            (self).handler = _cast(value, lambda: quark.WSHandler)

        if ((name) == (u"sock")):
            (self).sock = _cast(value, lambda: MockSocket)

        if ((name) == (u"expectIdx")):
            (self).expectIdx = _cast(value, lambda: int)


SocketEvent.quark_mock_SocketEvent_ref = None
class MockMessage(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def isBinary(self):
        return not (self.isText())

    def isText(self):
        raise NotImplementedError('`MockMessage.isText` is an abstract method')

    def _getClass(self):
        return u"quark.mock.MockMessage"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
MockMessage.quark_mock_MockMessage_ref = None
class TextMessage(MockMessage):
    """
    A text message.
    """
    def _init(self):
        MockMessage._init(self)
        self.text = None

    def __init__(self, message):
        super(TextMessage, self).__init__();
        self.text = message

    def isText(self):
        return True

    def _getClass(self):
        return u"quark.mock.TextMessage"

    def _getField(self, name):
        if ((name) == (u"text")):
            return (self).text

        return None

    def _setField(self, name, value):
        if ((name) == (u"text")):
            (self).text = _cast(value, lambda: unicode)


TextMessage.quark_mock_TextMessage_ref = None
class BinaryMessage(MockMessage):
    """
    A binary message.
    """
    def _init(self):
        MockMessage._init(self)
        self.bytes = None

    def __init__(self, message):
        super(BinaryMessage, self).__init__();
        self.bytes = message

    def isText(self):
        return False

    def _getClass(self):
        return u"quark.mock.BinaryMessage"

    def _getField(self, name):
        if ((name) == (u"bytes")):
            return (self).bytes

        return None

    def _setField(self, name, value):
        if ((name) == (u"bytes")):
            (self).bytes = value


BinaryMessage.quark_mock_BinaryMessage_ref = None
class MockSocket(_QObject):
    def _init(self):
        self.messages = _List([])
        self.closed = False
        self.handler = None

    def __init__(self, handler):
        self._init()
        (self).handler = handler
        (self).closed = False
        (self).messages = _List([])
        (handler).onWSInit(self);
        (handler).onWSConnected(self);

    def send(self, message):
        (self.messages).append(TextMessage(message));
        return True

    def sendBinary(self, bytes):
        (self.messages).append(BinaryMessage(bytes));
        return True

    def close(self):
        if (self.closed):
            (quark.concurrent.Context.runtime()).fail(u"already closed");
        else:
            (self.handler).onWSClosed(self);
            (self.handler).onWSFinal(self);
            self.closed = True

        return True

    def _getClass(self):
        return u"quark.mock.MockSocket"

    def _getField(self, name):
        if ((name) == (u"messages")):
            return (self).messages

        if ((name) == (u"closed")):
            return (self).closed

        if ((name) == (u"handler")):
            return (self).handler

        return None

    def _setField(self, name, value):
        if ((name) == (u"messages")):
            (self).messages = _cast(value, lambda: _List)

        if ((name) == (u"closed")):
            (self).closed = _cast(value, lambda: bool)

        if ((name) == (u"handler")):
            (self).handler = _cast(value, lambda: quark.WSHandler)


MockSocket.quark_List_quark_mock_MockMessage__ref = None
MockSocket.quark_mock_MockSocket_ref = None
class RequestEvent(MockEvent):
    def _init(self):
        MockEvent._init(self)
        self.request = None
        self.handler = None

    def __init__(self, request, handler):
        super(RequestEvent, self).__init__();
        (self).request = request
        (self).handler = handler

    def getType(self):
        return u"request"

    def getArgs(self):
        return _List([self.request, self.handler])

    def respond(self, code, headers, body):
        response = MockResponse();
        (response).code = code
        (response).headers = headers
        (response).body = body
        (self.handler).onHTTPInit(self.request);
        (self.handler).onHTTPResponse(self.request, response);
        (self.handler).onHTTPFinal(self.request);

    def fail(self, error):
        (self.handler).onHTTPInit(self.request);
        (self.handler).onHTTPError(self.request, error);
        (self.handler).onHTTPFinal(self.request);

    def _getClass(self):
        return u"quark.mock.RequestEvent"

    def _getField(self, name):
        if ((name) == (u"request")):
            return (self).request

        if ((name) == (u"handler")):
            return (self).handler

        return None

    def _setField(self, name, value):
        if ((name) == (u"request")):
            (self).request = _cast(value, lambda: quark.HTTPRequest)

        if ((name) == (u"handler")):
            (self).handler = _cast(value, lambda: quark.HTTPHandler)


RequestEvent.quark_mock_RequestEvent_ref = None
class MockResponse(_QObject):
    def _init(self):
        self.code = None
        self.body = None
        self.headers = {}

    def __init__(self): self._init()

    def getCode(self):
        return self.code

    def setCode(self, code):
        (self).code = code

    def getBody(self):
        return self.body

    def setBody(self, body):
        (self).body = body

    def setHeader(self, key, value):
        (self.headers)[key] = (value);

    def getHeader(self, key):
        return (self.headers).get(key)

    def getHeaders(self):
        return _List(list((self.headers).keys()))

    def _getClass(self):
        return u"quark.mock.MockResponse"

    def _getField(self, name):
        if ((name) == (u"code")):
            return (self).code

        if ((name) == (u"body")):
            return (self).body

        if ((name) == (u"headers")):
            return (self).headers

        return None

    def _setField(self, name, value):
        if ((name) == (u"code")):
            (self).code = _cast(value, lambda: int)

        if ((name) == (u"body")):
            (self).body = _cast(value, lambda: unicode)

        if ((name) == (u"headers")):
            (self).headers = _cast(value, lambda: _Map)


MockResponse.quark_mock_MockResponse_ref = None
class MockTask(_QObject):
    def _init(self):
        self.task = None
        self.delay = None
        self._scheduledFor = None

    def __init__(self, task, delay):
        self._init()
        (self).task = task
        (self).delay = delay

    def _getClass(self):
        return u"quark.mock.MockTask"

    def _getField(self, name):
        if ((name) == (u"task")):
            return (self).task

        if ((name) == (u"delay")):
            return (self).delay

        if ((name) == (u"_scheduledFor")):
            return (self)._scheduledFor

        return None

    def _setField(self, name, value):
        if ((name) == (u"task")):
            (self).task = _cast(value, lambda: quark.Task)

        if ((name) == (u"delay")):
            (self).delay = _cast(value, lambda: float)

        if ((name) == (u"_scheduledFor")):
            (self)._scheduledFor = _cast(value, lambda: int)


MockTask.quark_mock_MockTask_ref = None
class MockRuntime(_QObject):
    def _init(self):
        self.runtime = None
        self.events = _List([])
        self.tasks = _List([])
        self._executed_tasks = _List([])
        self.executed = 0
        self._currentTime = 1000000

    def __init__(self, runtime):
        self._init()
        (self).runtime = runtime

    def pump(self):
        """
        Execute all currently scheduled tasks.
        """
        size = len(self.tasks);
        idx = 0;
        while ((idx) < (size)):
            if ((self._executed_tasks)[idx]):
                idx = (idx) + (1)
                continue;

            wrapper = (self.tasks)[idx];
            next = ((self.tasks)[idx]).task;
            if (((wrapper)._scheduledFor) <= ((self).now())):
                (self._executed_tasks)[idx] = (True);
                (next).onExecute(self);
                self.executed = (self.executed) + (1)

            idx = (idx) + (1)

    def open(self, url, handler):
        (self.events).append(SocketEvent(url, handler));

    def request(self, request, handler):
        (self.events).append(RequestEvent(request, handler));

    def schedule(self, handler, delayInSeconds):
        task = MockTask(handler, delayInSeconds);
        (task)._scheduledFor = ((self).now()) + (int(round((1000.0) * (delayInSeconds))))
        (self.tasks).append(task);
        (self._executed_tasks).append(False);

    def codec(self):
        return (self.runtime).codec()

    def now(self):
        return self._currentTime

    def advanceClock(self, ms):
        self._currentTime = (self._currentTime) + (ms)

    def sleep(self, seconds):
        (self.runtime).sleep(seconds);

    def uuid(self):
        return (self.runtime).uuid()

    def serveHTTP(self, url, servlet):
        (self.runtime).fail(u"Runtime.serveHTTP not yet supported by the MockRuntime");

    def serveWS(self, url, servlet):
        (self.runtime).fail(u"Runtime.serveWS not yet supported by the MockRuntime");

    def respond(self, request, response):
        (self.runtime).fail(u"Runtime.respond not yet supported by the MockRuntime");

    def fail(self, message):
        (self.runtime).fail(message);

    def logger(self, topic):
        return (self.runtime).logger(topic)

    def callSafely(self, callee, defaultResult):
        return (callee)(None) if callable(callee) else (callee).call(None)

    def _getClass(self):
        return u"quark.mock.MockRuntime"

    def _getField(self, name):
        if ((name) == (u"runtime")):
            return (self).runtime

        if ((name) == (u"events")):
            return (self).events

        if ((name) == (u"tasks")):
            return (self).tasks

        if ((name) == (u"_executed_tasks")):
            return (self)._executed_tasks

        if ((name) == (u"executed")):
            return (self).executed

        if ((name) == (u"_currentTime")):
            return (self)._currentTime

        return None

    def _setField(self, name, value):
        if ((name) == (u"runtime")):
            (self).runtime = _cast(value, lambda: quark.Runtime)

        if ((name) == (u"events")):
            (self).events = _cast(value, lambda: _List)

        if ((name) == (u"tasks")):
            (self).tasks = _cast(value, lambda: _List)

        if ((name) == (u"_executed_tasks")):
            (self)._executed_tasks = _cast(value, lambda: _List)

        if ((name) == (u"executed")):
            (self).executed = _cast(value, lambda: int)

        if ((name) == (u"_currentTime")):
            (self)._currentTime = _cast(value, lambda: int)


MockRuntime.quark_List_quark_mock_MockEvent__ref = None
MockRuntime.quark_List_quark_mock_MockTask__ref = None
MockRuntime.quark_List_quark_bool__ref = None
MockRuntime.quark_mock_MockRuntime_ref = None
class MockRuntimeTest(_QObject):
    def _init(self):
        self.mock = None
        self.old = None
        self.expectIdx = 0
        self.sockets = None

    def __init__(self): self._init()

    def setup(self):
        self.old = quark.concurrent.Context.current()
        ctx = quark.concurrent.Context(quark.concurrent.Context.current());
        self.mock = MockRuntime((ctx)._runtime)
        (ctx)._runtime = self.mock
        quark.concurrent.Context.swap(ctx);
        self.expectIdx = 0
        self.sockets = {}

    def teardown(self):
        quark.concurrent.Context.swap(self.old);

    def pump(self):
        """
        Execute any pending asynchronous tasks.
        """
        (self.mock).pump();

    def expectNone(self):
        delta = (len((self.mock).events)) - (self.expectIdx);
        quark.test.check((delta) == (0), (u"expected no events, got ") + (_toString(delta)));
        return delta

    def expectEvent(self, expectedType):
        result = _cast(None, lambda: MockEvent);
        if (quark.test.check((len((self.mock).events)) > (self.expectIdx), ((u"expected ") + (expectedType)) + (u" event, got no events"))):
            type = (((self.mock).events)[self.expectIdx]).getType();
            if (quark.test.check((type) == (expectedType), (((u"expected ") + (expectedType)) + (u" event, got ")) + (type))):
                result = ((self.mock).events)[self.expectIdx]

        self.expectIdx = (self.expectIdx) + (1)
        return result

    def expectRequest(self, expectedUrl):
        rev = _cast(self.expectEvent(u"request"), lambda: RequestEvent);
        if ((rev) != (None)):
            if ((expectedUrl) == (None)):
                return rev

            url = ((rev).request).getUrl();
            if (quark.test.check((url) == (expectedUrl), ((((u"expected request event to url(") + (expectedUrl)) + (u"), got url(")) + (url)) + (u")"))):
                return rev

        return _cast(None, lambda: RequestEvent)

    def expectSocket(self, expectedUrl):
        sev = _cast(self.expectEvent(u"socket"), lambda: SocketEvent);
        if ((sev) != (None)):
            (self.sockets)[(sev).url] = (sev);
            if ((expectedUrl) == (None)):
                return sev

            url = (sev).url;
            if (quark.test.check((url) == (expectedUrl), ((((u"expected socket event to url(") + (expectedUrl)) + (u"), got url(")) + (url)) + (u")"))):
                return sev

        return _cast(None, lambda: SocketEvent)

    def _getClass(self):
        return u"quark.mock.MockRuntimeTest"

    def _getField(self, name):
        if ((name) == (u"mock")):
            return (self).mock

        if ((name) == (u"old")):
            return (self).old

        if ((name) == (u"expectIdx")):
            return (self).expectIdx

        if ((name) == (u"sockets")):
            return (self).sockets

        return None

    def _setField(self, name, value):
        if ((name) == (u"mock")):
            (self).mock = _cast(value, lambda: MockRuntime)

        if ((name) == (u"old")):
            (self).old = _cast(value, lambda: quark.concurrent.Context)

        if ((name) == (u"expectIdx")):
            (self).expectIdx = _cast(value, lambda: int)

        if ((name) == (u"sockets")):
            (self).sockets = _cast(value, lambda: _Map)


MockRuntimeTest.quark_Map_quark_String_quark_mock_SocketEvent__ref = None
MockRuntimeTest.quark_mock_MockRuntimeTest_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.mock")
