# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.behaviors")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark.error
import quark
import quark.concurrent


class RPCError(quark.error.Error):
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(RPCError, self).__init__(message);

    def _getClass(self):
        return u"quark.behaviors.RPCError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


RPCError.quark_behaviors_RPCError_ref = None
class RPC(_QObject):
    def _init(self):
        self.service = None
        self.returned = None
        self.timeout = None
        self.methodName = None
        self.instance = None

    def __init__(self, service, methodName):
        self._init()
        timeout = _cast((service)._getField(u"timeout"), lambda: float);
        if (((timeout) == (None)) or ((timeout) <= (0.0))):
            timeout = 10.0

        override = (service).getTimeout();
        if (((override) != (None)) and ((override) > (0.0))):
            timeout = override

        (self).returned = ((quark.reflect.Class.get(_getClass(service))).getMethod(methodName)).getType()
        (self).timeout = timeout
        (self).methodName = methodName
        (self).service = service

    def call(self, args):
        result = _cast(None, lambda: quark.concurrent.Future);
        (self).instance = ((self).service).getInstance()
        if (((self).instance) != (None)):
            request = _HTTPRequest(((self).instance).getURL());
            json = quark.toJSON(args, None);
            envelope = _JSONObject();
            (envelope).setObjectItem((u"$method"), ((_JSONObject()).setString((self).methodName)));
            (envelope).setObjectItem((u"$context"), ((_JSONObject()).setString(u"TBD")));
            (envelope).setObjectItem((u"rpc"), (json));
            body = (envelope).toString();
            (request).setBody(body);
            (request).setMethod(u"POST");
            rpc = RPCRequest(args, self);
            result = (rpc).call(request)
        else:
            result = _cast((self.returned).construct(_List([])), lambda: quark.concurrent.Future)
            (result).finish(RPCError(u"all services are down"));

        quark.concurrent.FutureWait.waitFor(result, 10.0);
        return result

    def succeed(self, info):
        ((self).instance).succeed(info);

    def fail(self, info):
        ((self).instance).fail(info);

    def toString(self):
        return ((((((u"RPC ") + (((self).service).getName())) + (u" at ")) + (((self).instance).getURL())) + (u": ")) + ((self).methodName)) + (u"(...)")

    def _getClass(self):
        return u"quark.behaviors.RPC"

    def _getField(self, name):
        if ((name) == (u"service")):
            return (self).service

        if ((name) == (u"returned")):
            return (self).returned

        if ((name) == (u"timeout")):
            return (self).timeout

        if ((name) == (u"methodName")):
            return (self).methodName

        if ((name) == (u"instance")):
            return (self).instance

        return None

    def _setField(self, name, value):
        if ((name) == (u"service")):
            (self).service = _cast(value, lambda: quark.Service)

        if ((name) == (u"returned")):
            (self).returned = _cast(value, lambda: quark.reflect.Class)

        if ((name) == (u"timeout")):
            (self).timeout = _cast(value, lambda: float)

        if ((name) == (u"methodName")):
            (self).methodName = _cast(value, lambda: unicode)

        if ((name) == (u"instance")):
            (self).instance = _cast(value, lambda: quark.ServiceInstance)


RPC.quark_behaviors_RPC_ref = None
class RPCRequest(_QObject):
    def _init(self):
        self.rpc = None
        self.retval = None
        self.args = None
        self.timeout = None

    def __init__(self, args, rpc):
        self._init()
        (self).retval = _cast(((rpc).returned).construct(_List([])), lambda: quark.concurrent.Future)
        (self).args = args
        (self).timeout = quark.concurrent.Timeout((rpc).timeout)
        (self).rpc = rpc

    def call(self, request):
        ((self).timeout).start(self);
        (quark.concurrent.Context.runtime()).request(request, self);
        return (self).retval

    def onHTTPResponse(self, rq, response):
        info = None;
        ((self).timeout).cancel();
        if (((response).getCode()) != (200)):
            info = ((((self).rpc).toString()) + (u" failed: Server returned error ")) + (_toString((response).getCode()))
            ((self).retval).finish(RPCError(info));
            ((self).rpc).fail(info);
            return

        body = (response).getBody();
        obj = _JSONObject.parse(body);
        classname = ((obj).getObjectItem(u"$class")).getString();
        if ((classname) == (None)):
            info = (((self).rpc).toString()) + (u" failed: Server returned unrecognizable content")
            ((self).retval).finish(RPCError(info));
            ((self).rpc).fail(info);
            return
        else:
            quark.fromJSON(((self).rpc).returned, (self).retval, obj);
            ((self).retval).finish(None);
            ((self).rpc).succeed(u"Success in the future...");

    def onTimeout(self, timeout):
        ((self).retval).finish(RPCError(u"request timed out"));
        ((self).rpc).fail(u"request timed out");

    def _getClass(self):
        return u"quark.behaviors.RPCRequest"

    def _getField(self, name):
        if ((name) == (u"rpc")):
            return (self).rpc

        if ((name) == (u"retval")):
            return (self).retval

        if ((name) == (u"args")):
            return (self).args

        if ((name) == (u"timeout")):
            return (self).timeout

        return None

    def _setField(self, name, value):
        if ((name) == (u"rpc")):
            (self).rpc = _cast(value, lambda: RPC)

        if ((name) == (u"retval")):
            (self).retval = _cast(value, lambda: quark.concurrent.Future)

        if ((name) == (u"args")):
            (self).args = _cast(value, lambda: _List)

        if ((name) == (u"timeout")):
            (self).timeout = _cast(value, lambda: quark.concurrent.Timeout)

    def onHTTPInit(self, request):
        pass

    def onHTTPError(self, request, message):
        pass

    def onHTTPFinal(self, request):
        pass
RPCRequest.quark_behaviors_RPCRequest_ref = None
class CircuitBreaker(_QObject):
    def _init(self):
        self.id = None
        self.failureLimit = None
        self.retestDelay = None
        self.active = True
        self.failureCount = 0
        self.mutex = _Lock()

    def __init__(self, id, failureLimit, retestDelay):
        self._init()
        (self).id = id
        (self).failureLimit = failureLimit
        (self).retestDelay = retestDelay

    def succeed(self):
        ((self).mutex).acquire();
        if (((self).failureCount) > (0)):
            (quark.Client.logger).info((u"- CLOSE breaker on ") + ((self).id));

        (self).failureCount = 0
        ((self).mutex).release();

    def fail(self):
        doSchedule = False;
        ((self).mutex).acquire();
        (self).failureCount = ((self).failureCount) + (1)
        if (((self).failureCount) >= ((self).failureLimit)):
            (self).active = False
            doSchedule = True
            (quark.Client.logger).warn((u"- OPEN breaker on ") + ((self).id));

        ((self).mutex).release();
        if (doSchedule):
            (quark.concurrent.Context.runtime()).schedule(self, (self).retestDelay);

    def onExecute(self, runtime):
        ((self).mutex).acquire();
        (self).active = True
        (quark.Client.logger).warn((u"- RETEST breaker on ") + ((self).id));
        ((self).mutex).release();

    def _getClass(self):
        return u"quark.behaviors.CircuitBreaker"

    def _getField(self, name):
        if ((name) == (u"id")):
            return (self).id

        if ((name) == (u"failureLimit")):
            return (self).failureLimit

        if ((name) == (u"retestDelay")):
            return (self).retestDelay

        if ((name) == (u"active")):
            return (self).active

        if ((name) == (u"failureCount")):
            return (self).failureCount

        if ((name) == (u"mutex")):
            return (self).mutex

        return None

    def _setField(self, name, value):
        if ((name) == (u"id")):
            (self).id = _cast(value, lambda: unicode)

        if ((name) == (u"failureLimit")):
            (self).failureLimit = _cast(value, lambda: int)

        if ((name) == (u"retestDelay")):
            (self).retestDelay = _cast(value, lambda: float)

        if ((name) == (u"active")):
            (self).active = _cast(value, lambda: bool)

        if ((name) == (u"failureCount")):
            (self).failureCount = _cast(value, lambda: int)

        if ((name) == (u"mutex")):
            (self).mutex = _cast(value, lambda: _Lock)


CircuitBreaker.quark_behaviors_CircuitBreaker_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.behaviors")
