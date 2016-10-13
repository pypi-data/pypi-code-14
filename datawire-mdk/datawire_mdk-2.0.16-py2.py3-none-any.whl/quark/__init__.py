# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark.concurrent
import quark.error
import quark.logging
import quark.behaviors
import quark.test
import quark.spi
import quark.spi_api
import quark.spi_api_tracing
import quark.os
import quark.mock


class Task(object):

    def onExecute(self, runtime):
        raise NotImplementedError('`Task.onExecute` is an abstract method')

Task.quark_Task_ref = None
class Runtime(object):

    def open(self, url, handler):
        raise NotImplementedError('`Runtime.open` is an abstract method')

    def request(self, request, handler):
        raise NotImplementedError('`Runtime.request` is an abstract method')

    def schedule(self, handler, delayInSeconds):
        raise NotImplementedError('`Runtime.schedule` is an abstract method')

    def codec(self):
        raise NotImplementedError('`Runtime.codec` is an abstract method')

    def serveHTTP(self, url, servlet):
        raise NotImplementedError('`Runtime.serveHTTP` is an abstract method')

    def serveWS(self, url, servlet):
        raise NotImplementedError('`Runtime.serveWS` is an abstract method')

    def respond(self, request, response):
        raise NotImplementedError('`Runtime.respond` is an abstract method')

    def fail(self, message):
        """
        Display the explanatory message and then terminate the program
        """
        raise NotImplementedError('`Runtime.fail` is an abstract method')

    def logger(self, topic):
        """
        Get a logger for the specified topic.
        """
        raise NotImplementedError('`Runtime.logger` is an abstract method')

    def now(self):
        """
        Get epoch time in milliseconds
        """
        raise NotImplementedError('`Runtime.now` is an abstract method')

    def sleep(self, seconds):
        """
        Suspend execution of this thread for some number of seconds
        """
        raise NotImplementedError('`Runtime.sleep` is an abstract method')

    def uuid(self):
        """
        Get a v4 random UUID (Universally Unique IDentifier)
        """
        raise NotImplementedError('`Runtime.uuid` is an abstract method')

    def callSafely(self, callable, defaultResult):
        """
        Call a UnaryCallable safely, catching native exceptions.

        The UnaryCallable is called with null.

        The result of calling the UnaryCallable will be returned, unless an
        exception is caught in which case the default is returned.

        """
        raise NotImplementedError('`Runtime.callSafely` is an abstract method')

Runtime.quark_Runtime_ref = None

def now():
    """
    Get epoch time in milliseconds
    """
    return (quark.concurrent.Context.runtime()).now()


def sleep(seconds):
    """
    Suspend execution of this thread for some number of seconds
    """
    (quark.concurrent.Context.runtime()).sleep(seconds);


def uuid():
    """
    Get a v4 random UUID (Universally Unique IDentifier)
    """
    return (quark.concurrent.Context.runtime()).uuid()


class Maybe(object):

    def getValue(self):
        raise NotImplementedError('`Maybe.getValue` is an abstract method')

    def hasValue(self):
        raise NotImplementedError('`Maybe.hasValue` is an abstract method')

Maybe.quark_Maybe_quark_Object__ref = None
class ParsedNumber(_QObject):
    def _init(self):
        self._value = None
        self._hasValue = False

    def __init__(self): self._init()

    def getValue(self):
        return (self)._value

    def hasValue(self):
        return (self)._hasValue

    def _parseLong(self, num):
        i = 0;
        val = (0);
        neg = False;
        if ((i) == (len(num))):
            return (0)

        first = ord(unicode(num)[0]);
        if (((first) == (ParsedNumber.MINUS)) or ((first) == (ParsedNumber.PLUS))):
            neg = (first) == (ParsedNumber.MINUS)
            i = (i) + (1)

        if ((i) == (len(num))):
            return (0)

        while ((i) < (len(num))):
            d = ord(unicode(num)[i]);
            if (((d) < (ParsedNumber.ZERO)) or ((d) > (ParsedNumber.NINE))):
                break;
            else:
                val = ((10) * (val)) + (((d) - (ParsedNumber.ZERO)))

            i = (i) + (1)

        (self)._hasValue = (i) == (len(num))
        if (neg):
            return -(val)
        else:
            return val

    def _getClass(self):
        return u"quark.ParsedNumber<quark.Object>"

    def _getField(self, name):
        if ((name) == (u"MINUS")):
            return ParsedNumber.MINUS

        if ((name) == (u"PLUS")):
            return ParsedNumber.PLUS

        if ((name) == (u"ZERO")):
            return ParsedNumber.ZERO

        if ((name) == (u"NINE")):
            return ParsedNumber.NINE

        if ((name) == (u"_value")):
            return (self)._value

        if ((name) == (u"_hasValue")):
            return (self)._hasValue

        return None

    def _setField(self, name, value):
        if ((name) == (u"MINUS")):
            ParsedNumber.MINUS = _cast(value, lambda: int)

        if ((name) == (u"PLUS")):
            ParsedNumber.PLUS = _cast(value, lambda: int)

        if ((name) == (u"ZERO")):
            ParsedNumber.ZERO = _cast(value, lambda: int)

        if ((name) == (u"NINE")):
            ParsedNumber.NINE = _cast(value, lambda: int)

        if ((name) == (u"_value")):
            (self)._value = _cast(value, lambda: T)

        if ((name) == (u"_hasValue")):
            (self)._hasValue = _cast(value, lambda: bool)


ParsedNumber.MINUS = ord(unicode(u"-")[0])
ParsedNumber.PLUS = ord(unicode(u"+")[0])
ParsedNumber.ZERO = ord(unicode(u"0")[0])
ParsedNumber.NINE = ord(unicode(u"9")[0])
class ParsedInt(ParsedNumber):
    def _init(self):
        ParsedNumber._init(self)
        self.MIN = (-(2147483647)) - (1)
        self.MAX = 2147483647

    def __init__(self, num):
        super(ParsedInt, self).__init__();
        temp = (self)._parseLong(num);
        if (((temp) < (((self).MIN))) or ((temp) > (((self).MAX)))):
            (self)._hasValue = False
            if ((temp) < ((0))):
                (self)._value = (self).MIN
            else:
                (self)._value = (self).MAX

        else:
            (self)._value = (temp)

    def _getClass(self):
        return u"quark.ParsedInt"

    def _getField(self, name):
        if ((name) == (u"MINUS")):
            return ParsedNumber.MINUS

        if ((name) == (u"PLUS")):
            return ParsedNumber.PLUS

        if ((name) == (u"ZERO")):
            return ParsedNumber.ZERO

        if ((name) == (u"NINE")):
            return ParsedNumber.NINE

        if ((name) == (u"_value")):
            return (self)._value

        if ((name) == (u"_hasValue")):
            return (self)._hasValue

        if ((name) == (u"MIN")):
            return (self).MIN

        if ((name) == (u"MAX")):
            return (self).MAX

        return None

    def _setField(self, name, value):
        if ((name) == (u"MINUS")):
            ParsedNumber.MINUS = _cast(value, lambda: int)

        if ((name) == (u"PLUS")):
            ParsedNumber.PLUS = _cast(value, lambda: int)

        if ((name) == (u"ZERO")):
            ParsedNumber.ZERO = _cast(value, lambda: int)

        if ((name) == (u"NINE")):
            ParsedNumber.NINE = _cast(value, lambda: int)

        if ((name) == (u"_value")):
            (self)._value = _cast(value, lambda: int)

        if ((name) == (u"_hasValue")):
            (self)._hasValue = _cast(value, lambda: bool)

        if ((name) == (u"MIN")):
            (self).MIN = _cast(value, lambda: int)

        if ((name) == (u"MAX")):
            (self).MAX = _cast(value, lambda: int)


ParsedInt.quark_ParsedNumber_quark_int__ref = None
ParsedInt.quark_ParsedInt_ref = None
class ParsedLong(ParsedNumber):
    def _init(self):
        ParsedNumber._init(self)

    def __init__(self, num):
        super(ParsedLong, self).__init__();
        (self)._value = (self)._parseLong(num)

    def _getClass(self):
        return u"quark.ParsedLong"

    def _getField(self, name):
        if ((name) == (u"MINUS")):
            return ParsedNumber.MINUS

        if ((name) == (u"PLUS")):
            return ParsedNumber.PLUS

        if ((name) == (u"ZERO")):
            return ParsedNumber.ZERO

        if ((name) == (u"NINE")):
            return ParsedNumber.NINE

        if ((name) == (u"_value")):
            return (self)._value

        if ((name) == (u"_hasValue")):
            return (self)._hasValue

        return None

    def _setField(self, name, value):
        if ((name) == (u"MINUS")):
            ParsedNumber.MINUS = _cast(value, lambda: int)

        if ((name) == (u"PLUS")):
            ParsedNumber.PLUS = _cast(value, lambda: int)

        if ((name) == (u"ZERO")):
            ParsedNumber.ZERO = _cast(value, lambda: int)

        if ((name) == (u"NINE")):
            ParsedNumber.NINE = _cast(value, lambda: int)

        if ((name) == (u"_value")):
            (self)._value = _cast(value, lambda: int)

        if ((name) == (u"_hasValue")):
            (self)._hasValue = _cast(value, lambda: bool)


ParsedLong.quark_ParsedNumber_quark_long__ref = None
ParsedLong.quark_ParsedLong_ref = None
class ListUtil(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def slice(self, qlist, start, stop):
        result = _List([]);
        if ((start) >= (len(qlist))):
            start = len(qlist)
        else:
            start = (start) % (len(qlist))

        if ((stop) >= (len(qlist))):
            stop = len(qlist)
        else:
            stop = (stop) % (len(qlist))

        idx = start;
        while ((idx) < (stop)):
            (result).append((qlist)[idx]);
            idx = (idx) + (1)

        return result

    def _getClass(self):
        return u"quark.ListUtil<quark.Object>"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
ListUtil.quark_List_quark_Object__ref = None
class UnaryCallable(object):

    def call(self, arg):
        raise NotImplementedError('`UnaryCallable.call` is an abstract method')

UnaryCallable.quark_UnaryCallable_ref = None

def callUnaryCallable(callee, arg):
    """
    Allow native code to call UnaryCallables.
    """
    return (callee)(arg) if callable(callee) else (callee).call(arg)



def _getLogger(topic):
    if (quark.logging.Config._autoconfig()):
        (quark.logging.makeConfig()).configure();

    return (quark.concurrent.Context.runtime()).logger(topic)




def toJSON(obj, cls):
    """
    Serializes object tree into JSON. skips over fields starting with underscore
    """
    result = _JSONObject();
    if ((obj) == (None)):
        (result).setNull();
        return result

    if (((cls) == (None)) or ((cls).isAbstract())):
        cls = quark.reflect.Class.get(_getClass(obj))

    idx = 0;
    if (((cls).name) == (u"quark.String")):
        (result).setString(_cast(obj, lambda: unicode));
        return result

    if (((((((cls).name) == (u"quark.byte")) or (((cls).name) == (u"quark.short"))) or (((cls).name) == (u"quark.int"))) or (((cls).name) == (u"quark.long"))) or (((cls).name) == (u"quark.float"))):
        (result).setNumber(obj);
        return result

    if (((cls).name) == (u"quark.List")):
        (result).setList();
        qlist = _cast(obj, lambda: _List);
        while ((idx) < (len(qlist))):
            (result).setListItem(idx, toJSON((qlist)[idx], None));
            idx = (idx) + (1)

        return result

    if (((cls).name) == (u"quark.Map")):
        (result).setObject();
        map = _cast(obj, lambda: _Map);
        keys = _List(list((map).keys()));
        key = None;
        strKey = None;
        keyMap = {};
        strKeys = _List([]);
        while ((idx) < (len(keys))):
            key = (keys)[idx]
            strKey = _toString(key)
            strKey = (toJSON(key, ((cls).getParameters())[0])).toString()
            (keyMap)[strKey] = (key);
            (strKeys).append(strKey);
            idx = (idx) + (1)

        (strKeys).sort();
        idx = 0
        hash = _cast(None, lambda: _JSONObject);
        hashIdx = 0;
        while ((idx) < (len(strKeys))):
            strKey = (strKeys)[idx]
            key = (keyMap).get(strKey)
            value = (map).get(key);
            if (((quark.reflect.Class.get(_getClass(key))).name) == (u"quark.String")):
                (result).setObjectItem((_cast(key, lambda: unicode)), (toJSON(value, ((cls).getParameters())[1])));
            else:
                if ((hash) == (None)):
                    hash = (_JSONObject()).setList()
                    (result).setObjectItem((u"$map"), (hash));

                (hash).setListItem(hashIdx, toJSON(key, ((cls).getParameters())[0]));
                (hash).setListItem((hashIdx) + (1), toJSON(value, ((cls).getParameters())[1]));
                hashIdx = (hashIdx) + (2)

            idx = (idx) + (1)

        return result

    (result).setObjectItem((u"$class"), ((_JSONObject()).setString((cls).id)));
    fields = (cls).getFields();
    while ((idx) < (len(fields))):
        fieldName = ((fields)[idx]).name;
        if (not ((fieldName).startswith(u"_"))):
            (result).setObjectItem((fieldName), (toJSON((obj)._getField(fieldName), ((fields)[idx]).getType())));

        idx = (idx) + (1)

    return result


def fromJSON(cls, result, json):
    """
    deserialize json into provided result object. Skip over fields starting with underscore
    """
    if ((((json) == (None)) or ((json).isNull())) or ((json).isUndefined())):
        return None

    idx = 0;
    genericNumber = False;
    if (((cls) == (None)) or ((cls).isAbstract())):
        type = (json).getType();
        if ((type) == (u"boolean")):
            cls = quark.reflect.Class.BOOL

        if ((type) == (u"number")):
            cls = quark.reflect.Class.FLOAT
            genericNumber = True

        if ((type) == (u"string")):
            cls = quark.reflect.Class.STRING

        if ((type) == (u"list")):
            if ((result) == (None)):
                result = _List([])

            cls = quark.reflect.Class.get(_getClass(result))

        if ((type) == (u"object")):
            klazz = ((json).getObjectItem(u"$class")).getString();
            if ((klazz) != (None)):
                cls = quark.reflect.Class.get(klazz)
            else:
                if ((result) == (None)):
                    result = {}

                cls = quark.reflect.Class.get(_getClass(result))

    if ((result) == (None)):
        if (((cls).name) == (u"quark.String")):
            s = (json).getString();
            return s

        if (((cls).name) == (u"quark.float")):
            flt = (json).getNumber();
            if (genericNumber):
                if ((int(round(flt))) == (flt)):
                    l2 = int(round((json).getNumber()));
                    return l2

            return flt

        if (((cls).name) == (u"quark.int")):
            i = int(round((json).getNumber()));
            return i

        if (((cls).name) == (u"quark.long")):
            l = int(round((json).getNumber()));
            return l

        if (((cls).name) == (u"quark.bool")):
            b = (json).getBool();
            return b

        result = (cls).construct(_List([]))

    if (((cls).name) == (u"quark.List")):
        qlist = _cast(result, lambda: _List);
        while ((idx) < ((json).size())):
            (qlist).append(fromJSON(((cls).getParameters())[0], None, (json).getListItem(idx)));
            idx = (idx) + (1)

        return qlist

    if (((cls).name) == (u"quark.Map")):
        map = _cast(result, lambda: _Map);
        keys = (json).keys();
        while ((idx) < (len(keys))):
            key = (keys)[idx];
            value = (json).getObjectItem(key);
            if ((key) != (u"$map")):
                (map)[key] = (fromJSON(((cls).getParameters())[1], None, value));
            else:
                hashIdx = 0;
                while ((hashIdx) < ((value).size())):
                    hkey = fromJSON(((cls).getParameters())[0], None, (value).getListItem(hashIdx));
                    hvalue = fromJSON(((cls).getParameters())[1], None, (value).getListItem((hashIdx) + (1)));
                    (map)[hkey] = (hvalue);
                    hashIdx = (hashIdx) + (2)

            idx = (idx) + (1)

    fields = (cls).getFields();
    while ((idx) < (len(fields))):
        f = (fields)[idx];
        idx = (idx) + (1)
        if (((f).name).startswith(u"_")):
            continue;

        if ((((json).getObjectItem((f).name)).isDefined()) and (not (((json).getObjectItem((f).name)).isNull()))):
            (result)._setField(((f).name), (fromJSON((f).getType(), None, (json).getObjectItem((f).name))));

    return result


class ServletError(quark.error.Error):
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(ServletError, self).__init__(message);

    def _getClass(self):
        return u"quark.ServletError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


ServletError.quark_ServletError_ref = None
class Servlet(object):
    """
    A service addresable with an url
    """

    def onServletInit(self, url, runtime):
        """
        called after the servlet is successfully installed. The url will be the actual url used, important especially if ephemeral port was requested
        """
        pass

    def onServletError(self, url, error):
        """
        called if the servlet could not be installed
        """
        pass

    def onServletEnd(self, url):
        """
        called when the servlet is removed
        """
        pass

Servlet.quark_Servlet_ref = None
class Resolver(object):

    def resolve(self, serviceName):
        raise NotImplementedError('`Resolver.resolve` is an abstract method')

Resolver.quark_Resolver_ref = None
class ResponseHolder(_QObject):
    def _init(self):
        self.response = None
        self.failure = None

    def __init__(self): self._init()

    def onHTTPResponse(self, request, response):
        (self).response = response

    def onHTTPError(self, request, error):
        self.failure = error

    def _getClass(self):
        return u"quark.ResponseHolder"

    def _getField(self, name):
        if ((name) == (u"response")):
            return (self).response

        if ((name) == (u"failure")):
            return (self).failure

        return None

    def _setField(self, name, value):
        if ((name) == (u"response")):
            (self).response = _cast(value, lambda: HTTPResponse)

        if ((name) == (u"failure")):
            (self).failure = _cast(value, lambda: HTTPError)

    def onHTTPInit(self, request):
        pass

    def onHTTPFinal(self, request):
        pass
ResponseHolder.quark_ResponseHolder_ref = None
class Service(object):

    def getName(self):
        raise NotImplementedError('`Service.getName` is an abstract method')

    def getInstance(self):
        raise NotImplementedError('`Service.getInstance` is an abstract method')

    def getTimeout(self):
        raise NotImplementedError('`Service.getTimeout` is an abstract method')

    def rpc(self, methodName, args):
        rpc = quark.behaviors.RPC(self, methodName);
        return (rpc).call(args)


Service.quark_Service_ref = None
class BaseService(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def getName(self):
        return _cast(None, lambda: unicode)

    def getInstance(self):
        return _cast(None, lambda: ServiceInstance)

    def getTimeout(self):
        return -(1.0)

    def _getClass(self):
        return u"quark.BaseService"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

    def rpc(self, methodName, args):
        rpc = quark.behaviors.RPC(self, methodName);
        return (rpc).call(args)

BaseService.quark_BaseService_ref = None
class ServiceInstance(_QObject):
    def _init(self):
        self.serviceName = None
        self.url = None
        self.breaker = None

    def __init__(self, serviceName, url, failureLimit, retestDelay):
        self._init()
        (self).serviceName = serviceName
        (self).url = url
        (self).breaker = quark.behaviors.CircuitBreaker(((((u"[") + (serviceName)) + (u" at ")) + (url)) + (u"]"), failureLimit, retestDelay)

    def isActive(self):
        return ((self).breaker).active

    def getURL(self):
        return (self).url

    def succeed(self, info):
        if (not ((self).isActive())):
            (Client.logger).info((((u"- CLOSE breaker for ") + ((self).serviceName)) + (u" at ")) + ((self).url));

        ((self).breaker).succeed();

    def fail(self, info):
        if (not ((self).isActive())):
            (Client.logger).warn((((u"- OPEN breaker for ") + ((self).serviceName)) + (u" at ")) + ((self).url));

        ((self).breaker).fail();

    def _getClass(self):
        return u"quark.ServiceInstance"

    def _getField(self, name):
        if ((name) == (u"serviceName")):
            return (self).serviceName

        if ((name) == (u"url")):
            return (self).url

        if ((name) == (u"breaker")):
            return (self).breaker

        return None

    def _setField(self, name, value):
        if ((name) == (u"serviceName")):
            (self).serviceName = _cast(value, lambda: unicode)

        if ((name) == (u"url")):
            (self).url = _cast(value, lambda: unicode)

        if ((name) == (u"breaker")):
            (self).breaker = _cast(value, lambda: quark.behaviors.CircuitBreaker)


ServiceInstance.quark_ServiceInstance_ref = None
class DegenerateResolver(_QObject):
    """
    DegenerateResolver assumes that the serviceName is an URL.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def resolve(self, serviceName):
        return _List([serviceName])

    def _getClass(self):
        return u"quark.DegenerateResolver"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
DegenerateResolver.quark_DegenerateResolver_ref = None
class Client(_QObject):
    def _init(self):
        self.resolver = None
        self.serviceName = None
        self._timeout = None
        self._failureLimit = 3
        self._retestDelay = 30.0
        self.mutex = None
        self.instanceMap = None
        self.counter = None

    def __init__(self, serviceName):
        self._init()
        (self).serviceName = serviceName
        (self).resolver = DegenerateResolver()
        (self)._timeout = 0.0
        (self).mutex = _Lock()
        (self).instanceMap = {}
        (self).counter = 0
        failureLimit = _cast((self)._getField(u"failureLimit"), lambda: int);
        if ((failureLimit) != (None)):
            (self)._failureLimit = failureLimit

        (Client.logger).info(((_toString(self)) + (u" failureLimit ")) + (_toString((self)._failureLimit)));
        retestDelay = _cast((self)._getField(u"retestDelay"), lambda: float);
        if ((retestDelay) != (None)):
            (self)._retestDelay = retestDelay

        (Client.logger).info(((_toString(self)) + (u" retestDelay ")) + (repr((self)._retestDelay)));

    def setResolver(self, resolver):
        (self).resolver = resolver

    def getInstance(self):
        urls = ((self).resolver).resolve((self).serviceName);
        if ((len(urls)) <= (0)):
            return _cast(None, lambda: ServiceInstance)

        (urls).sort();
        ((self).mutex).acquire();
        result = _cast(None, lambda: ServiceInstance);
        next = ((self).counter) % (len(urls));
        (self).counter = ((self).counter) + (1)
        idx = next;
        while (True):
            url = (urls)[idx];
            instance = ((self).instanceMap).get(url);
            if ((instance) == (None)):
                instance = ServiceInstance((self).serviceName, url, self._failureLimit, self._retestDelay)
                ((self).instanceMap)[url] = (instance);

            if ((instance).isActive()):
                (Client.logger).info((((((u"- ") + ((self).serviceName)) + (u" using instance ")) + (_toString((idx) + (1)))) + (u": ")) + (url));
                result = instance
                break;

            idx = ((idx) + (1)) % (len(urls))
            if ((idx) == (next)):
                (Client.logger).info(((u"- ") + ((self).serviceName)) + (u": no live instances! giving up."));
                break;

        ((self).mutex).release();
        return result

    def getName(self):
        return (self).serviceName

    def getTimeout(self):
        return (self)._timeout

    def setTimeout(self, timeout):
        (self)._timeout = timeout

    def _getClass(self):
        return u"quark.Client"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return Client.logger

        if ((name) == (u"resolver")):
            return (self).resolver

        if ((name) == (u"serviceName")):
            return (self).serviceName

        if ((name) == (u"_timeout")):
            return (self)._timeout

        if ((name) == (u"_failureLimit")):
            return (self)._failureLimit

        if ((name) == (u"_retestDelay")):
            return (self)._retestDelay

        if ((name) == (u"mutex")):
            return (self).mutex

        if ((name) == (u"instanceMap")):
            return (self).instanceMap

        if ((name) == (u"counter")):
            return (self).counter

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            Client.logger = value

        if ((name) == (u"resolver")):
            (self).resolver = _cast(value, lambda: Resolver)

        if ((name) == (u"serviceName")):
            (self).serviceName = _cast(value, lambda: unicode)

        if ((name) == (u"_timeout")):
            (self)._timeout = _cast(value, lambda: float)

        if ((name) == (u"_failureLimit")):
            (self)._failureLimit = _cast(value, lambda: int)

        if ((name) == (u"_retestDelay")):
            (self)._retestDelay = _cast(value, lambda: float)

        if ((name) == (u"mutex")):
            (self).mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"instanceMap")):
            (self).instanceMap = _cast(value, lambda: _Map)

        if ((name) == (u"counter")):
            (self).counter = _cast(value, lambda: int)


Client.logger = _getLogger(u"quark.client")
Client.quark_Map_quark_String_quark_ServiceInstance__ref = None
Client.quark_Client_ref = None
class ServerResponder(_QObject):
    def _init(self):
        self.sendCORS = None
        self.request = None
        self.response = None

    def __init__(self, sendCORS, request, response):
        self._init()
        (self).sendCORS = sendCORS
        (self).request = request
        (self).response = response

    def onFuture(self, result):
        error = (result).getError();
        if ((error) != (None)):
            (self.response).setCode(404);
        else:
            if ((self).sendCORS):
                ((self).response).setHeader(u"Access-Control-Allow-Origin", u"*");

            ((self).response).setBody((toJSON(result, None)).toString());
            ((self).response).setCode(200);

        (quark.concurrent.Context.runtime()).respond(self.request, self.response);

    def _getClass(self):
        return u"quark.ServerResponder"

    def _getField(self, name):
        if ((name) == (u"sendCORS")):
            return (self).sendCORS

        if ((name) == (u"request")):
            return (self).request

        if ((name) == (u"response")):
            return (self).response

        return None

    def _setField(self, name, value):
        if ((name) == (u"sendCORS")):
            (self).sendCORS = _cast(value, lambda: bool)

        if ((name) == (u"request")):
            (self).request = _cast(value, lambda: HTTPRequest)

        if ((name) == (u"response")):
            (self).response = _cast(value, lambda: HTTPResponse)


ServerResponder.quark_ServerResponder_ref = None
class Server(_QObject):
    def _init(self):
        self.impl = None
        self._sendCORS = None

    def __init__(self, impl):
        self._init()
        (self).impl = impl
        (self)._sendCORS = False

    def sendCORS(self, send):
        (self)._sendCORS = send

    def onHTTPRequest(self, request, response):
        body = (request).getBody();
        envelope = _JSONObject.parse(body);
        if ((((envelope).getObjectItem(u"$method")) == ((envelope).undefined())) or (((envelope).getObjectItem(u"rpc")) == ((envelope).undefined()))):
            (response).setBody(((u"Failed to understand request.\n\n") + (body)) + (u"\n"));
            (response).setCode(400);
            (quark.concurrent.Context.runtime()).respond(request, response);
        else:
            methodName = ((envelope).getObjectItem(u"$method")).getString();
            json = (envelope).getObjectItem(u"rpc");
            method = (((quark.reflect.Class.get(_getClass(self))).getField(u"impl")).getType()).getMethod(methodName);
            params = (method).getParameters();
            args = _List([]);
            idx = 0;
            while ((idx) < (len(params))):
                (args).append(fromJSON((params)[idx], None, (json).getListItem(idx)));
                idx = (idx) + (1)

            result = _cast((method).invoke(self.impl, args), lambda: quark.concurrent.Future);
            (result).onFinished(ServerResponder((self)._sendCORS, request, response));

    def onServletError(self, url, error):
        (quark.concurrent.Context.runtime()).fail((((u"RPC Server failed to register ") + (url)) + (u" due to: ")) + ((error).getMessage()));

    def _getClass(self):
        return u"quark.Server<quark.Object>"

    def _getField(self, name):
        if ((name) == (u"impl")):
            return (self).impl

        if ((name) == (u"_sendCORS")):
            return (self)._sendCORS

        return None

    def _setField(self, name, value):
        if ((name) == (u"impl")):
            (self).impl = _cast(value, lambda: T)

        if ((name) == (u"_sendCORS")):
            (self)._sendCORS = _cast(value, lambda: bool)

    def serveHTTP(self, url):
        (quark.concurrent.Context.runtime()).serveHTTP(url, self);

    def onServletInit(self, url, runtime):
        """
        called after the servlet is successfully installed. The url will be the actual url used, important especially if ephemeral port was requested
        """
        pass

    def onServletEnd(self, url):
        """
        called when the servlet is removed
        """
        pass
Server.quark_Server_quark_Object__ref = None


class HTTPError(quark.error.Error):
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(HTTPError, self).__init__(message);

    def _getClass(self):
        return u"quark.HTTPError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


HTTPError.quark_HTTPError_ref = None
class HTTPHandler(object):

    def onHTTPInit(self, request):
        pass

    def onHTTPResponse(self, request, response):
        pass

    def onHTTPError(self, request, message):
        pass

    def onHTTPFinal(self, request):
        pass

HTTPHandler.quark_HTTPHandler_ref = None
class HTTPRequest(object):

    def getUrl(self):
        raise NotImplementedError('`HTTPRequest.getUrl` is an abstract method')

    def setMethod(self, method):
        raise NotImplementedError('`HTTPRequest.setMethod` is an abstract method')

    def getMethod(self):
        raise NotImplementedError('`HTTPRequest.getMethod` is an abstract method')

    def setBody(self, data):
        raise NotImplementedError('`HTTPRequest.setBody` is an abstract method')

    def getBody(self):
        raise NotImplementedError('`HTTPRequest.getBody` is an abstract method')

    def setHeader(self, key, value):
        raise NotImplementedError('`HTTPRequest.setHeader` is an abstract method')

    def getHeader(self, key):
        raise NotImplementedError('`HTTPRequest.getHeader` is an abstract method')

    def getHeaders(self):
        raise NotImplementedError('`HTTPRequest.getHeaders` is an abstract method')

HTTPRequest.quark_HTTPRequest_ref = None
class HTTPResponse(object):

    def getCode(self):
        raise NotImplementedError('`HTTPResponse.getCode` is an abstract method')

    def setCode(self, code):
        raise NotImplementedError('`HTTPResponse.setCode` is an abstract method')

    def getBody(self):
        raise NotImplementedError('`HTTPResponse.getBody` is an abstract method')

    def setBody(self, body):
        raise NotImplementedError('`HTTPResponse.setBody` is an abstract method')

    def setHeader(self, key, value):
        raise NotImplementedError('`HTTPResponse.setHeader` is an abstract method')

    def getHeader(self, key):
        raise NotImplementedError('`HTTPResponse.getHeader` is an abstract method')

    def getHeaders(self):
        raise NotImplementedError('`HTTPResponse.getHeaders` is an abstract method')

HTTPResponse.quark_HTTPResponse_ref = None
class HTTPServlet(object):
    """
    Http servlet
    """

    def onHTTPRequest(self, request, response):
        """
        incoming request. respond with Runtime.respond(). After responding the objects may get recycled by the runtime
        """
        pass

    def serveHTTP(self, url):
        (quark.concurrent.Context.runtime()).serveHTTP(url, self);


HTTPServlet.quark_HTTPServlet_ref = None

class WSError(quark.error.Error):
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(WSError, self).__init__(message);

    def _getClass(self):
        return u"quark.WSError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


WSError.quark_WSError_ref = None
class WSHandler(object):

    def onWSInit(self, socket):
        """
        Called when the WebSocket is first created.
        """
        pass

    def onWSConnected(self, socket):
        """
        Called when the WebSocket connects successfully.
        """
        pass

    def onWSMessage(self, socket, message):
        """
        Called when the WebSocket receives a message.
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

    def onWSError(self, socket, error):
        """
        Called when the WebSocket disconnects with an error, or fails to connect.
        """
        pass

    def onWSFinal(self, socket):
        """
        Called when the WebSocket is done with life, one way or another.
        """
        pass

WSHandler.quark_WSHandler_ref = None
class WebSocket(object):

    def send(self, message):
        raise NotImplementedError('`WebSocket.send` is an abstract method')

    def sendBinary(self, bytes):
        raise NotImplementedError('`WebSocket.sendBinary` is an abstract method')

    def close(self):
        raise NotImplementedError('`WebSocket.close` is an abstract method')

WebSocket.quark_WebSocket_ref = None
class WSServlet(object):
    """
    Websocket servlet
    """

    def onWSConnect(self, upgrade_request):
        """
        called for each new incoming WebSocket connection
        """
        return _cast(None, lambda: WSHandler)

    def serveWS(self, url):
        (quark.concurrent.Context.runtime()).serveWS(url, self);


WSServlet.quark_WSServlet_ref = None


class URL(_QObject):
    """
    A URL class.
    """
    def _init(self):
        self.scheme = None
        self.host = None
        self.port = None
        self.path = None

    def __init__(self): self._init()

    @staticmethod
    def parse(url):
        result = URL();
        if ((url) == (None)):
            return _cast(None, lambda: URL)

        parts = None;
        remaining = None;
        idx = (url).find(u"://");
        if ((idx) >= (0)):
            (result).scheme = (url)[(0):(idx)]
            remaining = (url)[((idx) + (3)):(len(url))]
        else:
            remaining = url

        firstSlash = (remaining).find(u"/");
        if ((firstSlash) == (0)):
            (result).path = remaining
            return result

        if ((firstSlash) < (0)):
            firstSlash = len(remaining)
        else:
            (result).path = (remaining)[(firstSlash):(len(remaining))]

        idx = (remaining).find(u":")
        if ((idx) > (firstSlash)):
            (result).host = (remaining)[(0):(firstSlash)]
        else:
            if ((idx) >= (0)):
                (result).host = (remaining)[(0):(idx)]
                (result).port = (remaining)[((idx) + (1)):(firstSlash)]
            else:
                (result).host = (remaining)[(0):(firstSlash)]

        return result

    def toString(self):
        result = u"";
        if ((self.scheme) != (None)):
            result = (self.scheme) + (u"://")

        if ((self.host) != (None)):
            result = (result) + (self.host)

        if ((self.port) != (None)):
            result = ((result) + (u":")) + (self.port)

        if ((self.path) != (None)):
            result = (result) + (self.path)

        return result

    def _getClass(self):
        return u"quark.URL"

    def _getField(self, name):
        if ((name) == (u"scheme")):
            return (self).scheme

        if ((name) == (u"host")):
            return (self).host

        if ((name) == (u"port")):
            return (self).port

        if ((name) == (u"path")):
            return (self).path

        return None

    def _setField(self, name, value):
        if ((name) == (u"scheme")):
            (self).scheme = _cast(value, lambda: unicode)

        if ((name) == (u"host")):
            (self).host = _cast(value, lambda: unicode)

        if ((name) == (u"port")):
            (self).port = _cast(value, lambda: unicode)

        if ((name) == (u"path")):
            (self).path = _cast(value, lambda: unicode)


URL.quark_URL_ref = None






class _ChainPromise(_QObject):
    def _init(self):
        self._next = None

    def __init__(self, next):
        self._init()
        (self)._next = next

    def call(self, arg):
        _CallbackEvent.fullfilPromise((self)._next, arg);
        return None

    def _getClass(self):
        return u"quark._ChainPromise"

    def _getField(self, name):
        if ((name) == (u"_next")):
            return (self)._next

        return None

    def _setField(self, name, value):
        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)


_ChainPromise.quark__ChainPromise_ref = None
class _CallbackEvent(_QObject):
    def _init(self):
        self._callable = None
        self._next = None
        self._value = None
        self._callback = None

    def __init__(self, callable, next, value, callback):
        self._init()
        (self)._callable = callable
        (self)._next = next
        (self)._value = value
        (self)._callback = callback

    def getContext(self):
        return (self)._callback

    @staticmethod
    def fullfilPromise(promise, value):
        if ((quark.reflect.Class.ERROR).hasInstance(value)):
            (promise)._reject(_cast(value, lambda: quark.error.Error));
        else:
            (promise)._resolve(value);

    def fireEvent(self):
        result = ((self)._callable)((self)._value) if callable((self)._callable) else ((self)._callable).call((self)._value);
        if ((quark.reflect.Class.get(u"quark.Promise")).hasInstance(result)):
            toChain = _cast(result, lambda: Promise);
            (toChain).andFinally(_ChainPromise((self)._next));
        else:
            _CallbackEvent.fullfilPromise((self)._next, result);

    def _getClass(self):
        return u"quark._CallbackEvent"

    def _getField(self, name):
        if ((name) == (u"_callable")):
            return (self)._callable

        if ((name) == (u"_next")):
            return (self)._next

        if ((name) == (u"_value")):
            return (self)._value

        if ((name) == (u"_callback")):
            return (self)._callback

        return None

    def _setField(self, name, value):
        if ((name) == (u"_callable")):
            (self)._callable = _cast(value, lambda: UnaryCallable)

        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)

        if ((name) == (u"_value")):
            (self)._value = value

        if ((name) == (u"_callback")):
            (self)._callback = _cast(value, lambda: _Callback)


_CallbackEvent.quark__CallbackEvent_ref = None
class _Callback(quark.concurrent.EventContext):
    def _init(self):
        quark.concurrent.EventContext._init(self)
        self._callable = None
        self._next = None

    def __init__(self, callable, next):
        super(_Callback, self).__init__();
        (self)._callable = callable
        (self)._next = next

    def call(self, result):
        event = _CallbackEvent((self)._callable, (self)._next, result, self);
        (((self).getContext()).collector).put(event);

    def _getClass(self):
        return u"quark._Callback"

    def _getField(self, name):
        if ((name) == (u"_context")):
            return (self)._context

        if ((name) == (u"_callable")):
            return (self)._callable

        if ((name) == (u"_next")):
            return (self)._next

        return None

    def _setField(self, name, value):
        if ((name) == (u"_context")):
            (self)._context = _cast(value, lambda: quark.concurrent.Context)

        if ((name) == (u"_callable")):
            (self)._callable = _cast(value, lambda: UnaryCallable)

        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)


_Callback.quark__Callback_ref = None
class _Passthrough(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def call(self, arg):
        return arg

    def _getClass(self):
        return u"quark._Passthrough"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
_Passthrough.quark__Passthrough_ref = None
class _CallIfIsInstance(_QObject):
    def _init(self):
        self._underlying = None
        self._class = None

    def __init__(self, underlying, klass):
        self._init()
        (self)._underlying = underlying
        (self)._class = klass

    def call(self, arg):
        if (((self)._class).hasInstance(arg)):
            return ((self)._underlying)(arg) if callable((self)._underlying) else ((self)._underlying).call(arg)
        else:
            return arg

    def _getClass(self):
        return u"quark._CallIfIsInstance"

    def _getField(self, name):
        if ((name) == (u"_underlying")):
            return (self)._underlying

        if ((name) == (u"_class")):
            return (self)._class

        return None

    def _setField(self, name, value):
        if ((name) == (u"_underlying")):
            (self)._underlying = _cast(value, lambda: UnaryCallable)

        if ((name) == (u"_class")):
            (self)._class = _cast(value, lambda: quark.reflect.Class)


_CallIfIsInstance.quark__CallIfIsInstance_ref = None
class PromiseValue(_QObject):
    """
    Snapshot of the value of a Promise, if it has one.
    """
    def _init(self):
        self._successResult = None
        self._failureResult = None
        self._hasValue = None

    def __init__(self, successResult, failureResult, hasValue):
        self._init()
        (self)._successResult = successResult
        (self)._failureResult = failureResult
        (self)._hasValue = hasValue

    def hasValue(self):
        """
        Return true if the Promise had a value at the time this was created.
        """
        return (self)._hasValue

    def isError(self):
        """
        Return true if value is error. Result is only valid if hasValue() is true.
        """
        return ((self)._failureResult) != (None)

    def getValue(self):
        """
        Return the value. Result is only valid if hasValue() is true.
        """
        if ((self).isError()):
            return (self)._failureResult
        else:
            return (self)._successResult

    def _getClass(self):
        return u"quark.PromiseValue"

    def _getField(self, name):
        if ((name) == (u"_successResult")):
            return (self)._successResult

        if ((name) == (u"_failureResult")):
            return (self)._failureResult

        if ((name) == (u"_hasValue")):
            return (self)._hasValue

        return None

    def _setField(self, name, value):
        if ((name) == (u"_successResult")):
            (self)._successResult = value

        if ((name) == (u"_failureResult")):
            (self)._failureResult = _cast(value, lambda: quark.error.Error)

        if ((name) == (u"_hasValue")):
            (self)._hasValue = _cast(value, lambda: bool)


PromiseValue.quark_PromiseValue_ref = None
class Promise(_QObject):
    """
    An object that will eventually have a result.
    Results are passed to callables whose return value is passed
    to resulting Promise. If a return result is a Promise it will
    be chained automatically, i.e. callables will never be called
    with a Promise, only with values.
    """
    def _init(self):
        self._lock = None
        self._successResult = None
        self._failureResult = None
        self._hasResult = None
        self._successCallbacks = None
        self._failureCallbacks = None

    def __init__(self):
        self._init()
        (self)._lock = _Lock()
        (self)._hasResult = False
        (self)._successResult = None
        (self)._failureResult = _cast(None, lambda: quark.error.Error)
        (self)._successCallbacks = _List([])
        (self)._failureCallbacks = _List([])

    def _maybeRunCallbacks(self):
        ((self)._lock).acquire();
        if (not ((self)._hasResult)):
            ((self)._lock).release();
            return

        callbacks = (self)._successCallbacks;
        value = (self)._successResult;
        if (((self)._failureResult) != (None)):
            callbacks = (self)._failureCallbacks
            value = (self)._failureResult

        (self)._failureCallbacks = _List([])
        (self)._successCallbacks = _List([])
        ((self)._lock).release();
        idx = 0;
        while ((idx) < (len(callbacks))):
            ((callbacks)[idx]).call(value);
            idx = (idx) + (1)

    def _resolve(self, result):
        if ((quark.reflect.Class.ERROR).hasInstance(result)):
            (self)._reject(_cast(result, lambda: quark.error.Error));
            return

        ((self)._lock).acquire();
        if ((self)._hasResult):
            _println(u"BUG: Resolved Promise that already has a value.");
            ((self)._lock).release();
            return

        (self)._hasResult = True
        (self)._successResult = result
        ((self)._lock).release();
        (self)._maybeRunCallbacks();

    def _reject(self, err):
        ((self)._lock).acquire();
        if ((self)._hasResult):
            _println(u"BUG: Rejected Promise that already has a value.");
            ((self)._lock).release();
            return

        (self)._hasResult = True
        (self)._failureResult = err
        ((self)._lock).release();
        (self)._maybeRunCallbacks();

    def andThen(self, callable):
        """
        Add callback that will be called on non-Error values.
        Its result will become the value of the returned Promise.
        """
        result = Promise();
        ((self)._lock).acquire();
        ((self)._successCallbacks).append(_Callback(callable, result));
        ((self)._failureCallbacks).append(_Callback(_Passthrough(), result));
        ((self)._lock).release();
        (self)._maybeRunCallbacks();
        return result

    def andCatch(self, errorClass, callable):
        """
        Add callback that will be called on Error values.
        Its result will become the value of the returned Promise.
        """
        result = Promise();
        callback = _Callback(_CallIfIsInstance(callable, errorClass), result);
        ((self)._lock).acquire();
        ((self)._failureCallbacks).append(callback);
        ((self)._successCallbacks).append(_Callback(_Passthrough(), result));
        ((self)._lock).release();
        (self)._maybeRunCallbacks();
        return result

    def andEither(self, success, failure):
        """
        Two callbacks, one for success and one for error results.
        """
        result = Promise();
        ((self)._lock).acquire();
        ((self)._successCallbacks).append(_Callback(success, result));
        ((self)._failureCallbacks).append(_Callback(failure, result));
        ((self)._lock).release();
        (self)._maybeRunCallbacks();
        return result

    def andFinally(self, callable):
        """
        Callback that will be called for both success and error results.
        """
        return self.andEither(callable, callable)

    def value(self):
        """
        Synchronous extraction of the promise's current value, if it has any.
        Its result will become the value of the returned Promise.
        """
        ((self)._lock).acquire();
        result = PromiseValue((self)._successResult, (self)._failureResult, (self)._hasResult);
        ((self)._lock).release();
        return result

    def _getClass(self):
        return u"quark.Promise"

    def _getField(self, name):
        if ((name) == (u"_lock")):
            return (self)._lock

        if ((name) == (u"_successResult")):
            return (self)._successResult

        if ((name) == (u"_failureResult")):
            return (self)._failureResult

        if ((name) == (u"_hasResult")):
            return (self)._hasResult

        if ((name) == (u"_successCallbacks")):
            return (self)._successCallbacks

        if ((name) == (u"_failureCallbacks")):
            return (self)._failureCallbacks

        return None

    def _setField(self, name, value):
        if ((name) == (u"_lock")):
            (self)._lock = _cast(value, lambda: _Lock)

        if ((name) == (u"_successResult")):
            (self)._successResult = value

        if ((name) == (u"_failureResult")):
            (self)._failureResult = _cast(value, lambda: quark.error.Error)

        if ((name) == (u"_hasResult")):
            (self)._hasResult = _cast(value, lambda: bool)

        if ((name) == (u"_successCallbacks")):
            (self)._successCallbacks = _cast(value, lambda: _List)

        if ((name) == (u"_failureCallbacks")):
            (self)._failureCallbacks = _cast(value, lambda: _List)


Promise.quark_List_quark__Callback__ref = None
Promise.quark_Promise_ref = None
class PromiseFactory(_QObject):
    """
    Create Promises and input their initial value. Should typically only be used by Quark standard library.
    """
    def _init(self):
        self.promise = None

    def __init__(self):
        self._init()
        (self).promise = Promise()

    def resolve(self, result):
        """
        Set the attached Promise's initial value.
        """
        ((self).promise)._resolve(result);

    def reject(self, err):
        """
        Set the attached Promise's initial value to an Error.
        """
        ((self).promise)._reject(err);

    def _getClass(self):
        return u"quark.PromiseFactory"

    def _getField(self, name):
        if ((name) == (u"promise")):
            return (self).promise

        return None

    def _setField(self, name, value):
        if ((name) == (u"promise")):
            (self).promise = _cast(value, lambda: Promise)


PromiseFactory.quark_PromiseFactory_ref = None
class _BoundMethod(_QObject):
    def _init(self):
        self.target = None
        self.method = None
        self.additionalArgs = None

    def __init__(self, target, methodName, additionalArgs):
        self._init()
        (self).target = target
        (self).method = (quark.reflect.Class.get(_getClass(target))).getMethod(methodName)
        (self).additionalArgs = additionalArgs

    def call(self, arg):
        args = (ListUtil()).slice(self.additionalArgs, 0, len(self.additionalArgs));
        (args).insert((0), (arg));
        return ((self).method).invoke((self).target, args)

    def _getClass(self):
        return u"quark._BoundMethod"

    def _getField(self, name):
        if ((name) == (u"target")):
            return (self).target

        if ((name) == (u"method")):
            return (self).method

        if ((name) == (u"additionalArgs")):
            return (self).additionalArgs

        return None

    def _setField(self, name, value):
        if ((name) == (u"target")):
            (self).target = value

        if ((name) == (u"method")):
            (self).method = _cast(value, lambda: quark.reflect.Method)

        if ((name) == (u"additionalArgs")):
            (self).additionalArgs = _cast(value, lambda: _List)


_BoundMethod.quark__BoundMethod_ref = None

class _IOScheduleTask(_QObject):
    def _init(self):
        self.factory = None

    def __init__(self, factory):
        self._init()
        (self).factory = factory

    def onExecute(self, runtime):
        ((self).factory).resolve(True);

    def _getClass(self):
        return u"quark._IOScheduleTask"

    def _getField(self, name):
        if ((name) == (u"factory")):
            return (self).factory

        return None

    def _setField(self, name, value):
        if ((name) == (u"factory")):
            (self).factory = _cast(value, lambda: PromiseFactory)


_IOScheduleTask.quark__IOScheduleTask_ref = None
class _IOHTTPHandler(_QObject):
    def _init(self):
        self.factory = None

    def __init__(self, factory):
        self._init()
        (self).factory = factory

    def onHTTPInit(self, request):
        pass

    def onHTTPFinal(self, request):
        pass

    def onHTTPResponse(self, request, response):
        ((self).factory).resolve(response);

    def onHTTPError(self, request, message):
        ((self).factory).reject(message);

    def _getClass(self):
        return u"quark._IOHTTPHandler"

    def _getField(self, name):
        if ((name) == (u"factory")):
            return (self).factory

        return None

    def _setField(self, name, value):
        if ((name) == (u"factory")):
            (self).factory = _cast(value, lambda: PromiseFactory)


_IOHTTPHandler.quark__IOHTTPHandler_ref = None
class IO(_QObject):
    """
    Promise-based I/O and scheduling APIs.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def httpRequest(request):
        """
        Send a HTTP request, get back Promise that gets HTTPResponse or HTTPError result.
        """
        factory = PromiseFactory();
        (quark.concurrent.Context.runtime()).request(request, _IOHTTPHandler(factory));
        return (factory).promise

    @staticmethod
    def schedule(delayInSeconds):
        """
        Schedule a callable to run in the future, return Promise with null result.
        """
        factory = PromiseFactory();
        (quark.concurrent.Context.runtime()).schedule(_IOScheduleTask(factory), delayInSeconds);
        return (factory).promise

    def _getClass(self):
        return u"quark.IO"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
IO.quark_IO_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark")
