# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.spi_api")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent


class ServletProxy(_QObject):
    def _init(self):
        self.servlet_impl = None
        self.real_runtime = None

    def __init__(self, real_runtime, servlet_impl):
        self._init()
        (self).real_runtime = real_runtime
        (self).servlet_impl = servlet_impl

    def onServletInit(self, url, runtime):
        (self.servlet_impl).onServletInit(url, self.real_runtime);

    def onServletError(self, url, error):
        (self.servlet_impl).onServletError(url, error);

    def onServletEnd(self, url):
        (self.servlet_impl).onServletEnd(url);

    def _getClass(self):
        return u"quark.spi_api.ServletProxy"

    def _getField(self, name):
        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        return None

    def _setField(self, name, value):
        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: quark.Runtime)


ServletProxy.quark_spi_api_ServletProxy_ref = None
class HTTPServletProxy(ServletProxy):
    def _init(self):
        ServletProxy._init(self)
        self.http_servlet_impl = None

    def __init__(self, real_runtime, http_servlet_impl):
        super(HTTPServletProxy, self).__init__(real_runtime, http_servlet_impl);
        (self).http_servlet_impl = http_servlet_impl

    def onHTTPRequest(self, request, response):
        (self.http_servlet_impl).onHTTPRequest(request, response);

    def _getClass(self):
        return u"quark.spi_api.HTTPServletProxy"

    def _getField(self, name):
        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        if ((name) == (u"http_servlet_impl")):
            return (self).http_servlet_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: quark.Runtime)

        if ((name) == (u"http_servlet_impl")):
            (self).http_servlet_impl = _cast(value, lambda: quark.HTTPServlet)

    def serveHTTP(self, url):
        (quark.concurrent.Context.runtime()).serveHTTP(url, self);

HTTPServletProxy.quark_spi_api_HTTPServletProxy_ref = None
class WSServletProxy(ServletProxy):
    def _init(self):
        ServletProxy._init(self)
        self.ws_servlet_impl = None

    def __init__(self, real_runtime, ws_servlet_impl):
        super(WSServletProxy, self).__init__(real_runtime, ws_servlet_impl);
        (self).ws_servlet_impl = ws_servlet_impl

    def onWSConnect(self, upgradeRequest):
        return (self.ws_servlet_impl).onWSConnect(upgradeRequest)

    def _getClass(self):
        return u"quark.spi_api.WSServletProxy"

    def _getField(self, name):
        if ((name) == (u"servlet_impl")):
            return (self).servlet_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        if ((name) == (u"ws_servlet_impl")):
            return (self).ws_servlet_impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"servlet_impl")):
            (self).servlet_impl = _cast(value, lambda: quark.Servlet)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: quark.Runtime)

        if ((name) == (u"ws_servlet_impl")):
            (self).ws_servlet_impl = _cast(value, lambda: quark.WSServlet)

    def serveWS(self, url):
        (quark.concurrent.Context.runtime()).serveWS(url, self);

WSServletProxy.quark_spi_api_WSServletProxy_ref = None
class TaskProxy(_QObject):
    def _init(self):
        self.task_impl = None
        self.real_runtime = None

    def __init__(self, real_runtime, task_impl):
        self._init()
        (self).task_impl = task_impl
        (self).real_runtime = real_runtime

    def onExecute(self, runtime):
        (self.task_impl).onExecute(self.real_runtime);

    def _getClass(self):
        return u"quark.spi_api.TaskProxy"

    def _getField(self, name):
        if ((name) == (u"task_impl")):
            return (self).task_impl

        if ((name) == (u"real_runtime")):
            return (self).real_runtime

        return None

    def _setField(self, name, value):
        if ((name) == (u"task_impl")):
            (self).task_impl = _cast(value, lambda: quark.Task)

        if ((name) == (u"real_runtime")):
            (self).real_runtime = _cast(value, lambda: quark.Runtime)


TaskProxy.quark_spi_api_TaskProxy_ref = None
class RuntimeProxy(_QObject):
    def _init(self):
        self.impl = None

    def __init__(self, impl):
        self._init()
        (self).impl = impl

    def open(self, url, handler):
        (self.impl).open(url, handler);

    def request(self, request, handler):
        (self.impl).request(request, handler);

    def schedule(self, handler, delayInSeconds):
        (self.impl).schedule(TaskProxy(self, handler), delayInSeconds);

    def codec(self):
        return (self.impl).codec()

    def now(self):
        return (self.impl).now()

    def sleep(self, seconds):
        (self.impl).sleep(seconds);

    def uuid(self):
        return (self.impl).uuid()

    def serveHTTP(self, url, servlet):
        (self.impl).serveHTTP(url, HTTPServletProxy(self, servlet));

    def serveWS(self, url, servlet):
        (self.impl).serveWS(url, WSServletProxy(self, servlet));

    def respond(self, request, response):
        (self.impl).respond(request, response);

    def fail(self, message):
        (self.impl).fail(message);

    def logger(self, topic):
        return (self.impl).logger(topic)

    def callSafely(self, callee, defaultResult):
        return (self.impl).callSafely(callee, defaultResult)

    def _getClass(self):
        return u"quark.spi_api.RuntimeProxy"

    def _getField(self, name):
        if ((name) == (u"impl")):
            return (self).impl

        return None

    def _setField(self, name, value):
        if ((name) == (u"impl")):
            (self).impl = _cast(value, lambda: quark.Runtime)


RuntimeProxy.quark_spi_api_RuntimeProxy_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.spi_api")
