# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("datawire_mdk_md.mdk_MDK_start_Method")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect

class mdk_MDK_start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_start_Method, self).__init__(u"quark.void", u"start", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        (obj).start();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK_stop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_stop_Method, self).__init__(u"quark.void", u"stop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        (obj).stop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK_register_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_register_Method, self).__init__(u"quark.void", u"register", _List([u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        (obj).register(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK_setDefaultTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_setDefaultTimeout_Method, self).__init__(u"quark.void", u"setDefaultTimeout", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        (obj).setDefaultTimeout(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK_session_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_session_Method, self).__init__(u"mdk.Session", u"session", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        return (obj).session()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK_join_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDK_join_Method, self).__init__(u"mdk.Session", u"join", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDK);
        return (obj).join(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDK(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_MDK, self).__init__(u"mdk.MDK");
        (self).name = u"mdk.MDK"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"CONTEXT_HEADER")])
        (self).methods = _List([mdk_MDK_start_Method(), mdk_MDK_stop_Method(), mdk_MDK_register_Method(), mdk_MDK_setDefaultTimeout_Method(), mdk_MDK_session_Method(), mdk_MDK_join_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_MDK.singleton = mdk_MDK()
class mdk_Session_inject_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_inject_Method, self).__init__(u"quark.String", u"inject", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).inject()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_externalize_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_externalize_Method, self).__init__(u"quark.String", u"externalize", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).externalize()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_critical_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_critical_Method, self).__init__(u"quark.void", u"critical", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).critical(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_error_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_error_Method, self).__init__(u"quark.void", u"error", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).error(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_warn_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_warn_Method, self).__init__(u"quark.void", u"warn", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).warn(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_info_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_info_Method, self).__init__(u"quark.void", u"info", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).info(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_debug_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_debug_Method, self).__init__(u"quark.void", u"debug", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).debug(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_trace_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_trace_Method, self).__init__(u"quark.void", u"trace", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).trace(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_route_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_route_Method, self).__init__(u"quark.void", u"route", _List([u"quark.String", u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).route(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode), _cast((args)[3], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_resolve_Method, self).__init__(u"mdk_discovery.Node", u"resolve", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).resolve(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_resolve_until_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_resolve_until_Method, self).__init__(u"mdk_discovery.Node", u"resolve_until", _List([u"quark.String", u"quark.String", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).resolve_until(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: float))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_resolve_async_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_resolve_async_Method, self).__init__(u"quark.Object", u"resolve_async", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).resolve_async(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_start_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_start_interaction_Method, self).__init__(u"quark.void", u"start_interaction", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).start_interaction();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_fail_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_fail_interaction_Method, self).__init__(u"quark.void", u"fail_interaction", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).fail_interaction(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_finish_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_finish_interaction_Method, self).__init__(u"quark.void", u"finish_interaction", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).finish_interaction();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_interact_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_interact_Method, self).__init__(u"quark.void", u"interact", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).interact(_cast((args)[0], lambda: quark.UnaryCallable));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_setTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_setTimeout_Method, self).__init__(u"quark.void", u"setTimeout", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        (obj).setTimeout(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session_getRemainingTime_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_Session_getRemainingTime_Method, self).__init__(u"quark.float", u"getRemainingTime", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.Session);
        return (obj).getRemainingTime()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_Session(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_Session, self).__init__(u"mdk.Session");
        (self).name = u"mdk.Session"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_Session_inject_Method(), mdk_Session_externalize_Method(), mdk_Session_critical_Method(), mdk_Session_error_Method(), mdk_Session_warn_Method(), mdk_Session_info_Method(), mdk_Session_debug_Method(), mdk_Session_trace_Method(), mdk_Session_route_Method(), mdk_Session_resolve_Method(), mdk_Session_resolve_until_Method(), mdk_Session_resolve_async_Method(), mdk_Session_start_interaction_Method(), mdk_Session_fail_interaction_Method(), mdk_Session_finish_interaction_Method(), mdk_Session_interact_Method(), mdk_Session_setTimeout_Method(), mdk_Session_getRemainingTime_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_Session.singleton = mdk_Session()
class mdk_MDKImpl_getDiscoveryFactory_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_getDiscoveryFactory_Method, self).__init__(u"mdk_discovery.DiscoverySourceFactory", u"getDiscoveryFactory", _List([u"mdk_runtime.EnvironmentVariables"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj).getDiscoveryFactory(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_getFailurePolicy_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_getFailurePolicy_Method, self).__init__(u"mdk_discovery.FailurePolicyFactory", u"getFailurePolicy", _List([u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj).getFailurePolicy(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_getWSClient_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_getWSClient_Method, self).__init__(u"mdk_protocol.WSClient", u"getWSClient", _List([u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj).getWSClient(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl__timeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl__timeout_Method, self).__init__(u"quark.float", u"_timeout", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj)._timeout()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_start_Method, self).__init__(u"quark.void", u"start", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        (obj).start();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_stop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_stop_Method, self).__init__(u"quark.void", u"stop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        (obj).stop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_register_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_register_Method, self).__init__(u"quark.void", u"register", _List([u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        (obj).register(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_setDefaultTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_setDefaultTimeout_Method, self).__init__(u"quark.void", u"setDefaultTimeout", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        (obj).setDefaultTimeout(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_session_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_session_Method, self).__init__(u"mdk.Session", u"session", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj).session()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl_join_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_MDKImpl_join_Method, self).__init__(u"mdk.Session", u"join", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.MDKImpl);
        return (obj).join(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_MDKImpl(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_MDKImpl, self).__init__(u"mdk.MDKImpl");
        (self).name = u"mdk.MDKImpl"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"CONTEXT_HEADER"), quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.Map<quark.String,quark.Object>", u"_reflection_hack"), quark.reflect.Field(u"mdk_runtime.MDKRuntime", u"_runtime"), quark.reflect.Field(u"mdk_protocol.WSClient", u"_wsclient"), quark.reflect.Field(u"mdk_protocol.OpenCloseSubscriber", u"_openclose"), quark.reflect.Field(u"mdk_discovery.Discovery", u"_disco"), quark.reflect.Field(u"mdk_discovery.DiscoverySource", u"_discoSource"), quark.reflect.Field(u"mdk_tracing.Tracer", u"_tracer"), quark.reflect.Field(u"quark.String", u"procUUID"), quark.reflect.Field(u"quark.bool", u"_running"), quark.reflect.Field(u"quark.float", u"_defaultTimeout")])
        (self).methods = _List([mdk_MDKImpl_getDiscoveryFactory_Method(), mdk_MDKImpl_getFailurePolicy_Method(), mdk_MDKImpl_getWSClient_Method(), mdk_MDKImpl__timeout_Method(), mdk_MDKImpl_start_Method(), mdk_MDKImpl_stop_Method(), mdk_MDKImpl_register_Method(), mdk_MDKImpl_setDefaultTimeout_Method(), mdk_MDKImpl_session_Method(), mdk_MDKImpl_join_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk.MDKImpl(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_MDKImpl.singleton = mdk_MDKImpl()
class mdk__TLSInit_getValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk__TLSInit_getValue_Method, self).__init__(u"quark.bool", u"getValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk._TLSInit);
        return (obj).getValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk__TLSInit(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk__TLSInit, self).__init__(u"mdk._TLSInit");
        (self).name = u"mdk._TLSInit"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk__TLSInit_getValue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk._TLSInit()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk__TLSInit.singleton = mdk__TLSInit()
class mdk_SessionImpl_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_get_Method, self).__init__(u"quark.Object", u"get", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).get(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_set_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_set_Method, self).__init__(u"quark.void", u"set", _List([u"quark.String", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).set(_cast((args)[0], lambda: unicode), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_has_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_has_Method, self).__init__(u"quark.bool", u"has", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).has(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_setTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_setTimeout_Method, self).__init__(u"quark.void", u"setTimeout", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).setTimeout(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_getRemainingTime_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_getRemainingTime_Method, self).__init__(u"quark.float", u"getRemainingTime", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).getRemainingTime()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_route_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_route_Method, self).__init__(u"quark.void", u"route", _List([u"quark.String", u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).route(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode), _cast((args)[3], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_trace_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_trace_Method, self).__init__(u"quark.void", u"trace", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).trace(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__level_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__level_Method, self).__init__(u"quark.int", u"_level", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return mdk.SessionImpl._level(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__enabled_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__enabled_Method, self).__init__(u"quark.bool", u"_enabled", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj)._enabled(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__log_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__log_Method, self).__init__(u"quark.void", u"_log", _List([u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj)._log(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_critical_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_critical_Method, self).__init__(u"quark.void", u"critical", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).critical(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_error_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_error_Method, self).__init__(u"quark.void", u"error", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).error(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_warn_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_warn_Method, self).__init__(u"quark.void", u"warn", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).warn(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_info_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_info_Method, self).__init__(u"quark.void", u"info", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).info(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_debug_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_debug_Method, self).__init__(u"quark.void", u"debug", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).debug(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__resolve_Method, self).__init__(u"mdk_runtime.promise.Promise", u"_resolve", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj)._resolve(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_resolve_async_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_resolve_async_Method, self).__init__(u"quark.Object", u"resolve_async", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).resolve_async(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_resolve_Method, self).__init__(u"mdk_discovery.Node", u"resolve", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).resolve(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_resolve_until_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_resolve_until_Method, self).__init__(u"mdk_discovery.Node", u"resolve_until", _List([u"quark.String", u"quark.String", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).resolve_until(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: float))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__resolvedCallback_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__resolvedCallback_Method, self).__init__(u"mdk_discovery.Node", u"_resolvedCallback", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj)._resolvedCallback(_cast((args)[0], lambda: mdk_discovery.Node))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl__current_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl__current_interaction_Method, self).__init__(u"quark.List<mdk_discovery.Node>", u"_current_interaction", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj)._current_interaction()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_start_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_start_interaction_Method, self).__init__(u"quark.void", u"start_interaction", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).start_interaction();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_inject_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_inject_Method, self).__init__(u"quark.String", u"inject", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).inject()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_externalize_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_externalize_Method, self).__init__(u"quark.String", u"externalize", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        return (obj).externalize()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_fail_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_fail_interaction_Method, self).__init__(u"quark.void", u"fail_interaction", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).fail_interaction(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_finish_interaction_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_finish_interaction_Method, self).__init__(u"quark.void", u"finish_interaction", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).finish_interaction();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl_interact_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_SessionImpl_interact_Method, self).__init__(u"quark.void", u"interact", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk.SessionImpl);
        (obj).interact(_cast((args)[0], lambda: quark.UnaryCallable));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_SessionImpl(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_SessionImpl, self).__init__(u"mdk.SessionImpl");
        (self).name = u"mdk.SessionImpl"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Map<quark.String,quark.int>", u"_levels"), quark.reflect.Field(u"quark.concurrent.TLS<quark.bool>", u"_inLogging"), quark.reflect.Field(u"mdk.MDKImpl", u"_mdk"), quark.reflect.Field(u"quark.List<quark.List<mdk_discovery.Node>>", u"_resolved"), quark.reflect.Field(u"mdk_protocol.SharedContext", u"_context"), quark.reflect.Field(u"quark.bool", u"_experimental")])
        (self).methods = _List([mdk_SessionImpl_get_Method(), mdk_SessionImpl_set_Method(), mdk_SessionImpl_has_Method(), mdk_SessionImpl_setTimeout_Method(), mdk_SessionImpl_getRemainingTime_Method(), mdk_SessionImpl_route_Method(), mdk_SessionImpl_trace_Method(), mdk_SessionImpl__level_Method(), mdk_SessionImpl__enabled_Method(), mdk_SessionImpl__log_Method(), mdk_SessionImpl_critical_Method(), mdk_SessionImpl_error_Method(), mdk_SessionImpl_warn_Method(), mdk_SessionImpl_info_Method(), mdk_SessionImpl_debug_Method(), mdk_SessionImpl__resolve_Method(), mdk_SessionImpl_resolve_async_Method(), mdk_SessionImpl_resolve_Method(), mdk_SessionImpl_resolve_until_Method(), mdk_SessionImpl__resolvedCallback_Method(), mdk_SessionImpl__current_interaction_Method(), mdk_SessionImpl_start_interaction_Method(), mdk_SessionImpl_inject_Method(), mdk_SessionImpl_externalize_Method(), mdk_SessionImpl_fail_interaction_Method(), mdk_SessionImpl_finish_interaction_Method(), mdk_SessionImpl_interact_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk.SessionImpl(_cast((args)[0], lambda: mdk.MDKImpl), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_SessionImpl.singleton = mdk_SessionImpl()
class quark_Task(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Task, self).__init__(u"quark.Task");
        (self).name = u"quark.Task"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Task.singleton = quark_Task()
class quark_Runtime(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Runtime, self).__init__(u"quark.Runtime");
        (self).name = u"quark.Runtime"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Runtime.singleton = quark_Runtime()
class quark_Maybe_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Maybe_quark_Object_, self).__init__(u"quark.Maybe<quark.Object>");
        (self).name = u"quark.Maybe"
        (self).parameters = _List([u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Maybe_quark_Object_.singleton = quark_Maybe_quark_Object_()
class quark_ParsedNumber_quark_int_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ParsedNumber_quark_int_, self).__init__(u"quark.ParsedNumber<quark.int>");
        (self).name = u"quark.ParsedNumber"
        (self).parameters = _List([u"quark.int"])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"MINUS"), quark.reflect.Field(u"quark.int", u"PLUS"), quark.reflect.Field(u"quark.int", u"ZERO"), quark.reflect.Field(u"quark.int", u"NINE"), quark.reflect.Field(u"quark.int", u"_value"), quark.reflect.Field(u"quark.bool", u"_hasValue")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ParsedNumber()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ParsedNumber_quark_int_.singleton = quark_ParsedNumber_quark_int_()
class quark_ParsedNumber_quark_long_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ParsedNumber_quark_long_, self).__init__(u"quark.ParsedNumber<quark.long>");
        (self).name = u"quark.ParsedNumber"
        (self).parameters = _List([u"quark.long"])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"MINUS"), quark.reflect.Field(u"quark.int", u"PLUS"), quark.reflect.Field(u"quark.int", u"ZERO"), quark.reflect.Field(u"quark.int", u"NINE"), quark.reflect.Field(u"quark.long", u"_value"), quark.reflect.Field(u"quark.bool", u"_hasValue")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ParsedNumber()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ParsedNumber_quark_long_.singleton = quark_ParsedNumber_quark_long_()
class quark_ParsedInt(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ParsedInt, self).__init__(u"quark.ParsedInt");
        (self).name = u"quark.ParsedInt"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"MINUS"), quark.reflect.Field(u"quark.int", u"PLUS"), quark.reflect.Field(u"quark.int", u"ZERO"), quark.reflect.Field(u"quark.int", u"NINE"), quark.reflect.Field(u"quark.int", u"_value"), quark.reflect.Field(u"quark.bool", u"_hasValue"), quark.reflect.Field(u"quark.int", u"MIN"), quark.reflect.Field(u"quark.int", u"MAX")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ParsedInt(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ParsedInt.singleton = quark_ParsedInt()
class quark_ParsedLong(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ParsedLong, self).__init__(u"quark.ParsedLong");
        (self).name = u"quark.ParsedLong"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"MINUS"), quark.reflect.Field(u"quark.int", u"PLUS"), quark.reflect.Field(u"quark.int", u"ZERO"), quark.reflect.Field(u"quark.int", u"NINE"), quark.reflect.Field(u"quark.long", u"_value"), quark.reflect.Field(u"quark.bool", u"_hasValue")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ParsedLong(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ParsedLong.singleton = quark_ParsedLong()
class quark_ListUtil_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ListUtil_quark_Object_, self).__init__(u"quark.ListUtil<quark.Object>");
        (self).name = u"quark.ListUtil"
        (self).parameters = _List([u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ListUtil()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ListUtil_quark_Object_.singleton = quark_ListUtil_quark_Object_()
class quark_ListUtil_mdk_discovery_Node_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ListUtil_mdk_discovery_Node_, self).__init__(u"quark.ListUtil<mdk_discovery.Node>");
        (self).name = u"quark.ListUtil"
        (self).parameters = _List([u"mdk_discovery.Node"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ListUtil()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ListUtil_mdk_discovery_Node_.singleton = quark_ListUtil_mdk_discovery_Node_()
class quark_List_quark_List_mdk_discovery_Node__(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_List_mdk_discovery_Node__, self).__init__(u"quark.List<quark.List<mdk_discovery.Node>>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.List<mdk_discovery.Node>"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_List_mdk_discovery_Node__.singleton = quark_List_quark_List_mdk_discovery_Node__()
class quark_List_mdk_discovery_Node_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_discovery_Node_, self).__init__(u"quark.List<mdk_discovery.Node>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_discovery.Node"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_discovery_Node_.singleton = quark_List_mdk_discovery_Node_()
class quark_List_quark_Map_quark_String_quark_String__(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_Map_quark_String_quark_String__, self).__init__(u"quark.List<quark.Map<quark.String,quark.String>>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.Map<quark.String,quark.String>"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_Map_quark_String_quark_String__.singleton = quark_List_quark_Map_quark_String_quark_String__()
class quark_List_quark_String_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_String_, self).__init__(u"quark.List<quark.String>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.String"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_String_.singleton = quark_List_quark_String_()
class quark_List_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_Object_, self).__init__(u"quark.List<quark.Object>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_Object_.singleton = quark_List_quark_Object_()
class quark_List_quark_reflect_Field_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_reflect_Field_, self).__init__(u"quark.List<quark.reflect.Field>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.reflect.Field"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_reflect_Field_.singleton = quark_List_quark_reflect_Field_()
class quark_List_quark_reflect_Method_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_reflect_Method_, self).__init__(u"quark.List<quark.reflect.Method>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.reflect.Method"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_reflect_Method_.singleton = quark_List_quark_reflect_Method_()
class quark_List_quark_reflect_Class_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_reflect_Class_, self).__init__(u"quark.List<quark.reflect.Class>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.reflect.Class"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_reflect_Class_.singleton = quark_List_quark_reflect_Class_()
class quark_List_quark_concurrent_FutureCompletion_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_concurrent_FutureCompletion_, self).__init__(u"quark.List<quark.concurrent.FutureCompletion>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.concurrent.FutureCompletion"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_concurrent_FutureCompletion_.singleton = quark_List_quark_concurrent_FutureCompletion_()
class quark_List_quark_test_Test_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_test_Test_, self).__init__(u"quark.List<quark.test.Test>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.test.Test"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_test_Test_.singleton = quark_List_quark_test_Test_()
class quark_List_quark_mock_MockMessage_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_mock_MockMessage_, self).__init__(u"quark.List<quark.mock.MockMessage>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.mock.MockMessage"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_mock_MockMessage_.singleton = quark_List_quark_mock_MockMessage_()
class quark_List_quark_mock_MockEvent_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_mock_MockEvent_, self).__init__(u"quark.List<quark.mock.MockEvent>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.mock.MockEvent"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_mock_MockEvent_.singleton = quark_List_quark_mock_MockEvent_()
class quark_List_quark_mock_MockTask_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_mock_MockTask_, self).__init__(u"quark.List<quark.mock.MockTask>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.mock.MockTask"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_mock_MockTask_.singleton = quark_List_quark_mock_MockTask_()
class quark_List_quark_bool_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_bool_, self).__init__(u"quark.List<quark.bool>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.bool"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_bool_.singleton = quark_List_quark_bool_()
class quark_List_quark__Callback_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark__Callback_, self).__init__(u"quark.List<quark._Callback>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark._Callback"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark__Callback_.singleton = quark_List_quark__Callback_()
class quark_List_mdk_runtime_WSActor_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_WSActor_, self).__init__(u"quark.List<mdk_runtime.WSActor>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.WSActor"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_WSActor_.singleton = quark_List_mdk_runtime_WSActor_()
class quark_List_mdk_runtime_FakeWSActor_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_FakeWSActor_, self).__init__(u"quark.List<mdk_runtime.FakeWSActor>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.FakeWSActor"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_FakeWSActor_.singleton = quark_List_mdk_runtime_FakeWSActor_()
class quark_List_quark_long_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_long_, self).__init__(u"quark.List<quark.long>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.long"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_long_.singleton = quark_List_quark_long_()
class quark_List_mdk_runtime_actors__QueuedMessage_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_actors__QueuedMessage_, self).__init__(u"quark.List<mdk_runtime.actors._QueuedMessage>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.actors._QueuedMessage"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_actors__QueuedMessage_.singleton = quark_List_mdk_runtime_actors__QueuedMessage_()
class quark_List_mdk_runtime_promise__Callback_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_promise__Callback_, self).__init__(u"quark.List<mdk_runtime.promise._Callback>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.promise._Callback"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_promise__Callback_.singleton = quark_List_mdk_runtime_promise__Callback_()
class quark_List_mdk_runtime_files__Subscription_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_files__Subscription_, self).__init__(u"quark.List<mdk_runtime.files._Subscription>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.files._Subscription"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_files__Subscription_.singleton = quark_List_mdk_runtime_files__Subscription_()
class quark_List_mdk_discovery__Request_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_discovery__Request_, self).__init__(u"quark.List<mdk_discovery._Request>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_discovery._Request"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_discovery__Request_.singleton = quark_List_mdk_discovery__Request_()
class quark_List_quark_int_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_quark_int_, self).__init__(u"quark.List<quark.int>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"quark.int"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_quark_int_.singleton = quark_List_quark_int_()
class quark_List_mdk_runtime_actors_Actor_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_runtime_actors_Actor_, self).__init__(u"quark.List<mdk_runtime.actors.Actor>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_runtime.actors.Actor"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_runtime_actors_Actor_.singleton = quark_List_mdk_runtime_actors_Actor_()
class quark_List_mdk_tracing_protocol_LogEvent_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_List_mdk_tracing_protocol_LogEvent_, self).__init__(u"quark.List<mdk_tracing.protocol.LogEvent>");
        (self).name = u"quark.List"
        (self).parameters = _List([u"mdk_tracing.protocol.LogEvent"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _List()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_List_mdk_tracing_protocol_LogEvent_.singleton = quark_List_mdk_tracing_protocol_LogEvent_()
class quark_Map_quark_String_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_Object_, self).__init__(u"quark.Map<quark.String,quark.Object>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_Object_.singleton = quark_Map_quark_String_quark_Object_()
class quark_Map_quark_String_quark_int_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_int_, self).__init__(u"quark.Map<quark.String,quark.int>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.int"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_int_.singleton = quark_Map_quark_String_quark_int_()
class quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String___(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String___, self).__init__(u"quark.Map<quark.String,quark.List<quark.Map<quark.String,quark.String>>>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.List<quark.Map<quark.String,quark.String>>"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String___.singleton = quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String___()
class quark_Map_quark_String_quark_String_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_String_, self).__init__(u"quark.Map<quark.String,quark.String>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.String"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_String_.singleton = quark_Map_quark_String_quark_String_()
class quark_Map_quark_Object_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_Object_quark_Object_, self).__init__(u"quark.Map<quark.Object,quark.Object>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.Object", u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_Object_quark_Object_.singleton = quark_Map_quark_Object_quark_Object_()
class quark_Map_quark_String_quark_reflect_Class_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_reflect_Class_, self).__init__(u"quark.Map<quark.String,quark.reflect.Class>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.reflect.Class"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_reflect_Class_.singleton = quark_Map_quark_String_quark_reflect_Class_()
class quark_Map_quark_String_quark_ServiceInstance_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_ServiceInstance_, self).__init__(u"quark.Map<quark.String,quark.ServiceInstance>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.ServiceInstance"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_ServiceInstance_.singleton = quark_Map_quark_String_quark_ServiceInstance_()
class quark_Map_quark_String_quark_mock_SocketEvent_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_quark_mock_SocketEvent_, self).__init__(u"quark.Map<quark.String,quark.mock.SocketEvent>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"quark.mock.SocketEvent"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_quark_mock_SocketEvent_.singleton = quark_Map_quark_String_quark_mock_SocketEvent_()
class quark_Map_quark_long_mdk_runtime__FakeTimeRequest_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_long_mdk_runtime__FakeTimeRequest_, self).__init__(u"quark.Map<quark.long,mdk_runtime._FakeTimeRequest>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.long", u"mdk_runtime._FakeTimeRequest"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_long_mdk_runtime__FakeTimeRequest_.singleton = quark_Map_quark_long_mdk_runtime__FakeTimeRequest_()
class quark_Map_quark_String_mdk_discovery_FailurePolicy_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_mdk_discovery_FailurePolicy_, self).__init__(u"quark.Map<quark.String,mdk_discovery.FailurePolicy>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"mdk_discovery.FailurePolicy"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_mdk_discovery_FailurePolicy_.singleton = quark_Map_quark_String_mdk_discovery_FailurePolicy_()
class quark_Map_quark_String_mdk_discovery_Cluster_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Map_quark_String_mdk_discovery_Cluster_, self).__init__(u"quark.Map<quark.String,mdk_discovery.Cluster>");
        (self).name = u"quark.Map"
        (self).parameters = _List([u"quark.String", u"mdk_discovery.Cluster"])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return _Map()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Map_quark_String_mdk_discovery_Cluster_.singleton = quark_Map_quark_String_mdk_discovery_Cluster_()
class quark_UnaryCallable(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_UnaryCallable, self).__init__(u"quark.UnaryCallable");
        (self).name = u"quark.UnaryCallable"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_UnaryCallable.singleton = quark_UnaryCallable()
class quark_error_Error_getMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_error_Error_getMessage_Method, self).__init__(u"quark.String", u"getMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.error.Error);
        return (obj).getMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_error_Error_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_error_Error_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.error.Error);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_error_Error(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_error_Error, self).__init__(u"quark.error.Error");
        (self).name = u"quark.error.Error"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([quark_error_Error_getMessage_Method(), quark_error_Error_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.error.Error(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_error_Error.singleton = quark_error_Error()
class quark_logging_Appender(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_logging_Appender, self).__init__(u"quark.logging.Appender");
        (self).name = u"quark.logging.Appender"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"name")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.logging.Appender(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_logging_Appender.singleton = quark_logging_Appender()
class quark_logging_Config_setAppender_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_logging_Config_setAppender_Method, self).__init__(u"quark.logging.Config", u"setAppender", _List([u"quark.logging.Appender"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.logging.Config);
        return (obj).setAppender(_cast((args)[0], lambda: quark.logging.Appender))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_logging_Config_setLevel_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_logging_Config_setLevel_Method, self).__init__(u"quark.logging.Config", u"setLevel", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.logging.Config);
        return (obj).setLevel(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_logging_Config__getOverrideIfExists_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_logging_Config__getOverrideIfExists_Method, self).__init__(u"quark.String", u"_getOverrideIfExists", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.logging.Config);
        return quark.logging.Config._getOverrideIfExists()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_logging_Config__autoconfig_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_logging_Config__autoconfig_Method, self).__init__(u"quark.bool", u"_autoconfig", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.logging.Config);
        return quark.logging.Config._autoconfig()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_logging_Config_configure_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_logging_Config_configure_Method, self).__init__(u"quark.void", u"configure", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.logging.Config);
        (obj).configure();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_logging_Config(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_logging_Config, self).__init__(u"quark.logging.Config");
        (self).name = u"quark.logging.Config"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_overrideEnvVar"), quark.reflect.Field(u"quark.String", u"_overrideLevel"), quark.reflect.Field(u"quark.bool", u"_configured"), quark.reflect.Field(u"quark.logging.Appender", u"appender"), quark.reflect.Field(u"quark.String", u"level")])
        (self).methods = _List([quark_logging_Config_setAppender_Method(), quark_logging_Config_setLevel_Method(), quark_logging_Config__getOverrideIfExists_Method(), quark_logging_Config__autoconfig_Method(), quark_logging_Config_configure_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.logging.Config()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_logging_Config.singleton = quark_logging_Config()
class quark_reflect_Class(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_reflect_Class, self).__init__(u"quark.reflect.Class");
        (self).name = u"quark.reflect.Class"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Map<quark.String,quark.reflect.Class>", u"classes"), quark.reflect.Field(u"quark.reflect.Class", u"VOID"), quark.reflect.Field(u"quark.reflect.Class", u"BOOL"), quark.reflect.Field(u"quark.reflect.Class", u"INT"), quark.reflect.Field(u"quark.reflect.Class", u"LONG"), quark.reflect.Field(u"quark.reflect.Class", u"FLOAT"), quark.reflect.Field(u"quark.reflect.Class", u"STRING"), quark.reflect.Field(u"quark.reflect.Class", u"OBJECT"), quark.reflect.Field(u"quark.reflect.Class", u"ERROR"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.String", u"name"), quark.reflect.Field(u"quark.List<quark.String>", u"parameters"), quark.reflect.Field(u"quark.List<quark.reflect.Field>", u"fields"), quark.reflect.Field(u"quark.List<quark.reflect.Method>", u"methods"), quark.reflect.Field(u"quark.List<quark.String>", u"parents")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.reflect.Class(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_reflect_Class.singleton = quark_reflect_Class()
class quark_reflect_Field(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_reflect_Field, self).__init__(u"quark.reflect.Field");
        (self).name = u"quark.reflect.Field"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"type"), quark.reflect.Field(u"quark.String", u"name")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.reflect.Field(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_reflect_Field.singleton = quark_reflect_Field()
class quark_reflect_Method(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_reflect_Method, self).__init__(u"quark.reflect.Method");
        (self).name = u"quark.reflect.Method"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"type"), quark.reflect.Field(u"quark.String", u"name"), quark.reflect.Field(u"quark.List<quark.String>", u"parameters")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_reflect_Method.singleton = quark_reflect_Method()
class quark_ServletError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ServletError, self).__init__(u"quark.ServletError");
        (self).name = u"quark.ServletError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return quark.ServletError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ServletError.singleton = quark_ServletError()
class quark_Servlet(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Servlet, self).__init__(u"quark.Servlet");
        (self).name = u"quark.Servlet"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Servlet.singleton = quark_Servlet()
class quark_Resolver(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Resolver, self).__init__(u"quark.Resolver");
        (self).name = u"quark.Resolver"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Resolver.singleton = quark_Resolver()
class quark_ResponseHolder(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ResponseHolder, self).__init__(u"quark.ResponseHolder");
        (self).name = u"quark.ResponseHolder"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.HTTPResponse", u"response"), quark.reflect.Field(u"quark.HTTPError", u"failure")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ResponseHolder()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ResponseHolder.singleton = quark_ResponseHolder()
class quark_Service(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Service, self).__init__(u"quark.Service");
        (self).name = u"quark.Service"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Service.singleton = quark_Service()
class quark_BaseService(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_BaseService, self).__init__(u"quark.BaseService");
        (self).name = u"quark.BaseService"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.BaseService()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_BaseService.singleton = quark_BaseService()
class quark_ServiceInstance(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ServiceInstance, self).__init__(u"quark.ServiceInstance");
        (self).name = u"quark.ServiceInstance"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"serviceName"), quark.reflect.Field(u"quark.String", u"url"), quark.reflect.Field(u"quark.behaviors.CircuitBreaker", u"breaker")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ServiceInstance(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: int), _cast((args)[3], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ServiceInstance.singleton = quark_ServiceInstance()
class quark_DegenerateResolver(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_DegenerateResolver, self).__init__(u"quark.DegenerateResolver");
        (self).name = u"quark.DegenerateResolver"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.DegenerateResolver()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_DegenerateResolver.singleton = quark_DegenerateResolver()
class quark_Client(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Client, self).__init__(u"quark.Client");
        (self).name = u"quark.Client"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.Resolver", u"resolver"), quark.reflect.Field(u"quark.String", u"serviceName"), quark.reflect.Field(u"quark.float", u"_timeout"), quark.reflect.Field(u"quark.int", u"_failureLimit"), quark.reflect.Field(u"quark.float", u"_retestDelay"), quark.reflect.Field(u"quark.concurrent.Lock", u"mutex"), quark.reflect.Field(u"quark.Map<quark.String,quark.ServiceInstance>", u"instanceMap"), quark.reflect.Field(u"quark.int", u"counter")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.Client(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Client.singleton = quark_Client()
class quark_ServerResponder(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_ServerResponder, self).__init__(u"quark.ServerResponder");
        (self).name = u"quark.ServerResponder"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.bool", u"sendCORS"), quark.reflect.Field(u"quark.HTTPRequest", u"request"), quark.reflect.Field(u"quark.HTTPResponse", u"response")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.ServerResponder(_cast((args)[0], lambda: bool), _cast((args)[1], lambda: quark.HTTPRequest), _cast((args)[2], lambda: quark.HTTPResponse))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_ServerResponder.singleton = quark_ServerResponder()
class quark_Server_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Server_quark_Object_, self).__init__(u"quark.Server<quark.Object>");
        (self).name = u"quark.Server"
        (self).parameters = _List([u"quark.Object"])
        (self).fields = _List([quark.reflect.Field(u"quark.Object", u"impl"), quark.reflect.Field(u"quark.bool", u"_sendCORS")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.Server((args)[0])

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Server_quark_Object_.singleton = quark_Server_quark_Object_()
class quark_behaviors_RPCError_getMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCError_getMessage_Method, self).__init__(u"quark.String", u"getMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCError);
        return (obj).getMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCError_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCError_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCError);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_behaviors_RPCError, self).__init__(u"quark.behaviors.RPCError");
        (self).name = u"quark.behaviors.RPCError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([quark_behaviors_RPCError_getMessage_Method(), quark_behaviors_RPCError_toString_Method()])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return quark.behaviors.RPCError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_behaviors_RPCError.singleton = quark_behaviors_RPCError()
class quark_behaviors_RPC_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPC_call_Method, self).__init__(u"quark.concurrent.Future", u"call", _List([u"quark.List<quark.Object>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPC);
        return (obj).call(_cast((args)[0], lambda: _List))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPC_succeed_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPC_succeed_Method, self).__init__(u"quark.void", u"succeed", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPC);
        (obj).succeed(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPC_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPC_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPC);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPC_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPC_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPC);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPC(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_behaviors_RPC, self).__init__(u"quark.behaviors.RPC");
        (self).name = u"quark.behaviors.RPC"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Service", u"service"), quark.reflect.Field(u"quark.reflect.Class", u"returned"), quark.reflect.Field(u"quark.float", u"timeout"), quark.reflect.Field(u"quark.String", u"methodName"), quark.reflect.Field(u"quark.ServiceInstance", u"instance")])
        (self).methods = _List([quark_behaviors_RPC_call_Method(), quark_behaviors_RPC_succeed_Method(), quark_behaviors_RPC_fail_Method(), quark_behaviors_RPC_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.behaviors.RPC(_cast((args)[0], lambda: quark.Service), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_behaviors_RPC.singleton = quark_behaviors_RPC()
class quark_behaviors_RPCRequest_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_call_Method, self).__init__(u"quark.concurrent.Future", u"call", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        return (obj).call(_cast((args)[0], lambda: quark.HTTPRequest))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest_onHTTPResponse_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_onHTTPResponse_Method, self).__init__(u"quark.void", u"onHTTPResponse", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        (obj).onHTTPResponse(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest_onTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_onTimeout_Method, self).__init__(u"quark.void", u"onTimeout", _List([u"quark.concurrent.Timeout"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        (obj).onTimeout(_cast((args)[0], lambda: quark.concurrent.Timeout));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest_onHTTPInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_onHTTPInit_Method, self).__init__(u"quark.void", u"onHTTPInit", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        (obj).onHTTPInit(_cast((args)[0], lambda: quark.HTTPRequest));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest_onHTTPError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_onHTTPError_Method, self).__init__(u"quark.void", u"onHTTPError", _List([u"quark.HTTPRequest", u"quark.HTTPError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        (obj).onHTTPError(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest_onHTTPFinal_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest_onHTTPFinal_Method, self).__init__(u"quark.void", u"onHTTPFinal", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.RPCRequest);
        (obj).onHTTPFinal(_cast((args)[0], lambda: quark.HTTPRequest));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_RPCRequest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_behaviors_RPCRequest, self).__init__(u"quark.behaviors.RPCRequest");
        (self).name = u"quark.behaviors.RPCRequest"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.behaviors.RPC", u"rpc"), quark.reflect.Field(u"quark.concurrent.Future", u"retval"), quark.reflect.Field(u"quark.List<quark.Object>", u"args"), quark.reflect.Field(u"quark.concurrent.Timeout", u"timeout")])
        (self).methods = _List([quark_behaviors_RPCRequest_call_Method(), quark_behaviors_RPCRequest_onHTTPResponse_Method(), quark_behaviors_RPCRequest_onTimeout_Method(), quark_behaviors_RPCRequest_onHTTPInit_Method(), quark_behaviors_RPCRequest_onHTTPError_Method(), quark_behaviors_RPCRequest_onHTTPFinal_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.behaviors.RPCRequest(_cast((args)[0], lambda: _List), _cast((args)[1], lambda: quark.behaviors.RPC))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_behaviors_RPCRequest.singleton = quark_behaviors_RPCRequest()
class quark_behaviors_CircuitBreaker_succeed_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_CircuitBreaker_succeed_Method, self).__init__(u"quark.void", u"succeed", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.CircuitBreaker);
        (obj).succeed();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_CircuitBreaker_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_CircuitBreaker_fail_Method, self).__init__(u"quark.void", u"fail", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.CircuitBreaker);
        (obj).fail();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_CircuitBreaker_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_behaviors_CircuitBreaker_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.behaviors.CircuitBreaker);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_behaviors_CircuitBreaker(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_behaviors_CircuitBreaker, self).__init__(u"quark.behaviors.CircuitBreaker");
        (self).name = u"quark.behaviors.CircuitBreaker"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.int", u"failureLimit"), quark.reflect.Field(u"quark.float", u"retestDelay"), quark.reflect.Field(u"quark.bool", u"active"), quark.reflect.Field(u"quark.int", u"failureCount"), quark.reflect.Field(u"quark.concurrent.Lock", u"mutex")])
        (self).methods = _List([quark_behaviors_CircuitBreaker_succeed_Method(), quark_behaviors_CircuitBreaker_fail_Method(), quark_behaviors_CircuitBreaker_onExecute_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.behaviors.CircuitBreaker(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: int), _cast((args)[2], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_behaviors_CircuitBreaker.singleton = quark_behaviors_CircuitBreaker()
class quark_concurrent_Event_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Event_getContext_Method, self).__init__(u"quark.concurrent.EventContext", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Event);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Event_fireEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Event_fireEvent_Method, self).__init__(u"quark.void", u"fireEvent", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Event);
        (obj).fireEvent();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Event(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Event, self).__init__(u"quark.concurrent.Event");
        (self).name = u"quark.concurrent.Event"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_concurrent_Event_getContext_Method(), quark_concurrent_Event_fireEvent_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Event.singleton = quark_concurrent_Event()
class quark_concurrent_FutureListener_onFuture_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureListener_onFuture_Method, self).__init__(u"quark.void", u"onFuture", _List([u"quark.concurrent.Future"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureListener);
        (obj).onFuture(_cast((args)[0], lambda: quark.concurrent.Future));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureListener(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_FutureListener, self).__init__(u"quark.concurrent.FutureListener");
        (self).name = u"quark.concurrent.FutureListener"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_concurrent_FutureListener_onFuture_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_FutureListener.singleton = quark_concurrent_FutureListener()
class quark_concurrent_FutureCompletion_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureCompletion_getContext_Method, self).__init__(u"quark.concurrent.EventContext", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureCompletion);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureCompletion_fireEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureCompletion_fireEvent_Method, self).__init__(u"quark.void", u"fireEvent", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureCompletion);
        (obj).fireEvent();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureCompletion(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_FutureCompletion, self).__init__(u"quark.concurrent.FutureCompletion");
        (self).name = u"quark.concurrent.FutureCompletion"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Future", u"future"), quark.reflect.Field(u"quark.concurrent.FutureListener", u"listener")])
        (self).methods = _List([quark_concurrent_FutureCompletion_getContext_Method(), quark_concurrent_FutureCompletion_fireEvent_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.FutureCompletion(_cast((args)[0], lambda: quark.concurrent.Future), _cast((args)[1], lambda: quark.concurrent.FutureListener))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_FutureCompletion.singleton = quark_concurrent_FutureCompletion()
class quark_concurrent_EventContext_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_EventContext_getContext_Method, self).__init__(u"quark.concurrent.Context", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.EventContext);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_EventContext(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_EventContext, self).__init__(u"quark.concurrent.EventContext");
        (self).name = u"quark.concurrent.EventContext"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_context")])
        (self).methods = _List([quark_concurrent_EventContext_getContext_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.EventContext()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_EventContext.singleton = quark_concurrent_EventContext()
class quark_concurrent_Future_onFinished_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_onFinished_Method, self).__init__(u"quark.void", u"onFinished", _List([u"quark.concurrent.FutureListener"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        (obj).onFinished(_cast((args)[0], lambda: quark.concurrent.FutureListener));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future_finish_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_finish_Method, self).__init__(u"quark.void", u"finish", _List([u"quark.error.Error"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        (obj).finish(_cast((args)[0], lambda: quark.error.Error));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future_isFinished_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_isFinished_Method, self).__init__(u"quark.bool", u"isFinished", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        return (obj).isFinished()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future_getError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_getError_Method, self).__init__(u"quark.error.Error", u"getError", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        return (obj).getError()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future_await_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_await_Method, self).__init__(u"quark.void", u"await", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        (obj).await(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Future_getContext_Method, self).__init__(u"quark.concurrent.Context", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Future);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Future(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Future, self).__init__(u"quark.concurrent.Future");
        (self).name = u"quark.concurrent.Future"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_context"), quark.reflect.Field(u"quark.bool", u"_finished"), quark.reflect.Field(u"quark.error.Error", u"_error"), quark.reflect.Field(u"quark.List<quark.concurrent.FutureCompletion>", u"_callbacks"), quark.reflect.Field(u"quark.concurrent.Lock", u"_lock")])
        (self).methods = _List([quark_concurrent_Future_onFinished_Method(), quark_concurrent_Future_finish_Method(), quark_concurrent_Future_isFinished_Method(), quark_concurrent_Future_getError_Method(), quark_concurrent_Future_await_Method(), quark_concurrent_Future_getContext_Method()])
        (self).parents = _List([u"quark.concurrent.EventContext"])

    def construct(self, args):
        return quark.concurrent.Future()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Future.singleton = quark_concurrent_Future()
class quark_concurrent_FutureWait_wait_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureWait_wait_Method, self).__init__(u"quark.void", u"wait", _List([u"quark.concurrent.Future", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureWait);
        (obj).wait(_cast((args)[0], lambda: quark.concurrent.Future), _cast((args)[1], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureWait_onFuture_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureWait_onFuture_Method, self).__init__(u"quark.void", u"onFuture", _List([u"quark.concurrent.Future"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureWait);
        (obj).onFuture(_cast((args)[0], lambda: quark.concurrent.Future));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureWait_waitFor_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_FutureWait_waitFor_Method, self).__init__(u"quark.concurrent.Future", u"waitFor", _List([u"quark.concurrent.Future", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.FutureWait);
        return quark.concurrent.FutureWait.waitFor(_cast((args)[0], lambda: quark.concurrent.Future), _cast((args)[1], lambda: float))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_FutureWait(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_FutureWait, self).__init__(u"quark.concurrent.FutureWait");
        (self).name = u"quark.concurrent.FutureWait"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Condition", u"_lock"), quark.reflect.Field(u"quark.concurrent.Future", u"_future")])
        (self).methods = _List([quark_concurrent_FutureWait_wait_Method(), quark_concurrent_FutureWait_onFuture_Method(), quark_concurrent_FutureWait_waitFor_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.FutureWait()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_FutureWait.singleton = quark_concurrent_FutureWait()
class quark_concurrent_Queue_quark_concurrent_Event__put_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Queue_quark_concurrent_Event__put_Method, self).__init__(u"quark.void", u"put", _List([u"quark.concurrent.Event"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Queue);
        (obj).put(_cast((args)[0], lambda: quark.concurrent.Event));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Queue_quark_concurrent_Event__get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Queue_quark_concurrent_Event__get_Method, self).__init__(u"quark.concurrent.Event", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Queue);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Queue_quark_concurrent_Event__size_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Queue_quark_concurrent_Event__size_Method, self).__init__(u"quark.int", u"size", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Queue);
        return (obj).size()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Queue_quark_concurrent_Event_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Queue_quark_concurrent_Event_, self).__init__(u"quark.concurrent.Queue<quark.concurrent.Event>");
        (self).name = u"quark.concurrent.Queue"
        (self).parameters = _List([u"quark.concurrent.Event"])
        (self).fields = _List([quark.reflect.Field(u"quark.List<quark.Object>", u"items"), quark.reflect.Field(u"quark.int", u"head"), quark.reflect.Field(u"quark.int", u"tail")])
        (self).methods = _List([quark_concurrent_Queue_quark_concurrent_Event__put_Method(), quark_concurrent_Queue_quark_concurrent_Event__get_Method(), quark_concurrent_Queue_quark_concurrent_Event__size_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.Queue()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Queue_quark_concurrent_Event_.singleton = quark_concurrent_Queue_quark_concurrent_Event_()
class quark_concurrent_CollectorExecutor__start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_CollectorExecutor__start_Method, self).__init__(u"quark.void", u"_start", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.CollectorExecutor);
        (obj)._start();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_CollectorExecutor_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_CollectorExecutor_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.CollectorExecutor);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_CollectorExecutor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_CollectorExecutor, self).__init__(u"quark.concurrent.CollectorExecutor");
        (self).name = u"quark.concurrent.CollectorExecutor"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Queue<quark.concurrent.Event>", u"events"), quark.reflect.Field(u"quark.concurrent.Collector", u"collector")])
        (self).methods = _List([quark_concurrent_CollectorExecutor__start_Method(), quark_concurrent_CollectorExecutor_onExecute_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.CollectorExecutor(_cast((args)[0], lambda: quark.concurrent.Collector))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_CollectorExecutor.singleton = quark_concurrent_CollectorExecutor()
class quark_concurrent_Collector_put_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Collector_put_Method, self).__init__(u"quark.void", u"put", _List([u"quark.concurrent.Event"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Collector);
        (obj).put(_cast((args)[0], lambda: quark.concurrent.Event));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Collector__swap_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Collector__swap_Method, self).__init__(u"quark.concurrent.Queue<quark.concurrent.Event>", u"_swap", _List([u"quark.concurrent.Queue<quark.concurrent.Event>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Collector);
        return (obj)._swap(_cast((args)[0], lambda: quark.concurrent.Queue))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Collector__poll_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Collector__poll_Method, self).__init__(u"quark.void", u"_poll", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Collector);
        (obj)._poll();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Collector(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Collector, self).__init__(u"quark.concurrent.Collector");
        (self).name = u"quark.concurrent.Collector"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Lock", u"lock"), quark.reflect.Field(u"quark.concurrent.Queue<quark.concurrent.Event>", u"pending"), quark.reflect.Field(u"quark.concurrent.CollectorExecutor", u"executor"), quark.reflect.Field(u"quark.bool", u"idle")])
        (self).methods = _List([quark_concurrent_Collector_put_Method(), quark_concurrent_Collector__swap_Method(), quark_concurrent_Collector__poll_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.Collector()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Collector.singleton = quark_concurrent_Collector()
class quark_concurrent_TimeoutListener_onTimeout_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_TimeoutListener_onTimeout_Method, self).__init__(u"quark.void", u"onTimeout", _List([u"quark.concurrent.Timeout"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.TimeoutListener);
        (obj).onTimeout(_cast((args)[0], lambda: quark.concurrent.Timeout));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_TimeoutListener(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_TimeoutListener, self).__init__(u"quark.concurrent.TimeoutListener");
        (self).name = u"quark.concurrent.TimeoutListener"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_concurrent_TimeoutListener_onTimeout_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_TimeoutListener.singleton = quark_concurrent_TimeoutListener()
class quark_concurrent_TimeoutExpiry_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_TimeoutExpiry_getContext_Method, self).__init__(u"quark.concurrent.EventContext", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.TimeoutExpiry);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_TimeoutExpiry_fireEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_TimeoutExpiry_fireEvent_Method, self).__init__(u"quark.void", u"fireEvent", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.TimeoutExpiry);
        (obj).fireEvent();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_TimeoutExpiry(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_TimeoutExpiry, self).__init__(u"quark.concurrent.TimeoutExpiry");
        (self).name = u"quark.concurrent.TimeoutExpiry"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Timeout", u"timeout"), quark.reflect.Field(u"quark.concurrent.TimeoutListener", u"listener")])
        (self).methods = _List([quark_concurrent_TimeoutExpiry_getContext_Method(), quark_concurrent_TimeoutExpiry_fireEvent_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.TimeoutExpiry(_cast((args)[0], lambda: quark.concurrent.Timeout), _cast((args)[1], lambda: quark.concurrent.TimeoutListener))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_TimeoutExpiry.singleton = quark_concurrent_TimeoutExpiry()
class quark_concurrent_Timeout_start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Timeout_start_Method, self).__init__(u"quark.void", u"start", _List([u"quark.concurrent.TimeoutListener"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Timeout);
        (obj).start(_cast((args)[0], lambda: quark.concurrent.TimeoutListener));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Timeout_cancel_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Timeout_cancel_Method, self).__init__(u"quark.void", u"cancel", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Timeout);
        (obj).cancel();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Timeout_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Timeout_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Timeout);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Timeout_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Timeout_getContext_Method, self).__init__(u"quark.concurrent.Context", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Timeout);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Timeout(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Timeout, self).__init__(u"quark.concurrent.Timeout");
        (self).name = u"quark.concurrent.Timeout"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_context"), quark.reflect.Field(u"quark.float", u"timeout"), quark.reflect.Field(u"quark.concurrent.Lock", u"lock"), quark.reflect.Field(u"quark.concurrent.TimeoutListener", u"listener")])
        (self).methods = _List([quark_concurrent_Timeout_start_Method(), quark_concurrent_Timeout_cancel_Method(), quark_concurrent_Timeout_onExecute_Method(), quark_concurrent_Timeout_getContext_Method()])
        (self).parents = _List([u"quark.concurrent.EventContext"])

    def construct(self, args):
        return quark.concurrent.Timeout(_cast((args)[0], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Timeout.singleton = quark_concurrent_Timeout()
class quark_concurrent_TLSContextInitializer_getValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_TLSContextInitializer_getValue_Method, self).__init__(u"quark.concurrent.Context", u"getValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.TLSContextInitializer);
        return (obj).getValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_TLSContextInitializer(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_TLSContextInitializer, self).__init__(u"quark.concurrent.TLSContextInitializer");
        (self).name = u"quark.concurrent.TLSContextInitializer"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_concurrent_TLSContextInitializer_getValue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.TLSContextInitializer()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_TLSContextInitializer.singleton = quark_concurrent_TLSContextInitializer()
class quark_concurrent_Context_current_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Context_current_Method, self).__init__(u"quark.concurrent.Context", u"current", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Context);
        return quark.concurrent.Context.current()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Context_global_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Context_global_Method, self).__init__(u"quark.concurrent.Context", u"global", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Context);
        return quark.concurrent.Context.global_()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Context_runtime_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Context_runtime_Method, self).__init__(u"quark.Runtime", u"runtime", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Context);
        return quark.concurrent.Context.runtime()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Context_swap_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_concurrent_Context_swap_Method, self).__init__(u"quark.void", u"swap", _List([u"quark.concurrent.Context"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.concurrent.Context);
        quark.concurrent.Context.swap(_cast((args)[0], lambda: quark.concurrent.Context));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_concurrent_Context(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_concurrent_Context, self).__init__(u"quark.concurrent.Context");
        (self).name = u"quark.concurrent.Context"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_global"), quark.reflect.Field(u"quark.concurrent.TLS<quark.concurrent.Context>", u"_current"), quark.reflect.Field(u"quark.concurrent.Context", u"_parent"), quark.reflect.Field(u"quark.Runtime", u"_runtime"), quark.reflect.Field(u"quark.concurrent.Collector", u"collector")])
        (self).methods = _List([quark_concurrent_Context_current_Method(), quark_concurrent_Context_global_Method(), quark_concurrent_Context_runtime_Method(), quark_concurrent_Context_swap_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.concurrent.Context(_cast((args)[0], lambda: quark.concurrent.Context))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_concurrent_Context.singleton = quark_concurrent_Context()
class quark_HTTPError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_HTTPError, self).__init__(u"quark.HTTPError");
        (self).name = u"quark.HTTPError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return quark.HTTPError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_HTTPError.singleton = quark_HTTPError()
class quark_HTTPHandler(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_HTTPHandler, self).__init__(u"quark.HTTPHandler");
        (self).name = u"quark.HTTPHandler"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_HTTPHandler.singleton = quark_HTTPHandler()
class quark_HTTPRequest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_HTTPRequest, self).__init__(u"quark.HTTPRequest");
        (self).name = u"quark.HTTPRequest"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_HTTPRequest.singleton = quark_HTTPRequest()
class quark_HTTPResponse(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_HTTPResponse, self).__init__(u"quark.HTTPResponse");
        (self).name = u"quark.HTTPResponse"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_HTTPResponse.singleton = quark_HTTPResponse()
class quark_HTTPServlet(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_HTTPServlet, self).__init__(u"quark.HTTPServlet");
        (self).name = u"quark.HTTPServlet"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_HTTPServlet.singleton = quark_HTTPServlet()
class quark_WSError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_WSError, self).__init__(u"quark.WSError");
        (self).name = u"quark.WSError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return quark.WSError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_WSError.singleton = quark_WSError()
class quark_WSHandler(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_WSHandler, self).__init__(u"quark.WSHandler");
        (self).name = u"quark.WSHandler"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_WSHandler.singleton = quark_WSHandler()
class quark_WebSocket(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_WebSocket, self).__init__(u"quark.WebSocket");
        (self).name = u"quark.WebSocket"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_WebSocket.singleton = quark_WebSocket()
class quark_WSServlet(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_WSServlet, self).__init__(u"quark.WSServlet");
        (self).name = u"quark.WSServlet"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_WSServlet.singleton = quark_WSServlet()
class quark_test_TestInitializer_getValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_TestInitializer_getValue_Method, self).__init__(u"quark.test.Test", u"getValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.TestInitializer);
        return (obj).getValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_TestInitializer(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_test_TestInitializer, self).__init__(u"quark.test.TestInitializer");
        (self).name = u"quark.test.TestInitializer"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_test_TestInitializer_getValue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.test.TestInitializer()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_test_TestInitializer.singleton = quark_test_TestInitializer()
class quark_test_Test_current_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_current_Method, self).__init__(u"quark.test.Test", u"current", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        return quark.test.Test.current()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_match_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_match_Method, self).__init__(u"quark.bool", u"match", _List([u"quark.List<quark.String>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        return (obj).match(_cast((args)[0], lambda: _List))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_start_Method, self).__init__(u"quark.void", u"start", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        (obj).start();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_stop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_stop_Method, self).__init__(u"quark.void", u"stop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        (obj).stop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_check_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_check_Method, self).__init__(u"quark.bool", u"check", _List([u"quark.bool", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        return (obj).check(_cast((args)[0], lambda: bool), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test_run_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Test_run_Method, self).__init__(u"quark.void", u"run", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Test);
        (obj).run();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Test(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_test_Test, self).__init__(u"quark.test.Test");
        (self).name = u"quark.test.Test"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.TLS<quark.test.Test>", u"ctx"), quark.reflect.Field(u"quark.String", u"name"), quark.reflect.Field(u"quark.int", u"checks"), quark.reflect.Field(u"quark.List<quark.String>", u"successes"), quark.reflect.Field(u"quark.List<quark.String>", u"failures")])
        (self).methods = _List([quark_test_Test_current_Method(), quark_test_Test_match_Method(), quark_test_Test_start_Method(), quark_test_Test_stop_Method(), quark_test_Test_check_Method(), quark_test_Test_fail_Method(), quark_test_Test_run_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.test.Test(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_test_Test.singleton = quark_test_Test()
class quark_test_SafeMethodCaller_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_SafeMethodCaller_call_Method, self).__init__(u"quark.Object", u"call", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.SafeMethodCaller);
        return (obj).call((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_SafeMethodCaller_callMethod_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_SafeMethodCaller_callMethod_Method, self).__init__(u"quark.bool", u"callMethod", _List([u"quark.reflect.Method", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.SafeMethodCaller);
        return quark.test.SafeMethodCaller.callMethod(_cast((args)[0], lambda: quark.reflect.Method), (args)[1])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_SafeMethodCaller(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_test_SafeMethodCaller, self).__init__(u"quark.test.SafeMethodCaller");
        (self).name = u"quark.test.SafeMethodCaller"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.bool", u"useSafeCalls"), quark.reflect.Field(u"quark.reflect.Method", u"method"), quark.reflect.Field(u"quark.Object", u"test")])
        (self).methods = _List([quark_test_SafeMethodCaller_call_Method(), quark_test_SafeMethodCaller_callMethod_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.test.SafeMethodCaller(_cast((args)[0], lambda: quark.reflect.Method), (args)[1])

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_test_SafeMethodCaller.singleton = quark_test_SafeMethodCaller()
class quark_test_MethodTest_run_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_run_Method, self).__init__(u"quark.void", u"run", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        (obj).run();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_current_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_current_Method, self).__init__(u"quark.test.Test", u"current", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        return quark.test.Test.current()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_match_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_match_Method, self).__init__(u"quark.bool", u"match", _List([u"quark.List<quark.String>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        return (obj).match(_cast((args)[0], lambda: _List))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_start_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_start_Method, self).__init__(u"quark.void", u"start", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        (obj).start();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_stop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_stop_Method, self).__init__(u"quark.void", u"stop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        (obj).stop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_check_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_check_Method, self).__init__(u"quark.bool", u"check", _List([u"quark.bool", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        return (obj).check(_cast((args)[0], lambda: bool), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_MethodTest_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.MethodTest);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_MethodTest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_test_MethodTest, self).__init__(u"quark.test.MethodTest");
        (self).name = u"quark.test.MethodTest"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.TLS<quark.test.Test>", u"ctx"), quark.reflect.Field(u"quark.String", u"name"), quark.reflect.Field(u"quark.int", u"checks"), quark.reflect.Field(u"quark.List<quark.String>", u"successes"), quark.reflect.Field(u"quark.List<quark.String>", u"failures"), quark.reflect.Field(u"quark.reflect.Class", u"klass"), quark.reflect.Field(u"quark.reflect.Method", u"method")])
        (self).methods = _List([quark_test_MethodTest_run_Method(), quark_test_MethodTest_current_Method(), quark_test_MethodTest_match_Method(), quark_test_MethodTest_start_Method(), quark_test_MethodTest_stop_Method(), quark_test_MethodTest_check_Method(), quark_test_MethodTest_fail_Method()])
        (self).parents = _List([u"quark.test.Test"])

    def construct(self, args):
        return quark.test.MethodTest(_cast((args)[0], lambda: quark.reflect.Class), _cast((args)[1], lambda: quark.reflect.Method))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_test_MethodTest.singleton = quark_test_MethodTest()
class quark_test_Harness_collect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Harness_collect_Method, self).__init__(u"quark.void", u"collect", _List([u"quark.List<quark.String>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Harness);
        (obj).collect(_cast((args)[0], lambda: _List));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Harness_list_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Harness_list_Method, self).__init__(u"quark.void", u"list", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Harness);
        (obj).list();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Harness_run_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Harness_run_Method, self).__init__(u"quark.int", u"run", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Harness);
        return (obj).run()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Harness_json_report_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_test_Harness_json_report_Method, self).__init__(u"quark.void", u"json_report", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.test.Harness);
        (obj).json_report();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_test_Harness(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_test_Harness, self).__init__(u"quark.test.Harness");
        (self).name = u"quark.test.Harness"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"pkg"), quark.reflect.Field(u"quark.List<quark.test.Test>", u"tests"), quark.reflect.Field(u"quark.int", u"filtered")])
        (self).methods = _List([quark_test_Harness_collect_Method(), quark_test_Harness_list_Method(), quark_test_Harness_run_Method(), quark_test_Harness_json_report_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.test.Harness(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_test_Harness.singleton = quark_test_Harness()
class quark_URL(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_URL, self).__init__(u"quark.URL");
        (self).name = u"quark.URL"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"scheme"), quark.reflect.Field(u"quark.String", u"host"), quark.reflect.Field(u"quark.String", u"port"), quark.reflect.Field(u"quark.String", u"path")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.URL()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_URL.singleton = quark_URL()
class quark_spi_RuntimeSpi_open_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_open_Method, self).__init__(u"quark.void", u"open", _List([u"quark.String", u"quark.WSHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).open(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_request_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_request_Method, self).__init__(u"quark.void", u"request", _List([u"quark.HTTPRequest", u"quark.HTTPHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).request(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_schedule_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_schedule_Method, self).__init__(u"quark.void", u"schedule", _List([u"quark.Task", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).schedule(_cast((args)[0], lambda: quark.Task), _cast((args)[1], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_codec_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_codec_Method, self).__init__(u"quark.Codec", u"codec", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        return (obj).codec()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String", u"quark.HTTPServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.HTTPServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String", u"quark.WSServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).serveWS(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_respond_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_respond_Method, self).__init__(u"quark.void", u"respond", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).respond(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_logger_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_logger_Method, self).__init__(u"quark.Logger", u"logger", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        return (obj).logger(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_now_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_now_Method, self).__init__(u"quark.long", u"now", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        return (obj).now()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_sleep_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_sleep_Method, self).__init__(u"quark.void", u"sleep", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        (obj).sleep(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_uuid_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_uuid_Method, self).__init__(u"quark.String", u"uuid", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        return (obj).uuid()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi_callSafely_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi_callSafely_Method, self).__init__(u"quark.Object", u"callSafely", _List([u"quark.UnaryCallable", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeSpi);
        return (obj).callSafely(_cast((args)[0], lambda: quark.UnaryCallable), (args)[1])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeSpi(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_RuntimeSpi, self).__init__(u"quark.spi.RuntimeSpi");
        (self).name = u"quark.spi.RuntimeSpi"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_spi_RuntimeSpi_open_Method(), quark_spi_RuntimeSpi_request_Method(), quark_spi_RuntimeSpi_schedule_Method(), quark_spi_RuntimeSpi_codec_Method(), quark_spi_RuntimeSpi_serveHTTP_Method(), quark_spi_RuntimeSpi_serveWS_Method(), quark_spi_RuntimeSpi_respond_Method(), quark_spi_RuntimeSpi_fail_Method(), quark_spi_RuntimeSpi_logger_Method(), quark_spi_RuntimeSpi_now_Method(), quark_spi_RuntimeSpi_sleep_Method(), quark_spi_RuntimeSpi_uuid_Method(), quark_spi_RuntimeSpi_callSafely_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_RuntimeSpi.singleton = quark_spi_RuntimeSpi()
class quark_spi_RuntimeFactory_makeRuntime_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_RuntimeFactory_makeRuntime_Method, self).__init__(u"quark.Runtime", u"makeRuntime", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi.RuntimeFactory);
        return (obj).makeRuntime()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_RuntimeFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_RuntimeFactory, self).__init__(u"quark.spi.RuntimeFactory");
        (self).name = u"quark.spi.RuntimeFactory"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi.RuntimeFactory", u"factory"), quark.reflect.Field(u"quark.bool", u"enable_tracing"), quark.reflect.Field(u"quark.bool", u"env_checked")])
        (self).methods = _List([quark_spi_RuntimeFactory_makeRuntime_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi.RuntimeFactory()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_RuntimeFactory.singleton = quark_spi_RuntimeFactory()
class quark_spi_api_ServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_ServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.ServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_ServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_ServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.ServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_ServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_ServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.ServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_ServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_ServletProxy, self).__init__(u"quark.spi_api.ServletProxy");
        (self).name = u"quark.spi_api.ServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.Runtime", u"real_runtime")])
        (self).methods = _List([quark_spi_api_ServletProxy_onServletInit_Method(), quark_spi_api_ServletProxy_onServletError_Method(), quark_spi_api_ServletProxy_onServletEnd_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi_api.ServletProxy(_cast((args)[0], lambda: quark.Runtime), _cast((args)[1], lambda: quark.Servlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_ServletProxy.singleton = quark_spi_api_ServletProxy()
class quark_spi_api_HTTPServletProxy_onHTTPRequest_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy_onHTTPRequest_Method, self).__init__(u"quark.void", u"onHTTPRequest", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.HTTPServletProxy);
        (obj).onHTTPRequest(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_HTTPServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.HTTPServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_HTTPServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.HTTPServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_HTTPServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.HTTPServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_HTTPServletProxy_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.HTTPServletProxy);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_HTTPServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_HTTPServletProxy, self).__init__(u"quark.spi_api.HTTPServletProxy");
        (self).name = u"quark.spi_api.HTTPServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.Runtime", u"real_runtime"), quark.reflect.Field(u"quark.HTTPServlet", u"http_servlet_impl")])
        (self).methods = _List([quark_spi_api_HTTPServletProxy_onHTTPRequest_Method(), quark_spi_api_HTTPServletProxy_onServletInit_Method(), quark_spi_api_HTTPServletProxy_onServletError_Method(), quark_spi_api_HTTPServletProxy_onServletEnd_Method(), quark_spi_api_HTTPServletProxy_serveHTTP_Method()])
        (self).parents = _List([u"quark.spi_api.ServletProxy"])

    def construct(self, args):
        return quark.spi_api.HTTPServletProxy(_cast((args)[0], lambda: quark.Runtime), _cast((args)[1], lambda: quark.HTTPServlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_HTTPServletProxy.singleton = quark_spi_api_HTTPServletProxy()
class quark_spi_api_WSServletProxy_onWSConnect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy_onWSConnect_Method, self).__init__(u"quark.WSHandler", u"onWSConnect", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.WSServletProxy);
        return (obj).onWSConnect(_cast((args)[0], lambda: quark.HTTPRequest))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_WSServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.WSServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_WSServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.WSServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_WSServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.WSServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_WSServletProxy_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.WSServletProxy);
        (obj).serveWS(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_WSServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_WSServletProxy, self).__init__(u"quark.spi_api.WSServletProxy");
        (self).name = u"quark.spi_api.WSServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.Runtime", u"real_runtime"), quark.reflect.Field(u"quark.WSServlet", u"ws_servlet_impl")])
        (self).methods = _List([quark_spi_api_WSServletProxy_onWSConnect_Method(), quark_spi_api_WSServletProxy_onServletInit_Method(), quark_spi_api_WSServletProxy_onServletError_Method(), quark_spi_api_WSServletProxy_onServletEnd_Method(), quark_spi_api_WSServletProxy_serveWS_Method()])
        (self).parents = _List([u"quark.spi_api.ServletProxy"])

    def construct(self, args):
        return quark.spi_api.WSServletProxy(_cast((args)[0], lambda: quark.Runtime), _cast((args)[1], lambda: quark.WSServlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_WSServletProxy.singleton = quark_spi_api_WSServletProxy()
class quark_spi_api_TaskProxy_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_TaskProxy_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.TaskProxy);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_TaskProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_TaskProxy, self).__init__(u"quark.spi_api.TaskProxy");
        (self).name = u"quark.spi_api.TaskProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Task", u"task_impl"), quark.reflect.Field(u"quark.Runtime", u"real_runtime")])
        (self).methods = _List([quark_spi_api_TaskProxy_onExecute_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi_api.TaskProxy(_cast((args)[0], lambda: quark.Runtime), _cast((args)[1], lambda: quark.Task))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_TaskProxy.singleton = quark_spi_api_TaskProxy()
class quark_spi_api_RuntimeProxy_open_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_open_Method, self).__init__(u"quark.void", u"open", _List([u"quark.String", u"quark.WSHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).open(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_request_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_request_Method, self).__init__(u"quark.void", u"request", _List([u"quark.HTTPRequest", u"quark.HTTPHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).request(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_schedule_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_schedule_Method, self).__init__(u"quark.void", u"schedule", _List([u"quark.Task", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).schedule(_cast((args)[0], lambda: quark.Task), _cast((args)[1], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_codec_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_codec_Method, self).__init__(u"quark.Codec", u"codec", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        return (obj).codec()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_now_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_now_Method, self).__init__(u"quark.long", u"now", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        return (obj).now()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_sleep_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_sleep_Method, self).__init__(u"quark.void", u"sleep", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).sleep(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_uuid_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_uuid_Method, self).__init__(u"quark.String", u"uuid", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        return (obj).uuid()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String", u"quark.HTTPServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.HTTPServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String", u"quark.WSServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).serveWS(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_respond_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_respond_Method, self).__init__(u"quark.void", u"respond", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).respond(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_logger_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_logger_Method, self).__init__(u"quark.Logger", u"logger", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        return (obj).logger(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy_callSafely_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy_callSafely_Method, self).__init__(u"quark.Object", u"callSafely", _List([u"quark.UnaryCallable", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api.RuntimeProxy);
        return (obj).callSafely(_cast((args)[0], lambda: quark.UnaryCallable), (args)[1])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_RuntimeProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_RuntimeProxy, self).__init__(u"quark.spi_api.RuntimeProxy");
        (self).name = u"quark.spi_api.RuntimeProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Runtime", u"impl")])
        (self).methods = _List([quark_spi_api_RuntimeProxy_open_Method(), quark_spi_api_RuntimeProxy_request_Method(), quark_spi_api_RuntimeProxy_schedule_Method(), quark_spi_api_RuntimeProxy_codec_Method(), quark_spi_api_RuntimeProxy_now_Method(), quark_spi_api_RuntimeProxy_sleep_Method(), quark_spi_api_RuntimeProxy_uuid_Method(), quark_spi_api_RuntimeProxy_serveHTTP_Method(), quark_spi_api_RuntimeProxy_serveWS_Method(), quark_spi_api_RuntimeProxy_respond_Method(), quark_spi_api_RuntimeProxy_fail_Method(), quark_spi_api_RuntimeProxy_logger_Method(), quark_spi_api_RuntimeProxy_callSafely_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi_api.RuntimeProxy(_cast((args)[0], lambda: quark.Runtime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_RuntimeProxy.singleton = quark_spi_api_RuntimeProxy()
class quark_spi_api_tracing_Identificator_next_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_Identificator_next_Method, self).__init__(u"quark.String", u"next", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.Identificator);
        return (obj).next(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_Identificator(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_Identificator, self).__init__(u"quark.spi_api_tracing.Identificator");
        (self).name = u"quark.spi_api_tracing.Identificator"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Lock", u"lock"), quark.reflect.Field(u"quark.int", u"seq")])
        (self).methods = _List([quark_spi_api_tracing_Identificator_next_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi_api_tracing.Identificator()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_Identificator.singleton = quark_spi_api_tracing_Identificator()
class quark_spi_api_tracing_Identifiable(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_Identifiable, self).__init__(u"quark.spi_api_tracing.Identifiable");
        (self).name = u"quark.spi_api_tracing.Identifiable"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.spi_api_tracing.Identifiable((args)[0], _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_Identifiable.singleton = quark_spi_api_tracing_Identifiable()
class quark_spi_api_tracing_ServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_ServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.ServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_ServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_ServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.ServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_ServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_ServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.ServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_ServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_ServletProxy, self).__init__(u"quark.spi_api_tracing.ServletProxy");
        (self).name = u"quark.spi_api_tracing.ServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.spi_api_tracing.RuntimeProxy", u"real_runtime")])
        (self).methods = _List([quark_spi_api_tracing_ServletProxy_onServletInit_Method(), quark_spi_api_tracing_ServletProxy_onServletError_Method(), quark_spi_api_tracing_ServletProxy_onServletEnd_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.ServletProxy((args)[0], _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: quark.spi_api_tracing.RuntimeProxy), _cast((args)[3], lambda: quark.Servlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_ServletProxy.singleton = quark_spi_api_tracing_ServletProxy()
class quark_spi_api_tracing_HTTPRequestProxy_getUrl_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_getUrl_Method, self).__init__(u"quark.String", u"getUrl", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        return (obj).getUrl()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_setMethod_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_setMethod_Method, self).__init__(u"quark.void", u"setMethod", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        (obj).setMethod(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_getMethod_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_getMethod_Method, self).__init__(u"quark.String", u"getMethod", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        return (obj).getMethod()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_setBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_setBody_Method, self).__init__(u"quark.void", u"setBody", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        (obj).setBody(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_getBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_getBody_Method, self).__init__(u"quark.String", u"getBody", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        return (obj).getBody()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_setHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_setHeader_Method, self).__init__(u"quark.void", u"setHeader", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        (obj).setHeader(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_getHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_getHeader_Method, self).__init__(u"quark.String", u"getHeader", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        return (obj).getHeader(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy_getHeaders_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy_getHeaders_Method, self).__init__(u"quark.List<quark.String>", u"getHeaders", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPRequestProxy);
        return (obj).getHeaders()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPRequestProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPRequestProxy, self).__init__(u"quark.spi_api_tracing.HTTPRequestProxy");
        (self).name = u"quark.spi_api_tracing.HTTPRequestProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.HTTPRequest", u"request_impl")])
        (self).methods = _List([quark_spi_api_tracing_HTTPRequestProxy_getUrl_Method(), quark_spi_api_tracing_HTTPRequestProxy_setMethod_Method(), quark_spi_api_tracing_HTTPRequestProxy_getMethod_Method(), quark_spi_api_tracing_HTTPRequestProxy_setBody_Method(), quark_spi_api_tracing_HTTPRequestProxy_getBody_Method(), quark_spi_api_tracing_HTTPRequestProxy_setHeader_Method(), quark_spi_api_tracing_HTTPRequestProxy_getHeader_Method(), quark_spi_api_tracing_HTTPRequestProxy_getHeaders_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.HTTPRequestProxy((args)[0], _cast((args)[1], lambda: quark.HTTPRequest))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_HTTPRequestProxy.singleton = quark_spi_api_tracing_HTTPRequestProxy()
class quark_spi_api_tracing_HTTPResponseProxy_getCode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_getCode_Method, self).__init__(u"quark.int", u"getCode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        return (obj).getCode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_setCode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_setCode_Method, self).__init__(u"quark.void", u"setCode", _List([u"quark.int"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        (obj).setCode(_cast((args)[0], lambda: int));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_setBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_setBody_Method, self).__init__(u"quark.void", u"setBody", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        (obj).setBody(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_getBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_getBody_Method, self).__init__(u"quark.String", u"getBody", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        return (obj).getBody()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_setHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_setHeader_Method, self).__init__(u"quark.void", u"setHeader", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        (obj).setHeader(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_getHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_getHeader_Method, self).__init__(u"quark.String", u"getHeader", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        return (obj).getHeader(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy_getHeaders_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy_getHeaders_Method, self).__init__(u"quark.List<quark.String>", u"getHeaders", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPResponseProxy);
        return (obj).getHeaders()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPResponseProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPResponseProxy, self).__init__(u"quark.spi_api_tracing.HTTPResponseProxy");
        (self).name = u"quark.spi_api_tracing.HTTPResponseProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.HTTPResponse", u"response_impl")])
        (self).methods = _List([quark_spi_api_tracing_HTTPResponseProxy_getCode_Method(), quark_spi_api_tracing_HTTPResponseProxy_setCode_Method(), quark_spi_api_tracing_HTTPResponseProxy_setBody_Method(), quark_spi_api_tracing_HTTPResponseProxy_getBody_Method(), quark_spi_api_tracing_HTTPResponseProxy_setHeader_Method(), quark_spi_api_tracing_HTTPResponseProxy_getHeader_Method(), quark_spi_api_tracing_HTTPResponseProxy_getHeaders_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.HTTPResponseProxy((args)[0], _cast((args)[1], lambda: quark.HTTPResponse))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_HTTPResponseProxy.singleton = quark_spi_api_tracing_HTTPResponseProxy()
class quark_spi_api_tracing_HTTPServletProxy_onHTTPRequest_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy_onHTTPRequest_Method, self).__init__(u"quark.void", u"onHTTPRequest", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPServletProxy);
        (obj).onHTTPRequest(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPServletProxy_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPServletProxy);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPServletProxy, self).__init__(u"quark.spi_api_tracing.HTTPServletProxy");
        (self).name = u"quark.spi_api_tracing.HTTPServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.spi_api_tracing.RuntimeProxy", u"real_runtime"), quark.reflect.Field(u"quark.HTTPServlet", u"http_servlet_impl")])
        (self).methods = _List([quark_spi_api_tracing_HTTPServletProxy_onHTTPRequest_Method(), quark_spi_api_tracing_HTTPServletProxy_onServletInit_Method(), quark_spi_api_tracing_HTTPServletProxy_onServletError_Method(), quark_spi_api_tracing_HTTPServletProxy_onServletEnd_Method(), quark_spi_api_tracing_HTTPServletProxy_serveHTTP_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.ServletProxy"])

    def construct(self, args):
        return quark.spi_api_tracing.HTTPServletProxy((args)[0], _cast((args)[1], lambda: quark.spi_api_tracing.RuntimeProxy), _cast((args)[2], lambda: quark.HTTPServlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_HTTPServletProxy.singleton = quark_spi_api_tracing_HTTPServletProxy()
class quark_spi_api_tracing_WSServletProxy_onWSConnect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy_onWSConnect_Method, self).__init__(u"quark.WSHandler", u"onWSConnect", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSServletProxy);
        return (obj).onWSConnect(_cast((args)[0], lambda: quark.HTTPRequest))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSServletProxy_onServletInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy_onServletInit_Method, self).__init__(u"quark.void", u"onServletInit", _List([u"quark.String", u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSServletProxy);
        (obj).onServletInit(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSServletProxy_onServletError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy_onServletError_Method, self).__init__(u"quark.void", u"onServletError", _List([u"quark.String", u"quark.ServletError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSServletProxy);
        (obj).onServletError(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.ServletError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSServletProxy_onServletEnd_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy_onServletEnd_Method, self).__init__(u"quark.void", u"onServletEnd", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSServletProxy);
        (obj).onServletEnd(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSServletProxy_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSServletProxy);
        (obj).serveWS(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSServletProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSServletProxy, self).__init__(u"quark.spi_api_tracing.WSServletProxy");
        (self).name = u"quark.spi_api_tracing.WSServletProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.Servlet", u"servlet_impl"), quark.reflect.Field(u"quark.spi_api_tracing.RuntimeProxy", u"real_runtime"), quark.reflect.Field(u"quark.WSServlet", u"ws_servlet_impl")])
        (self).methods = _List([quark_spi_api_tracing_WSServletProxy_onWSConnect_Method(), quark_spi_api_tracing_WSServletProxy_onServletInit_Method(), quark_spi_api_tracing_WSServletProxy_onServletError_Method(), quark_spi_api_tracing_WSServletProxy_onServletEnd_Method(), quark_spi_api_tracing_WSServletProxy_serveWS_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.ServletProxy"])

    def construct(self, args):
        return quark.spi_api_tracing.WSServletProxy((args)[0], _cast((args)[1], lambda: quark.spi_api_tracing.RuntimeProxy), _cast((args)[2], lambda: quark.WSServlet))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_WSServletProxy.singleton = quark_spi_api_tracing_WSServletProxy()
class quark_spi_api_tracing_TaskProxy_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_TaskProxy_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.TaskProxy);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_TaskProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_TaskProxy, self).__init__(u"quark.spi_api_tracing.TaskProxy");
        (self).name = u"quark.spi_api_tracing.TaskProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.Task", u"task_impl"), quark.reflect.Field(u"quark.spi_api_tracing.RuntimeProxy", u"real_runtime")])
        (self).methods = _List([quark_spi_api_tracing_TaskProxy_onExecute_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.TaskProxy((args)[0], _cast((args)[1], lambda: quark.spi_api_tracing.RuntimeProxy), _cast((args)[2], lambda: quark.Task))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_TaskProxy.singleton = quark_spi_api_tracing_TaskProxy()
class quark_spi_api_tracing_WebSocketProxy_send_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WebSocketProxy_send_Method, self).__init__(u"quark.bool", u"send", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WebSocketProxy);
        return (obj).send(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WebSocketProxy_sendBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WebSocketProxy_sendBinary_Method, self).__init__(u"quark.bool", u"sendBinary", _List([u"quark.Buffer"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WebSocketProxy);
        return (obj).sendBinary((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WebSocketProxy_close_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WebSocketProxy_close_Method, self).__init__(u"quark.bool", u"close", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WebSocketProxy);
        return (obj).close()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WebSocketProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WebSocketProxy, self).__init__(u"quark.spi_api_tracing.WebSocketProxy");
        (self).name = u"quark.spi_api_tracing.WebSocketProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.WebSocket", u"socket_impl")])
        (self).methods = _List([quark_spi_api_tracing_WebSocketProxy_send_Method(), quark_spi_api_tracing_WebSocketProxy_sendBinary_Method(), quark_spi_api_tracing_WebSocketProxy_close_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.WebSocketProxy((args)[0], _cast((args)[1], lambda: quark.WebSocket))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_WebSocketProxy.singleton = quark_spi_api_tracing_WebSocketProxy()
class quark_spi_api_tracing_WSHandlerProxy__wrap_socket_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy__wrap_socket_Method, self).__init__(u"quark.spi_api_tracing.WebSocketProxy", u"_wrap_socket", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        return (obj)._wrap_socket(_cast((args)[0], lambda: quark.WebSocket))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSInit_Method, self).__init__(u"quark.void", u"onWSInit", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSInit(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSConnected(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSMessage_Method, self).__init__(u"quark.void", u"onWSMessage", _List([u"quark.WebSocket", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSMessage(_cast((args)[0], lambda: quark.WebSocket), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSBinary_Method, self).__init__(u"quark.void", u"onWSBinary", _List([u"quark.WebSocket", u"quark.Buffer"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSBinary(_cast((args)[0], lambda: quark.WebSocket), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSClosed_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSClosed_Method, self).__init__(u"quark.void", u"onWSClosed", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSClosed(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSError_Method, self).__init__(u"quark.void", u"onWSError", _List([u"quark.WebSocket", u"quark.WSError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSError(_cast((args)[0], lambda: quark.WebSocket), _cast((args)[1], lambda: quark.WSError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy_onWSFinal_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy_onWSFinal_Method, self).__init__(u"quark.void", u"onWSFinal", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.WSHandlerProxy);
        (obj).onWSFinal(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_WSHandlerProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_WSHandlerProxy, self).__init__(u"quark.spi_api_tracing.WSHandlerProxy");
        (self).name = u"quark.spi_api_tracing.WSHandlerProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.WSHandler", u"handler_impl"), quark.reflect.Field(u"quark.spi_api_tracing.WebSocketProxy", u"_wrapped_socket")])
        (self).methods = _List([quark_spi_api_tracing_WSHandlerProxy__wrap_socket_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSInit_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSConnected_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSMessage_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSBinary_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSClosed_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSError_Method(), quark_spi_api_tracing_WSHandlerProxy_onWSFinal_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.WSHandlerProxy((args)[0], _cast((args)[1], lambda: quark.WSHandler))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_WSHandlerProxy.singleton = quark_spi_api_tracing_WSHandlerProxy()
class quark_spi_api_tracing_HTTPHandlerProxy_onHTTPInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPHandlerProxy_onHTTPInit_Method, self).__init__(u"quark.void", u"onHTTPInit", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPHandlerProxy);
        (obj).onHTTPInit(_cast((args)[0], lambda: quark.HTTPRequest));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPHandlerProxy_onHTTPResponse_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPHandlerProxy_onHTTPResponse_Method, self).__init__(u"quark.void", u"onHTTPResponse", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPHandlerProxy);
        (obj).onHTTPResponse(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPHandlerProxy_onHTTPError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPHandlerProxy_onHTTPError_Method, self).__init__(u"quark.void", u"onHTTPError", _List([u"quark.HTTPRequest", u"quark.HTTPError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPHandlerProxy);
        (obj).onHTTPError(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPHandlerProxy_onHTTPFinal_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPHandlerProxy_onHTTPFinal_Method, self).__init__(u"quark.void", u"onHTTPFinal", _List([u"quark.HTTPRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.HTTPHandlerProxy);
        (obj).onHTTPFinal(_cast((args)[0], lambda: quark.HTTPRequest));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_HTTPHandlerProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_HTTPHandlerProxy, self).__init__(u"quark.spi_api_tracing.HTTPHandlerProxy");
        (self).name = u"quark.spi_api_tracing.HTTPHandlerProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.HTTPHandler", u"handler_impl"), quark.reflect.Field(u"quark.spi_api_tracing.HTTPRequestProxy", u"wrapped_request")])
        (self).methods = _List([quark_spi_api_tracing_HTTPHandlerProxy_onHTTPInit_Method(), quark_spi_api_tracing_HTTPHandlerProxy_onHTTPResponse_Method(), quark_spi_api_tracing_HTTPHandlerProxy_onHTTPError_Method(), quark_spi_api_tracing_HTTPHandlerProxy_onHTTPFinal_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.HTTPHandlerProxy((args)[0], _cast((args)[1], lambda: quark.spi_api_tracing.HTTPRequestProxy), _cast((args)[2], lambda: quark.HTTPHandler))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_HTTPHandlerProxy.singleton = quark_spi_api_tracing_HTTPHandlerProxy()
class quark_spi_api_tracing_RuntimeProxy_open_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_open_Method, self).__init__(u"quark.void", u"open", _List([u"quark.String", u"quark.WSHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).open(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_request_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_request_Method, self).__init__(u"quark.void", u"request", _List([u"quark.HTTPRequest", u"quark.HTTPHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).request(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_schedule_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_schedule_Method, self).__init__(u"quark.void", u"schedule", _List([u"quark.Task", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).schedule(_cast((args)[0], lambda: quark.Task), _cast((args)[1], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_codec_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_codec_Method, self).__init__(u"quark.Codec", u"codec", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        return (obj).codec()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_now_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_now_Method, self).__init__(u"quark.long", u"now", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        return (obj).now()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_sleep_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_sleep_Method, self).__init__(u"quark.void", u"sleep", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).sleep(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_uuid_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_uuid_Method, self).__init__(u"quark.String", u"uuid", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        return (obj).uuid()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_callSafely_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_callSafely_Method, self).__init__(u"quark.Object", u"callSafely", _List([u"quark.UnaryCallable", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        return (obj).callSafely(_cast((args)[0], lambda: quark.UnaryCallable), (args)[1])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String", u"quark.HTTPServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.HTTPServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String", u"quark.WSServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).serveWS(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_respond_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_respond_Method, self).__init__(u"quark.void", u"respond", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).respond(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy_logger_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy_logger_Method, self).__init__(u"quark.Logger", u"logger", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.spi_api_tracing.RuntimeProxy);
        return (obj).logger(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_spi_api_tracing_RuntimeProxy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_spi_api_tracing_RuntimeProxy, self).__init__(u"quark.spi_api_tracing.RuntimeProxy");
        (self).name = u"quark.spi_api_tracing.RuntimeProxy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.spi_api_tracing.Identificator", u"namer"), quark.reflect.Field(u"quark.String", u"id"), quark.reflect.Field(u"quark.Logger", u"log"), quark.reflect.Field(u"quark.Runtime", u"impl")])
        (self).methods = _List([quark_spi_api_tracing_RuntimeProxy_open_Method(), quark_spi_api_tracing_RuntimeProxy_request_Method(), quark_spi_api_tracing_RuntimeProxy_schedule_Method(), quark_spi_api_tracing_RuntimeProxy_codec_Method(), quark_spi_api_tracing_RuntimeProxy_now_Method(), quark_spi_api_tracing_RuntimeProxy_sleep_Method(), quark_spi_api_tracing_RuntimeProxy_uuid_Method(), quark_spi_api_tracing_RuntimeProxy_callSafely_Method(), quark_spi_api_tracing_RuntimeProxy_serveHTTP_Method(), quark_spi_api_tracing_RuntimeProxy_serveWS_Method(), quark_spi_api_tracing_RuntimeProxy_respond_Method(), quark_spi_api_tracing_RuntimeProxy_fail_Method(), quark_spi_api_tracing_RuntimeProxy_logger_Method()])
        (self).parents = _List([u"quark.spi_api_tracing.Identifiable"])

    def construct(self, args):
        return quark.spi_api_tracing.RuntimeProxy(_cast((args)[0], lambda: quark.Runtime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_spi_api_tracing_RuntimeProxy.singleton = quark_spi_api_tracing_RuntimeProxy()
class quark_os_OSError_getMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_OSError_getMessage_Method, self).__init__(u"quark.String", u"getMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.OSError);
        return (obj).getMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_OSError_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_OSError_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.OSError);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_OSError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_os_OSError, self).__init__(u"quark.os.OSError");
        (self).name = u"quark.os.OSError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([quark_os_OSError_getMessage_Method(), quark_os_OSError_toString_Method()])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return quark.os.OSError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_os_OSError.singleton = quark_os_OSError()
class quark_os_FileContents_onFinished_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_onFinished_Method, self).__init__(u"quark.void", u"onFinished", _List([u"quark.concurrent.FutureListener"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        (obj).onFinished(_cast((args)[0], lambda: quark.concurrent.FutureListener));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents_finish_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_finish_Method, self).__init__(u"quark.void", u"finish", _List([u"quark.error.Error"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        (obj).finish(_cast((args)[0], lambda: quark.error.Error));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents_isFinished_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_isFinished_Method, self).__init__(u"quark.bool", u"isFinished", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        return (obj).isFinished()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents_getError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_getError_Method, self).__init__(u"quark.error.Error", u"getError", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        return (obj).getError()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents_await_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_await_Method, self).__init__(u"quark.void", u"await", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        (obj).await(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_FileContents_getContext_Method, self).__init__(u"quark.concurrent.Context", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.FileContents);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_FileContents(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_os_FileContents, self).__init__(u"quark.os.FileContents");
        (self).name = u"quark.os.FileContents"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_context"), quark.reflect.Field(u"quark.bool", u"_finished"), quark.reflect.Field(u"quark.error.Error", u"_error"), quark.reflect.Field(u"quark.List<quark.concurrent.FutureCompletion>", u"_callbacks"), quark.reflect.Field(u"quark.concurrent.Lock", u"_lock"), quark.reflect.Field(u"quark.String", u"value")])
        (self).methods = _List([quark_os_FileContents_onFinished_Method(), quark_os_FileContents_finish_Method(), quark_os_FileContents_isFinished_Method(), quark_os_FileContents_getError_Method(), quark_os_FileContents_await_Method(), quark_os_FileContents_getContext_Method()])
        (self).parents = _List([u"quark.concurrent.Future"])

    def construct(self, args):
        return quark.os.FileContents()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_os_FileContents.singleton = quark_os_FileContents()
class quark_os_Environment_getEnvironment_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_Environment_getEnvironment_Method, self).__init__(u"quark.os.Environment", u"getEnvironment", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.Environment);
        return quark.os.Environment.getEnvironment()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_Environment___get___Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_Environment___get___Method, self).__init__(u"quark.String", u"__get__", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.Environment);
        return (obj)._q__get__(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_Environment_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_Environment_get_Method, self).__init__(u"quark.String", u"get", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.Environment);
        return (obj).get(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_Environment_getUser_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_os_Environment_getUser_Method, self).__init__(u"quark.String", u"getUser", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.os.Environment);
        return quark.os.Environment.getUser()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_os_Environment(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_os_Environment, self).__init__(u"quark.os.Environment");
        (self).name = u"quark.os.Environment"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.os.Environment", u"ENV")])
        (self).methods = _List([quark_os_Environment_getEnvironment_Method(), quark_os_Environment___get___Method(), quark_os_Environment_get_Method(), quark_os_Environment_getUser_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.os.Environment()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_os_Environment.singleton = quark_os_Environment()
class quark_mock_MockEvent_getType_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockEvent_getType_Method, self).__init__(u"quark.String", u"getType", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockEvent);
        return (obj).getType()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockEvent_getArgs_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockEvent_getArgs_Method, self).__init__(u"quark.List<quark.Object>", u"getArgs", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockEvent);
        return (obj).getArgs()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockEvent_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockEvent_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockEvent);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockEvent, self).__init__(u"quark.mock.MockEvent");
        (self).name = u"quark.mock.MockEvent"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_mock_MockEvent_getType_Method(), quark_mock_MockEvent_getArgs_Method(), quark_mock_MockEvent_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockEvent.singleton = quark_mock_MockEvent()
class quark_mock_SocketEvent_getType_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_getType_Method, self).__init__(u"quark.String", u"getType", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).getType()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_getArgs_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_getArgs_Method, self).__init__(u"quark.List<quark.Object>", u"getArgs", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).getArgs()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_accept_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_accept_Method, self).__init__(u"quark.void", u"accept", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        (obj).accept();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_send_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_send_Method, self).__init__(u"quark.void", u"send", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        (obj).send(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_close_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_close_Method, self).__init__(u"quark.void", u"close", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        (obj).close();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_expectMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_expectMessage_Method, self).__init__(u"quark.mock.MockMessage", u"expectMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).expectMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_expectTextMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_expectTextMessage_Method, self).__init__(u"quark.mock.TextMessage", u"expectTextMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).expectTextMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_expectBinaryMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_expectBinaryMessage_Method, self).__init__(u"quark.mock.BinaryMessage", u"expectBinaryMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).expectBinaryMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.SocketEvent);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_SocketEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_SocketEvent, self).__init__(u"quark.mock.SocketEvent");
        (self).name = u"quark.mock.SocketEvent"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"url"), quark.reflect.Field(u"quark.WSHandler", u"handler"), quark.reflect.Field(u"quark.mock.MockSocket", u"sock"), quark.reflect.Field(u"quark.int", u"expectIdx")])
        (self).methods = _List([quark_mock_SocketEvent_getType_Method(), quark_mock_SocketEvent_getArgs_Method(), quark_mock_SocketEvent_accept_Method(), quark_mock_SocketEvent_send_Method(), quark_mock_SocketEvent_close_Method(), quark_mock_SocketEvent_expectMessage_Method(), quark_mock_SocketEvent_expectTextMessage_Method(), quark_mock_SocketEvent_expectBinaryMessage_Method(), quark_mock_SocketEvent_toString_Method()])
        (self).parents = _List([u"quark.mock.MockEvent"])

    def construct(self, args):
        return quark.mock.SocketEvent(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSHandler))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_SocketEvent.singleton = quark_mock_SocketEvent()
class quark_mock_MockMessage_isBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockMessage_isBinary_Method, self).__init__(u"quark.bool", u"isBinary", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockMessage);
        return (obj).isBinary()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockMessage_isText_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockMessage_isText_Method, self).__init__(u"quark.bool", u"isText", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockMessage);
        return (obj).isText()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockMessage, self).__init__(u"quark.mock.MockMessage");
        (self).name = u"quark.mock.MockMessage"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([quark_mock_MockMessage_isBinary_Method(), quark_mock_MockMessage_isText_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockMessage.singleton = quark_mock_MockMessage()
class quark_mock_TextMessage_isText_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_TextMessage_isText_Method, self).__init__(u"quark.bool", u"isText", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.TextMessage);
        return (obj).isText()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_TextMessage_isBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_TextMessage_isBinary_Method, self).__init__(u"quark.bool", u"isBinary", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.TextMessage);
        return (obj).isBinary()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_TextMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_TextMessage, self).__init__(u"quark.mock.TextMessage");
        (self).name = u"quark.mock.TextMessage"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"text")])
        (self).methods = _List([quark_mock_TextMessage_isText_Method(), quark_mock_TextMessage_isBinary_Method()])
        (self).parents = _List([u"quark.mock.MockMessage"])

    def construct(self, args):
        return quark.mock.TextMessage(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_TextMessage.singleton = quark_mock_TextMessage()
class quark_mock_BinaryMessage_isText_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_BinaryMessage_isText_Method, self).__init__(u"quark.bool", u"isText", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.BinaryMessage);
        return (obj).isText()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_BinaryMessage_isBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_BinaryMessage_isBinary_Method, self).__init__(u"quark.bool", u"isBinary", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.BinaryMessage);
        return (obj).isBinary()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_BinaryMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_BinaryMessage, self).__init__(u"quark.mock.BinaryMessage");
        (self).name = u"quark.mock.BinaryMessage"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Buffer", u"bytes")])
        (self).methods = _List([quark_mock_BinaryMessage_isText_Method(), quark_mock_BinaryMessage_isBinary_Method()])
        (self).parents = _List([u"quark.mock.MockMessage"])

    def construct(self, args):
        return quark.mock.BinaryMessage((args)[0])

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_BinaryMessage.singleton = quark_mock_BinaryMessage()
class quark_mock_MockSocket_send_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockSocket_send_Method, self).__init__(u"quark.bool", u"send", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockSocket);
        return (obj).send(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockSocket_sendBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockSocket_sendBinary_Method, self).__init__(u"quark.bool", u"sendBinary", _List([u"quark.Buffer"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockSocket);
        return (obj).sendBinary((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockSocket_close_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockSocket_close_Method, self).__init__(u"quark.bool", u"close", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockSocket);
        return (obj).close()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockSocket(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockSocket, self).__init__(u"quark.mock.MockSocket");
        (self).name = u"quark.mock.MockSocket"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.List<quark.mock.MockMessage>", u"messages"), quark.reflect.Field(u"quark.bool", u"closed"), quark.reflect.Field(u"quark.WSHandler", u"handler")])
        (self).methods = _List([quark_mock_MockSocket_send_Method(), quark_mock_MockSocket_sendBinary_Method(), quark_mock_MockSocket_close_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.mock.MockSocket(_cast((args)[0], lambda: quark.WSHandler))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockSocket.singleton = quark_mock_MockSocket()
class quark_mock_RequestEvent_getType_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent_getType_Method, self).__init__(u"quark.String", u"getType", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.RequestEvent);
        return (obj).getType()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_RequestEvent_getArgs_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent_getArgs_Method, self).__init__(u"quark.List<quark.Object>", u"getArgs", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.RequestEvent);
        return (obj).getArgs()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_RequestEvent_respond_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent_respond_Method, self).__init__(u"quark.void", u"respond", _List([u"quark.int", u"quark.Map<quark.String,quark.String>", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.RequestEvent);
        (obj).respond(_cast((args)[0], lambda: int), _cast((args)[1], lambda: _Map), _cast((args)[2], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_RequestEvent_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.HTTPError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.RequestEvent);
        (obj).fail(_cast((args)[0], lambda: quark.HTTPError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_RequestEvent_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.RequestEvent);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_RequestEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_RequestEvent, self).__init__(u"quark.mock.RequestEvent");
        (self).name = u"quark.mock.RequestEvent"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.HTTPRequest", u"request"), quark.reflect.Field(u"quark.HTTPHandler", u"handler")])
        (self).methods = _List([quark_mock_RequestEvent_getType_Method(), quark_mock_RequestEvent_getArgs_Method(), quark_mock_RequestEvent_respond_Method(), quark_mock_RequestEvent_fail_Method(), quark_mock_RequestEvent_toString_Method()])
        (self).parents = _List([u"quark.mock.MockEvent"])

    def construct(self, args):
        return quark.mock.RequestEvent(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPHandler))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_RequestEvent.singleton = quark_mock_RequestEvent()
class quark_mock_MockResponse_getCode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_getCode_Method, self).__init__(u"quark.int", u"getCode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        return (obj).getCode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_setCode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_setCode_Method, self).__init__(u"quark.void", u"setCode", _List([u"quark.int"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        (obj).setCode(_cast((args)[0], lambda: int));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_getBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_getBody_Method, self).__init__(u"quark.String", u"getBody", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        return (obj).getBody()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_setBody_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_setBody_Method, self).__init__(u"quark.void", u"setBody", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        (obj).setBody(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_setHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_setHeader_Method, self).__init__(u"quark.void", u"setHeader", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        (obj).setHeader(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_getHeader_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_getHeader_Method, self).__init__(u"quark.String", u"getHeader", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        return (obj).getHeader(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse_getHeaders_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockResponse_getHeaders_Method, self).__init__(u"quark.List<quark.String>", u"getHeaders", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockResponse);
        return (obj).getHeaders()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockResponse(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockResponse, self).__init__(u"quark.mock.MockResponse");
        (self).name = u"quark.mock.MockResponse"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"code"), quark.reflect.Field(u"quark.String", u"body"), quark.reflect.Field(u"quark.Map<quark.String,quark.String>", u"headers")])
        (self).methods = _List([quark_mock_MockResponse_getCode_Method(), quark_mock_MockResponse_setCode_Method(), quark_mock_MockResponse_getBody_Method(), quark_mock_MockResponse_setBody_Method(), quark_mock_MockResponse_setHeader_Method(), quark_mock_MockResponse_getHeader_Method(), quark_mock_MockResponse_getHeaders_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.mock.MockResponse()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockResponse.singleton = quark_mock_MockResponse()
class quark_mock_MockTask(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockTask, self).__init__(u"quark.mock.MockTask");
        (self).name = u"quark.mock.MockTask"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Task", u"task"), quark.reflect.Field(u"quark.float", u"delay"), quark.reflect.Field(u"quark.long", u"_scheduledFor")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.mock.MockTask(_cast((args)[0], lambda: quark.Task), _cast((args)[1], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockTask.singleton = quark_mock_MockTask()
class quark_mock_MockRuntime_pump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_pump_Method, self).__init__(u"quark.void", u"pump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).pump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_open_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_open_Method, self).__init__(u"quark.void", u"open", _List([u"quark.String", u"quark.WSHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).open(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_request_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_request_Method, self).__init__(u"quark.void", u"request", _List([u"quark.HTTPRequest", u"quark.HTTPHandler"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).request(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPHandler));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_schedule_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_schedule_Method, self).__init__(u"quark.void", u"schedule", _List([u"quark.Task", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).schedule(_cast((args)[0], lambda: quark.Task), _cast((args)[1], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_codec_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_codec_Method, self).__init__(u"quark.Codec", u"codec", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        return (obj).codec()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_now_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_now_Method, self).__init__(u"quark.long", u"now", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        return (obj).now()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_advanceClock_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_advanceClock_Method, self).__init__(u"quark.void", u"advanceClock", _List([u"quark.long"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).advanceClock(_cast((args)[0], lambda: int));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_sleep_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_sleep_Method, self).__init__(u"quark.void", u"sleep", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).sleep(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_uuid_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_uuid_Method, self).__init__(u"quark.String", u"uuid", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        return (obj).uuid()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_serveHTTP_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_serveHTTP_Method, self).__init__(u"quark.void", u"serveHTTP", _List([u"quark.String", u"quark.HTTPServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).serveHTTP(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.HTTPServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_serveWS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_serveWS_Method, self).__init__(u"quark.void", u"serveWS", _List([u"quark.String", u"quark.WSServlet"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).serveWS(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.WSServlet));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_respond_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_respond_Method, self).__init__(u"quark.void", u"respond", _List([u"quark.HTTPRequest", u"quark.HTTPResponse"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).respond(_cast((args)[0], lambda: quark.HTTPRequest), _cast((args)[1], lambda: quark.HTTPResponse));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_fail_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_fail_Method, self).__init__(u"quark.void", u"fail", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        (obj).fail(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_logger_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_logger_Method, self).__init__(u"quark.Logger", u"logger", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        return (obj).logger(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime_callSafely_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime_callSafely_Method, self).__init__(u"quark.Object", u"callSafely", _List([u"quark.UnaryCallable", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntime);
        return (obj).callSafely(_cast((args)[0], lambda: quark.UnaryCallable), (args)[1])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntime(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockRuntime, self).__init__(u"quark.mock.MockRuntime");
        (self).name = u"quark.mock.MockRuntime"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Runtime", u"runtime"), quark.reflect.Field(u"quark.List<quark.mock.MockEvent>", u"events"), quark.reflect.Field(u"quark.List<quark.mock.MockTask>", u"tasks"), quark.reflect.Field(u"quark.List<quark.bool>", u"_executed_tasks"), quark.reflect.Field(u"quark.int", u"executed"), quark.reflect.Field(u"quark.long", u"_currentTime")])
        (self).methods = _List([quark_mock_MockRuntime_pump_Method(), quark_mock_MockRuntime_open_Method(), quark_mock_MockRuntime_request_Method(), quark_mock_MockRuntime_schedule_Method(), quark_mock_MockRuntime_codec_Method(), quark_mock_MockRuntime_now_Method(), quark_mock_MockRuntime_advanceClock_Method(), quark_mock_MockRuntime_sleep_Method(), quark_mock_MockRuntime_uuid_Method(), quark_mock_MockRuntime_serveHTTP_Method(), quark_mock_MockRuntime_serveWS_Method(), quark_mock_MockRuntime_respond_Method(), quark_mock_MockRuntime_fail_Method(), quark_mock_MockRuntime_logger_Method(), quark_mock_MockRuntime_callSafely_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.mock.MockRuntime(_cast((args)[0], lambda: quark.Runtime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockRuntime.singleton = quark_mock_MockRuntime()
class quark_mock_MockRuntimeTest_setup_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_setup_Method, self).__init__(u"quark.void", u"setup", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        (obj).setup();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_teardown_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_teardown_Method, self).__init__(u"quark.void", u"teardown", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        (obj).teardown();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_pump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_pump_Method, self).__init__(u"quark.void", u"pump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        (obj).pump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_expectNone_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_expectNone_Method, self).__init__(u"quark.int", u"expectNone", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        return (obj).expectNone()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_expectEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_expectEvent_Method, self).__init__(u"quark.mock.MockEvent", u"expectEvent", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        return (obj).expectEvent(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_expectRequest_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_expectRequest_Method, self).__init__(u"quark.mock.RequestEvent", u"expectRequest", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        return (obj).expectRequest(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest_expectSocket_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest_expectSocket_Method, self).__init__(u"quark.mock.SocketEvent", u"expectSocket", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: quark.mock.MockRuntimeTest);
        return (obj).expectSocket(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class quark_mock_MockRuntimeTest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_mock_MockRuntimeTest, self).__init__(u"quark.mock.MockRuntimeTest");
        (self).name = u"quark.mock.MockRuntimeTest"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.mock.MockRuntime", u"mock"), quark.reflect.Field(u"quark.concurrent.Context", u"old"), quark.reflect.Field(u"quark.int", u"expectIdx"), quark.reflect.Field(u"quark.Map<quark.String,quark.mock.SocketEvent>", u"sockets")])
        (self).methods = _List([quark_mock_MockRuntimeTest_setup_Method(), quark_mock_MockRuntimeTest_teardown_Method(), quark_mock_MockRuntimeTest_pump_Method(), quark_mock_MockRuntimeTest_expectNone_Method(), quark_mock_MockRuntimeTest_expectEvent_Method(), quark_mock_MockRuntimeTest_expectRequest_Method(), quark_mock_MockRuntimeTest_expectSocket_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.mock.MockRuntimeTest()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_mock_MockRuntimeTest.singleton = quark_mock_MockRuntimeTest()
class quark__ChainPromise(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__ChainPromise, self).__init__(u"quark._ChainPromise");
        (self).name = u"quark._ChainPromise"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Promise", u"_next")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._ChainPromise(_cast((args)[0], lambda: quark.Promise))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__ChainPromise.singleton = quark__ChainPromise()
class quark__CallbackEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__CallbackEvent, self).__init__(u"quark._CallbackEvent");
        (self).name = u"quark._CallbackEvent"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.UnaryCallable", u"_callable"), quark.reflect.Field(u"quark.Promise", u"_next"), quark.reflect.Field(u"quark.Object", u"_value"), quark.reflect.Field(u"quark._Callback", u"_callback")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._CallbackEvent(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: quark.Promise), (args)[2], _cast((args)[3], lambda: quark._Callback))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__CallbackEvent.singleton = quark__CallbackEvent()
class quark__Callback(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__Callback, self).__init__(u"quark._Callback");
        (self).name = u"quark._Callback"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Context", u"_context"), quark.reflect.Field(u"quark.UnaryCallable", u"_callable"), quark.reflect.Field(u"quark.Promise", u"_next")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.concurrent.EventContext"])

    def construct(self, args):
        return quark._Callback(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: quark.Promise))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__Callback.singleton = quark__Callback()
class quark__Passthrough(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__Passthrough, self).__init__(u"quark._Passthrough");
        (self).name = u"quark._Passthrough"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._Passthrough()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__Passthrough.singleton = quark__Passthrough()
class quark__CallIfIsInstance(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__CallIfIsInstance, self).__init__(u"quark._CallIfIsInstance");
        (self).name = u"quark._CallIfIsInstance"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.UnaryCallable", u"_underlying"), quark.reflect.Field(u"quark.reflect.Class", u"_class")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._CallIfIsInstance(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: quark.reflect.Class))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__CallIfIsInstance.singleton = quark__CallIfIsInstance()
class quark_PromiseValue(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_PromiseValue, self).__init__(u"quark.PromiseValue");
        (self).name = u"quark.PromiseValue"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Object", u"_successResult"), quark.reflect.Field(u"quark.error.Error", u"_failureResult"), quark.reflect.Field(u"quark.bool", u"_hasValue")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.PromiseValue((args)[0], _cast((args)[1], lambda: quark.error.Error), _cast((args)[2], lambda: bool))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_PromiseValue.singleton = quark_PromiseValue()
class quark_Promise(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_Promise, self).__init__(u"quark.Promise");
        (self).name = u"quark.Promise"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Lock", u"_lock"), quark.reflect.Field(u"quark.Object", u"_successResult"), quark.reflect.Field(u"quark.error.Error", u"_failureResult"), quark.reflect.Field(u"quark.bool", u"_hasResult"), quark.reflect.Field(u"quark.List<quark._Callback>", u"_successCallbacks"), quark.reflect.Field(u"quark.List<quark._Callback>", u"_failureCallbacks")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.Promise()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_Promise.singleton = quark_Promise()
class quark_PromiseFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_PromiseFactory, self).__init__(u"quark.PromiseFactory");
        (self).name = u"quark.PromiseFactory"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Promise", u"promise")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.PromiseFactory()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_PromiseFactory.singleton = quark_PromiseFactory()
class quark__BoundMethod(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__BoundMethod, self).__init__(u"quark._BoundMethod");
        (self).name = u"quark._BoundMethod"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Object", u"target"), quark.reflect.Field(u"quark.reflect.Method", u"method"), quark.reflect.Field(u"quark.List<quark.Object>", u"additionalArgs")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._BoundMethod((args)[0], _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: _List))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__BoundMethod.singleton = quark__BoundMethod()
class quark__IOScheduleTask(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__IOScheduleTask, self).__init__(u"quark._IOScheduleTask");
        (self).name = u"quark._IOScheduleTask"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.PromiseFactory", u"factory")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._IOScheduleTask(_cast((args)[0], lambda: quark.PromiseFactory))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__IOScheduleTask.singleton = quark__IOScheduleTask()
class quark__IOHTTPHandler(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark__IOHTTPHandler, self).__init__(u"quark._IOHTTPHandler");
        (self).name = u"quark._IOHTTPHandler"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.PromiseFactory", u"factory")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark._IOHTTPHandler(_cast((args)[0], lambda: quark.PromiseFactory))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark__IOHTTPHandler.singleton = quark__IOHTTPHandler()
class quark_IO(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(quark_IO, self).__init__(u"quark.IO");
        (self).name = u"quark.IO"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return quark.IO()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
quark_IO.singleton = quark_IO()
class mdk_runtime_Dependencies_registerService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_Dependencies_registerService_Method, self).__init__(u"quark.void", u"registerService", _List([u"quark.String", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.Dependencies);
        (obj).registerService(_cast((args)[0], lambda: unicode), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_Dependencies_getService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_Dependencies_getService_Method, self).__init__(u"quark.Object", u"getService", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.Dependencies);
        return (obj).getService(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_Dependencies_hasService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_Dependencies_hasService_Method, self).__init__(u"quark.bool", u"hasService", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.Dependencies);
        return (obj).hasService(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_Dependencies(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_Dependencies, self).__init__(u"mdk_runtime.Dependencies");
        (self).name = u"mdk_runtime.Dependencies"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Map<quark.String,quark.Object>", u"_services")])
        (self).methods = _List([mdk_runtime_Dependencies_registerService_Method(), mdk_runtime_Dependencies_getService_Method(), mdk_runtime_Dependencies_hasService_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.Dependencies()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_Dependencies.singleton = mdk_runtime_Dependencies()
class mdk_runtime_MDKRuntime_getTimeService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_getTimeService_Method, self).__init__(u"mdk_runtime.Time", u"getTimeService", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        return (obj).getTimeService()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime_getScheduleService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_getScheduleService_Method, self).__init__(u"mdk_runtime.actors.Actor", u"getScheduleService", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        return (obj).getScheduleService()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime_getWebSocketsService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_getWebSocketsService_Method, self).__init__(u"mdk_runtime.WebSockets", u"getWebSocketsService", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        return (obj).getWebSocketsService()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime_getFileService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_getFileService_Method, self).__init__(u"mdk_runtime.files.FileActor", u"getFileService", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        return (obj).getFileService()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime_getEnvVarsService_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_getEnvVarsService_Method, self).__init__(u"mdk_runtime.EnvironmentVariables", u"getEnvVarsService", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        return (obj).getEnvVarsService()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime_stop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime_stop_Method, self).__init__(u"quark.void", u"stop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.MDKRuntime);
        (obj).stop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_MDKRuntime(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_MDKRuntime, self).__init__(u"mdk_runtime.MDKRuntime");
        (self).name = u"mdk_runtime.MDKRuntime"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.Dependencies", u"dependencies"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher")])
        (self).methods = _List([mdk_runtime_MDKRuntime_getTimeService_Method(), mdk_runtime_MDKRuntime_getScheduleService_Method(), mdk_runtime_MDKRuntime_getWebSocketsService_Method(), mdk_runtime_MDKRuntime_getFileService_Method(), mdk_runtime_MDKRuntime_getEnvVarsService_Method(), mdk_runtime_MDKRuntime_stop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.MDKRuntime()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_MDKRuntime.singleton = mdk_runtime_MDKRuntime()
class mdk_runtime_Time_time_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_Time_time_Method, self).__init__(u"quark.float", u"time", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.Time);
        return (obj).time()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_Time(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_Time, self).__init__(u"mdk_runtime.Time");
        (self).name = u"mdk_runtime.Time"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_Time_time_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_Time.singleton = mdk_runtime_Time()
class mdk_runtime_SchedulingActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_SchedulingActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.SchedulingActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_SchedulingActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_SchedulingActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.SchedulingActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_SchedulingActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_SchedulingActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.SchedulingActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_SchedulingActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_SchedulingActor, self).__init__(u"mdk_runtime.SchedulingActor");
        (self).name = u"mdk_runtime.SchedulingActor"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_SchedulingActor_onStart_Method(), mdk_runtime_SchedulingActor_onStop_Method(), mdk_runtime_SchedulingActor_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_SchedulingActor.singleton = mdk_runtime_SchedulingActor()
class mdk_runtime_WebSockets_connect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WebSockets_connect_Method, self).__init__(u"mdk_runtime.promise.Promise", u"connect", _List([u"quark.String", u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WebSockets);
        return (obj).connect(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.actors.Actor))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WebSockets_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WebSockets_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WebSockets);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WebSockets_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WebSockets_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WebSockets);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WebSockets_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WebSockets_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WebSockets);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WebSockets(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WebSockets, self).__init__(u"mdk_runtime.WebSockets");
        (self).name = u"mdk_runtime.WebSockets"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_WebSockets_connect_Method(), mdk_runtime_WebSockets_onStart_Method(), mdk_runtime_WebSockets_onStop_Method(), mdk_runtime_WebSockets_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WebSockets.singleton = mdk_runtime_WebSockets()
class mdk_runtime_WSConnectError_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WSConnectError_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WSConnectError);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WSConnectError_getMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WSConnectError_getMessage_Method, self).__init__(u"quark.String", u"getMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WSConnectError);
        return (obj).getMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WSConnectError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WSConnectError, self).__init__(u"mdk_runtime.WSConnectError");
        (self).name = u"mdk_runtime.WSConnectError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"message")])
        (self).methods = _List([mdk_runtime_WSConnectError_toString_Method(), mdk_runtime_WSConnectError_getMessage_Method()])
        (self).parents = _List([u"quark.error.Error"])

    def construct(self, args):
        return mdk_runtime.WSConnectError(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WSConnectError.singleton = mdk_runtime_WSConnectError()
class mdk_runtime_WSActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WSActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WSActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WSActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WSActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WSActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WSActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_WSActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.WSActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_WSActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WSActor, self).__init__(u"mdk_runtime.WSActor");
        (self).name = u"mdk_runtime.WSActor"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_WSActor_onStart_Method(), mdk_runtime_WSActor_onStop_Method(), mdk_runtime_WSActor_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WSActor.singleton = mdk_runtime_WSActor()
class mdk_runtime_WSMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WSMessage, self).__init__(u"mdk_runtime.WSMessage");
        (self).name = u"mdk_runtime.WSMessage"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"body")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.WSMessage(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WSMessage.singleton = mdk_runtime_WSMessage()
class mdk_runtime_WSClose(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WSClose, self).__init__(u"mdk_runtime.WSClose");
        (self).name = u"mdk_runtime.WSClose"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.WSClose()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WSClose.singleton = mdk_runtime_WSClose()
class mdk_runtime_WSClosed(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_WSClosed, self).__init__(u"mdk_runtime.WSClosed");
        (self).name = u"mdk_runtime.WSClosed"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.WSClosed()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_WSClosed.singleton = mdk_runtime_WSClosed()
class mdk_runtime_QuarkRuntimeWSActor_logTS_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_logTS_Method, self).__init__(u"quark.void", u"logTS", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).logTS(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_logPrologue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_logPrologue_Method, self).__init__(u"quark.void", u"logPrologue", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).logPrologue(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSConnected(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSError_Method, self).__init__(u"quark.void", u"onWSError", _List([u"quark.WebSocket", u"quark.WSError"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSError(_cast((args)[0], lambda: quark.WebSocket), _cast((args)[1], lambda: quark.WSError));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSMessage_Method, self).__init__(u"quark.void", u"onWSMessage", _List([u"quark.WebSocket", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSMessage(_cast((args)[0], lambda: quark.WebSocket), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSFinal_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSFinal_Method, self).__init__(u"quark.void", u"onWSFinal", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSFinal(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSInit_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSInit_Method, self).__init__(u"quark.void", u"onWSInit", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSInit(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSBinary_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSBinary_Method, self).__init__(u"quark.void", u"onWSBinary", _List([u"quark.WebSocket", u"quark.Buffer"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSBinary(_cast((args)[0], lambda: quark.WebSocket), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor_onWSClosed_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor_onWSClosed_Method, self).__init__(u"quark.void", u"onWSClosed", _List([u"quark.WebSocket"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWSActor);
        (obj).onWSClosed(_cast((args)[0], lambda: quark.WebSocket));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWSActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWSActor, self).__init__(u"mdk_runtime.QuarkRuntimeWSActor");
        (self).name = u"mdk_runtime.QuarkRuntimeWSActor"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.WebSocket", u"socket"), quark.reflect.Field(u"mdk_runtime.promise.PromiseResolver", u"factory"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"originator"), quark.reflect.Field(u"quark.String", u"url"), quark.reflect.Field(u"quark.String", u"shortURL"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.String", u"state")])
        (self).methods = _List([mdk_runtime_QuarkRuntimeWSActor_logTS_Method(), mdk_runtime_QuarkRuntimeWSActor_logPrologue_Method(), mdk_runtime_QuarkRuntimeWSActor_onStart_Method(), mdk_runtime_QuarkRuntimeWSActor_onMessage_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSConnected_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSError_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSMessage_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSFinal_Method(), mdk_runtime_QuarkRuntimeWSActor_onStop_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSInit_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSBinary_Method(), mdk_runtime_QuarkRuntimeWSActor_onWSClosed_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.QuarkRuntimeWSActor(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.actors.Actor), _cast((args)[2], lambda: mdk_runtime.promise.PromiseResolver))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_QuarkRuntimeWSActor.singleton = mdk_runtime_QuarkRuntimeWSActor()
class mdk_runtime_QuarkRuntimeWebSockets_connect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWebSockets_connect_Method, self).__init__(u"mdk_runtime.promise.Promise", u"connect", _List([u"quark.String", u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWebSockets);
        return (obj).connect(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.actors.Actor))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWebSockets_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWebSockets_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWebSockets);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWebSockets_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWebSockets_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWebSockets);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWebSockets_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWebSockets_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeWebSockets);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeWebSockets(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeWebSockets, self).__init__(u"mdk_runtime.QuarkRuntimeWebSockets");
        (self).name = u"mdk_runtime.QuarkRuntimeWebSockets"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.List<mdk_runtime.WSActor>", u"connections")])
        (self).methods = _List([mdk_runtime_QuarkRuntimeWebSockets_connect_Method(), mdk_runtime_QuarkRuntimeWebSockets_onStart_Method(), mdk_runtime_QuarkRuntimeWebSockets_onMessage_Method(), mdk_runtime_QuarkRuntimeWebSockets_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.QuarkRuntimeWebSockets()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_QuarkRuntimeWebSockets.singleton = mdk_runtime_QuarkRuntimeWebSockets()
class mdk_runtime_FakeWSActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_accept_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_accept_Method, self).__init__(u"quark.void", u"accept", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).accept();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_reject_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_reject_Method, self).__init__(u"quark.void", u"reject", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).reject();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_send_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_send_Method, self).__init__(u"quark.void", u"send", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).send(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_close_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_close_Method, self).__init__(u"quark.void", u"close", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).close();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_expectTextMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_expectTextMessage_Method, self).__init__(u"quark.String", u"expectTextMessage", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        return (obj).expectTextMessage()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWSActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWSActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWSActor, self).__init__(u"mdk_runtime.FakeWSActor");
        (self).name = u"mdk_runtime.FakeWSActor"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"url"), quark.reflect.Field(u"mdk_runtime.promise.PromiseResolver", u"resolver"), quark.reflect.Field(u"quark.bool", u"resolved"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"originator"), quark.reflect.Field(u"quark.List<quark.String>", u"sent"), quark.reflect.Field(u"quark.String", u"state"), quark.reflect.Field(u"quark.int", u"expectIdx")])
        (self).methods = _List([mdk_runtime_FakeWSActor_onStart_Method(), mdk_runtime_FakeWSActor_onMessage_Method(), mdk_runtime_FakeWSActor_accept_Method(), mdk_runtime_FakeWSActor_reject_Method(), mdk_runtime_FakeWSActor_send_Method(), mdk_runtime_FakeWSActor_close_Method(), mdk_runtime_FakeWSActor_expectTextMessage_Method(), mdk_runtime_FakeWSActor_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.FakeWSActor(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.promise.PromiseResolver), _cast((args)[2], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_FakeWSActor.singleton = mdk_runtime_FakeWSActor()
class mdk_runtime_FakeWebSockets_connect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets_connect_Method, self).__init__(u"mdk_runtime.promise.Promise", u"connect", _List([u"quark.String", u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWebSockets);
        return (obj).connect(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.actors.Actor))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWebSockets_lastConnection_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets_lastConnection_Method, self).__init__(u"mdk_runtime.FakeWSActor", u"lastConnection", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWebSockets);
        return (obj).lastConnection()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWebSockets_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWebSockets);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWebSockets_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWebSockets);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWebSockets_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeWebSockets);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeWebSockets(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_FakeWebSockets, self).__init__(u"mdk_runtime.FakeWebSockets");
        (self).name = u"mdk_runtime.FakeWebSockets"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.List<mdk_runtime.FakeWSActor>", u"fakeActors")])
        (self).methods = _List([mdk_runtime_FakeWebSockets_connect_Method(), mdk_runtime_FakeWebSockets_lastConnection_Method(), mdk_runtime_FakeWebSockets_onStart_Method(), mdk_runtime_FakeWebSockets_onMessage_Method(), mdk_runtime_FakeWebSockets_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.FakeWebSockets()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_FakeWebSockets.singleton = mdk_runtime_FakeWebSockets()
class mdk_runtime_Schedule(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_Schedule, self).__init__(u"mdk_runtime.Schedule");
        (self).name = u"mdk_runtime.Schedule"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"event"), quark.reflect.Field(u"quark.float", u"seconds")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.Schedule(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_Schedule.singleton = mdk_runtime_Schedule()
class mdk_runtime_Happening(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_Happening, self).__init__(u"mdk_runtime.Happening");
        (self).name = u"mdk_runtime.Happening"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"event"), quark.reflect.Field(u"quark.float", u"currentTime")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.Happening(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_Happening.singleton = mdk_runtime_Happening()
class mdk_runtime__ScheduleTask_onExecute_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime__ScheduleTask_onExecute_Method, self).__init__(u"quark.void", u"onExecute", _List([u"quark.Runtime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime._ScheduleTask);
        (obj).onExecute(_cast((args)[0], lambda: quark.Runtime));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime__ScheduleTask(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime__ScheduleTask, self).__init__(u"mdk_runtime._ScheduleTask");
        (self).name = u"mdk_runtime._ScheduleTask"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.QuarkRuntimeTime", u"timeService"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"requester"), quark.reflect.Field(u"quark.String", u"event")])
        (self).methods = _List([mdk_runtime__ScheduleTask_onExecute_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime._ScheduleTask(_cast((args)[0], lambda: mdk_runtime.QuarkRuntimeTime), _cast((args)[1], lambda: mdk_runtime.actors.Actor), _cast((args)[2], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime__ScheduleTask.singleton = mdk_runtime__ScheduleTask()
class mdk_runtime_QuarkRuntimeTime_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeTime_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeTime);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeTime_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeTime_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeTime);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeTime_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeTime_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeTime);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeTime_time_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeTime_time_Method, self).__init__(u"quark.float", u"time", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.QuarkRuntimeTime);
        return (obj).time()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_QuarkRuntimeTime(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_QuarkRuntimeTime, self).__init__(u"mdk_runtime.QuarkRuntimeTime");
        (self).name = u"mdk_runtime.QuarkRuntimeTime"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.bool", u"stopped")])
        (self).methods = _List([mdk_runtime_QuarkRuntimeTime_onStart_Method(), mdk_runtime_QuarkRuntimeTime_onStop_Method(), mdk_runtime_QuarkRuntimeTime_onMessage_Method(), mdk_runtime_QuarkRuntimeTime_time_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.QuarkRuntimeTime()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_QuarkRuntimeTime.singleton = mdk_runtime_QuarkRuntimeTime()
class mdk_runtime__FakeTimeRequest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime__FakeTimeRequest, self).__init__(u"mdk_runtime._FakeTimeRequest");
        (self).name = u"mdk_runtime._FakeTimeRequest"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"requester"), quark.reflect.Field(u"quark.String", u"event"), quark.reflect.Field(u"quark.float", u"happensAt")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime._FakeTimeRequest(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime__FakeTimeRequest.singleton = mdk_runtime__FakeTimeRequest()
class mdk_runtime_FakeTime_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_time_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_time_Method, self).__init__(u"quark.float", u"time", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        return (obj).time()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_pump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_pump_Method, self).__init__(u"quark.void", u"pump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        (obj).pump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_advance_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_advance_Method, self).__init__(u"quark.void", u"advance", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        (obj).advance(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_scheduled_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_scheduled_Method, self).__init__(u"quark.int", u"scheduled", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        return (obj).scheduled()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeTime);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeTime(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_FakeTime, self).__init__(u"mdk_runtime.FakeTime");
        (self).name = u"mdk_runtime.FakeTime"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.float", u"_now"), quark.reflect.Field(u"quark.Map<quark.long,mdk_runtime._FakeTimeRequest>", u"_scheduled"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher")])
        (self).methods = _List([mdk_runtime_FakeTime_onStart_Method(), mdk_runtime_FakeTime_onMessage_Method(), mdk_runtime_FakeTime_time_Method(), mdk_runtime_FakeTime_pump_Method(), mdk_runtime_FakeTime_advance_Method(), mdk_runtime_FakeTime_scheduled_Method(), mdk_runtime_FakeTime_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.FakeTime()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_FakeTime.singleton = mdk_runtime_FakeTime()
class mdk_runtime_EnvironmentVariable_isDefined_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariable_isDefined_Method, self).__init__(u"quark.bool", u"isDefined", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.EnvironmentVariable);
        return (obj).isDefined()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_EnvironmentVariable_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariable_get_Method, self).__init__(u"quark.String", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.EnvironmentVariable);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_EnvironmentVariable_orElseGet_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariable_orElseGet_Method, self).__init__(u"quark.String", u"orElseGet", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.EnvironmentVariable);
        return (obj).orElseGet(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_EnvironmentVariable(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariable, self).__init__(u"mdk_runtime.EnvironmentVariable");
        (self).name = u"mdk_runtime.EnvironmentVariable"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"variableName"), quark.reflect.Field(u"quark.String", u"_value")])
        (self).methods = _List([mdk_runtime_EnvironmentVariable_isDefined_Method(), mdk_runtime_EnvironmentVariable_get_Method(), mdk_runtime_EnvironmentVariable_orElseGet_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.EnvironmentVariable(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_EnvironmentVariable.singleton = mdk_runtime_EnvironmentVariable()
class mdk_runtime_EnvironmentVariables_var_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariables_var_Method, self).__init__(u"mdk_runtime.EnvironmentVariable", u"var", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.EnvironmentVariables);
        return (obj).var(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_EnvironmentVariables(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_EnvironmentVariables, self).__init__(u"mdk_runtime.EnvironmentVariables");
        (self).name = u"mdk_runtime.EnvironmentVariables"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_EnvironmentVariables_var_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_EnvironmentVariables.singleton = mdk_runtime_EnvironmentVariables()
class mdk_runtime_RealEnvVars_var_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_RealEnvVars_var_Method, self).__init__(u"mdk_runtime.EnvironmentVariable", u"var", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.RealEnvVars);
        return (obj).var(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_RealEnvVars(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_RealEnvVars, self).__init__(u"mdk_runtime.RealEnvVars");
        (self).name = u"mdk_runtime.RealEnvVars"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_RealEnvVars_var_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.RealEnvVars()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_RealEnvVars.singleton = mdk_runtime_RealEnvVars()
class mdk_runtime_FakeEnvVars_set_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeEnvVars_set_Method, self).__init__(u"quark.void", u"set", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeEnvVars);
        (obj).set(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeEnvVars_var_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_FakeEnvVars_var_Method, self).__init__(u"mdk_runtime.EnvironmentVariable", u"var", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.FakeEnvVars);
        return (obj).var(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_FakeEnvVars(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_FakeEnvVars, self).__init__(u"mdk_runtime.FakeEnvVars");
        (self).name = u"mdk_runtime.FakeEnvVars"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Map<quark.String,quark.String>", u"env")])
        (self).methods = _List([mdk_runtime_FakeEnvVars_set_Method(), mdk_runtime_FakeEnvVars_var_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.FakeEnvVars()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_FakeEnvVars.singleton = mdk_runtime_FakeEnvVars()
class mdk_runtime_actors_Actor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_Actor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.Actor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_Actor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_Actor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.Actor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_Actor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_Actor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.Actor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_Actor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_actors_Actor, self).__init__(u"mdk_runtime.actors.Actor");
        (self).name = u"mdk_runtime.actors.Actor"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_actors_Actor_onStart_Method(), mdk_runtime_actors_Actor_onStop_Method(), mdk_runtime_actors_Actor_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_actors_Actor.singleton = mdk_runtime_actors_Actor()
class mdk_runtime_actors__QueuedMessage_deliver_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors__QueuedMessage_deliver_Method, self).__init__(u"quark.void", u"deliver", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors._QueuedMessage);
        (obj).deliver();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors__QueuedMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_actors__QueuedMessage, self).__init__(u"mdk_runtime.actors._QueuedMessage");
        (self).name = u"mdk_runtime.actors._QueuedMessage"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_actors__QueuedMessage_deliver_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_actors__QueuedMessage.singleton = mdk_runtime_actors__QueuedMessage()
class mdk_runtime_actors__InFlightMessage_deliver_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors__InFlightMessage_deliver_Method, self).__init__(u"quark.void", u"deliver", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors._InFlightMessage);
        (obj).deliver();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors__InFlightMessage_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors__InFlightMessage_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors._InFlightMessage);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors__InFlightMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_actors__InFlightMessage, self).__init__(u"mdk_runtime.actors._InFlightMessage");
        (self).name = u"mdk_runtime.actors._InFlightMessage"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"origin"), quark.reflect.Field(u"quark.Object", u"msg"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"destination")])
        (self).methods = _List([mdk_runtime_actors__InFlightMessage_deliver_Method(), mdk_runtime_actors__InFlightMessage_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.actors._InFlightMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1], _cast((args)[2], lambda: mdk_runtime.actors.Actor))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_actors__InFlightMessage.singleton = mdk_runtime_actors__InFlightMessage()
class mdk_runtime_actors__StartStopActor_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors__StartStopActor_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors._StartStopActor);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors__StartStopActor_deliver_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors__StartStopActor_deliver_Method, self).__init__(u"quark.void", u"deliver", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors._StartStopActor);
        (obj).deliver();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors__StartStopActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_actors__StartStopActor, self).__init__(u"mdk_runtime.actors._StartStopActor");
        (self).name = u"mdk_runtime.actors._StartStopActor"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"actor"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.bool", u"start")])
        (self).methods = _List([mdk_runtime_actors__StartStopActor_toString_Method(), mdk_runtime_actors__StartStopActor_deliver_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.actors._StartStopActor(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.actors.MessageDispatcher), _cast((args)[2], lambda: bool))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_actors__StartStopActor.singleton = mdk_runtime_actors__StartStopActor()
class mdk_runtime_actors_MessageDispatcher_tell_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher_tell_Method, self).__init__(u"quark.void", u"tell", _List([u"mdk_runtime.actors.Actor", u"quark.Object", u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.MessageDispatcher);
        (obj).tell(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1], _cast((args)[2], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_MessageDispatcher_startActor_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher_startActor_Method, self).__init__(u"quark.void", u"startActor", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.MessageDispatcher);
        (obj).startActor(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_MessageDispatcher_stopActor_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher_stopActor_Method, self).__init__(u"quark.void", u"stopActor", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.MessageDispatcher);
        (obj).stopActor(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_MessageDispatcher__callQueuedMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher__callQueuedMessage_Method, self).__init__(u"quark.bool", u"_callQueuedMessage", _List([u"quark.Object", u"mdk_runtime.actors._QueuedMessage"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.MessageDispatcher);
        return (obj)._callQueuedMessage((args)[0], _cast((args)[1], lambda: mdk_runtime.actors._QueuedMessage))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_MessageDispatcher__queue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher__queue_Method, self).__init__(u"quark.void", u"_queue", _List([u"mdk_runtime.actors._QueuedMessage"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.actors.MessageDispatcher);
        (obj)._queue(_cast((args)[0], lambda: mdk_runtime.actors._QueuedMessage));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_actors_MessageDispatcher(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_actors_MessageDispatcher, self).__init__(u"mdk_runtime.actors.MessageDispatcher");
        (self).name = u"mdk_runtime.actors.MessageDispatcher"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.List<mdk_runtime.actors._QueuedMessage>", u"_queued"), quark.reflect.Field(u"quark.bool", u"_delivering"), quark.reflect.Field(u"quark.concurrent.Lock", u"_lock")])
        (self).methods = _List([mdk_runtime_actors_MessageDispatcher_tell_Method(), mdk_runtime_actors_MessageDispatcher_startActor_Method(), mdk_runtime_actors_MessageDispatcher_stopActor_Method(), mdk_runtime_actors_MessageDispatcher__callQueuedMessage_Method(), mdk_runtime_actors_MessageDispatcher__queue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.actors.MessageDispatcher()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_actors_MessageDispatcher.singleton = mdk_runtime_actors_MessageDispatcher()
class mdk_runtime_promise__ChainPromise_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise__ChainPromise_call_Method, self).__init__(u"quark.Object", u"call", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise._ChainPromise);
        return (obj).call((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise__ChainPromise(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise__ChainPromise, self).__init__(u"mdk_runtime.promise._ChainPromise");
        (self).name = u"mdk_runtime.promise._ChainPromise"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.promise.Promise", u"_next")])
        (self).methods = _List([mdk_runtime_promise__ChainPromise_call_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise._ChainPromise(_cast((args)[0], lambda: mdk_runtime.promise.Promise))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise__ChainPromise.singleton = mdk_runtime_promise__ChainPromise()
class mdk_runtime_promise__CallbackEvent_deliver_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise__CallbackEvent_deliver_Method, self).__init__(u"quark.void", u"deliver", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise._CallbackEvent);
        (obj).deliver();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise__CallbackEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise__CallbackEvent, self).__init__(u"mdk_runtime.promise._CallbackEvent");
        (self).name = u"mdk_runtime.promise._CallbackEvent"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.UnaryCallable", u"_callable"), quark.reflect.Field(u"mdk_runtime.promise.Promise", u"_next"), quark.reflect.Field(u"quark.Object", u"_value")])
        (self).methods = _List([mdk_runtime_promise__CallbackEvent_deliver_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise._CallbackEvent(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: mdk_runtime.promise.Promise), (args)[2])

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise__CallbackEvent.singleton = mdk_runtime_promise__CallbackEvent()
class mdk_runtime_promise__Callback_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise__Callback_call_Method, self).__init__(u"quark.void", u"call", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise._Callback);
        (obj).call((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise__Callback(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise__Callback, self).__init__(u"mdk_runtime.promise._Callback");
        (self).name = u"mdk_runtime.promise._Callback"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.UnaryCallable", u"_callable"), quark.reflect.Field(u"mdk_runtime.promise.Promise", u"_next")])
        (self).methods = _List([mdk_runtime_promise__Callback_call_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise._Callback(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: mdk_runtime.promise.Promise))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise__Callback.singleton = mdk_runtime_promise__Callback()
class mdk_runtime_promise__Passthrough_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise__Passthrough_call_Method, self).__init__(u"quark.Object", u"call", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise._Passthrough);
        return (obj).call((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise__Passthrough(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise__Passthrough, self).__init__(u"mdk_runtime.promise._Passthrough");
        (self).name = u"mdk_runtime.promise._Passthrough"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_promise__Passthrough_call_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise._Passthrough()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise__Passthrough.singleton = mdk_runtime_promise__Passthrough()
class mdk_runtime_promise__CallIfIsInstance_call_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise__CallIfIsInstance_call_Method, self).__init__(u"quark.Object", u"call", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise._CallIfIsInstance);
        return (obj).call((args)[0])

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise__CallIfIsInstance(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise__CallIfIsInstance, self).__init__(u"mdk_runtime.promise._CallIfIsInstance");
        (self).name = u"mdk_runtime.promise._CallIfIsInstance"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.UnaryCallable", u"_underlying"), quark.reflect.Field(u"quark.reflect.Class", u"_class")])
        (self).methods = _List([mdk_runtime_promise__CallIfIsInstance_call_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise._CallIfIsInstance(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: quark.reflect.Class))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise__CallIfIsInstance.singleton = mdk_runtime_promise__CallIfIsInstance()
class mdk_runtime_promise_PromiseValue_hasValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseValue_hasValue_Method, self).__init__(u"quark.bool", u"hasValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.PromiseValue);
        return (obj).hasValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_PromiseValue_isError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseValue_isError_Method, self).__init__(u"quark.bool", u"isError", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.PromiseValue);
        return (obj).isError()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_PromiseValue_getValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseValue_getValue_Method, self).__init__(u"quark.Object", u"getValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.PromiseValue);
        return (obj).getValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_PromiseValue(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseValue, self).__init__(u"mdk_runtime.promise.PromiseValue");
        (self).name = u"mdk_runtime.promise.PromiseValue"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Object", u"_successResult"), quark.reflect.Field(u"quark.error.Error", u"_failureResult"), quark.reflect.Field(u"quark.bool", u"_hasValue")])
        (self).methods = _List([mdk_runtime_promise_PromiseValue_hasValue_Method(), mdk_runtime_promise_PromiseValue_isError_Method(), mdk_runtime_promise_PromiseValue_getValue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise.PromiseValue((args)[0], _cast((args)[1], lambda: quark.error.Error), _cast((args)[2], lambda: bool))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise_PromiseValue.singleton = mdk_runtime_promise_PromiseValue()
class mdk_runtime_promise_Promise__maybeRunCallbacks_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise__maybeRunCallbacks_Method, self).__init__(u"quark.void", u"_maybeRunCallbacks", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        (obj)._maybeRunCallbacks();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise__resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise__resolve_Method, self).__init__(u"quark.void", u"_resolve", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        (obj)._resolve((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise__reject_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise__reject_Method, self).__init__(u"quark.void", u"_reject", _List([u"quark.error.Error"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        (obj)._reject(_cast((args)[0], lambda: quark.error.Error));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise_andThen_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise_andThen_Method, self).__init__(u"mdk_runtime.promise.Promise", u"andThen", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        return (obj).andThen(_cast((args)[0], lambda: quark.UnaryCallable))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise_andCatch_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise_andCatch_Method, self).__init__(u"mdk_runtime.promise.Promise", u"andCatch", _List([u"quark.reflect.Class", u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        return (obj).andCatch(_cast((args)[0], lambda: quark.reflect.Class), _cast((args)[1], lambda: quark.UnaryCallable))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise_andFinally_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise_andFinally_Method, self).__init__(u"mdk_runtime.promise.Promise", u"andFinally", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        return (obj).andFinally(_cast((args)[0], lambda: quark.UnaryCallable))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise_andEither_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise_andEither_Method, self).__init__(u"mdk_runtime.promise.Promise", u"andEither", _List([u"quark.UnaryCallable", u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        return (obj).andEither(_cast((args)[0], lambda: quark.UnaryCallable), _cast((args)[1], lambda: quark.UnaryCallable))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise_value_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise_value_Method, self).__init__(u"mdk_runtime.promise.PromiseValue", u"value", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.Promise);
        return (obj).value()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_Promise(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise_Promise, self).__init__(u"mdk_runtime.promise.Promise");
        (self).name = u"mdk_runtime.promise.Promise"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Lock", u"_lock"), quark.reflect.Field(u"quark.Object", u"_successResult"), quark.reflect.Field(u"quark.error.Error", u"_failureResult"), quark.reflect.Field(u"quark.bool", u"_hasResult"), quark.reflect.Field(u"quark.List<mdk_runtime.promise._Callback>", u"_successCallbacks"), quark.reflect.Field(u"quark.List<mdk_runtime.promise._Callback>", u"_failureCallbacks"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"_dispatcher")])
        (self).methods = _List([mdk_runtime_promise_Promise__maybeRunCallbacks_Method(), mdk_runtime_promise_Promise__resolve_Method(), mdk_runtime_promise_Promise__reject_Method(), mdk_runtime_promise_Promise_andThen_Method(), mdk_runtime_promise_Promise_andCatch_Method(), mdk_runtime_promise_Promise_andFinally_Method(), mdk_runtime_promise_Promise_andEither_Method(), mdk_runtime_promise_Promise_value_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise.Promise(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise_Promise.singleton = mdk_runtime_promise_Promise()
class mdk_runtime_promise_PromiseResolver_resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseResolver_resolve_Method, self).__init__(u"quark.void", u"resolve", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.PromiseResolver);
        (obj).resolve((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_PromiseResolver_reject_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseResolver_reject_Method, self).__init__(u"quark.void", u"reject", _List([u"quark.error.Error"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.promise.PromiseResolver);
        (obj).reject(_cast((args)[0], lambda: quark.error.Error));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_promise_PromiseResolver(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_promise_PromiseResolver, self).__init__(u"mdk_runtime.promise.PromiseResolver");
        (self).name = u"mdk_runtime.promise.PromiseResolver"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.promise.Promise", u"promise")])
        (self).methods = _List([mdk_runtime_promise_PromiseResolver_resolve_Method(), mdk_runtime_promise_PromiseResolver_reject_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.promise.PromiseResolver(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_promise_PromiseResolver.singleton = mdk_runtime_promise_PromiseResolver()
class mdk_runtime_files_SubscribeChanges(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files_SubscribeChanges, self).__init__(u"mdk_runtime.files.SubscribeChanges");
        (self).name = u"mdk_runtime.files.SubscribeChanges"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"path")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.files.SubscribeChanges(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files_SubscribeChanges.singleton = mdk_runtime_files_SubscribeChanges()
class mdk_runtime_files_FileContents(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileContents, self).__init__(u"mdk_runtime.files.FileContents");
        (self).name = u"mdk_runtime.files.FileContents"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"path"), quark.reflect.Field(u"quark.String", u"contents")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.files.FileContents(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files_FileContents.singleton = mdk_runtime_files_FileContents()
class mdk_runtime_files_FileDeleted(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileDeleted, self).__init__(u"mdk_runtime.files.FileDeleted");
        (self).name = u"mdk_runtime.files.FileDeleted"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"path")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.files.FileDeleted(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files_FileDeleted.singleton = mdk_runtime_files_FileDeleted()
class mdk_runtime_files_FileActor_mktempdir_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_mktempdir_Method, self).__init__(u"quark.String", u"mktempdir", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        return (obj).mktempdir()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor_write_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_write_Method, self).__init__(u"quark.void", u"write", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        (obj).write(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor_delete_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_delete_Method, self).__init__(u"quark.void", u"delete", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        (obj).delete(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActor, self).__init__(u"mdk_runtime.files.FileActor");
        (self).name = u"mdk_runtime.files.FileActor"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_runtime_files_FileActor_mktempdir_Method(), mdk_runtime_files_FileActor_write_Method(), mdk_runtime_files_FileActor_delete_Method(), mdk_runtime_files_FileActor_onStart_Method(), mdk_runtime_files_FileActor_onStop_Method(), mdk_runtime_files_FileActor_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files_FileActor.singleton = mdk_runtime_files_FileActor()
class mdk_runtime_files_FileActorImpl_mktempdir_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_mktempdir_Method, self).__init__(u"quark.String", u"mktempdir", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        return (obj).mktempdir()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl_write_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_write_Method, self).__init__(u"quark.void", u"write", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj).write(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl_delete_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_delete_Method, self).__init__(u"quark.void", u"delete", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj).delete(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl__checkSubscriptions_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl__checkSubscriptions_Method, self).__init__(u"quark.void", u"_checkSubscriptions", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj)._checkSubscriptions();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl__send_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl__send_Method, self).__init__(u"quark.void", u"_send", _List([u"quark.Object", u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files.FileActorImpl);
        (obj)._send((args)[0], _cast((args)[1], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files_FileActorImpl(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files_FileActorImpl, self).__init__(u"mdk_runtime.files.FileActorImpl");
        (self).name = u"mdk_runtime.files.FileActorImpl"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"scheduling"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.List<mdk_runtime.files._Subscription>", u"subscriptions"), quark.reflect.Field(u"quark.bool", u"stopped")])
        (self).methods = _List([mdk_runtime_files_FileActorImpl_mktempdir_Method(), mdk_runtime_files_FileActorImpl_write_Method(), mdk_runtime_files_FileActorImpl_delete_Method(), mdk_runtime_files_FileActorImpl__checkSubscriptions_Method(), mdk_runtime_files_FileActorImpl_onStart_Method(), mdk_runtime_files_FileActorImpl_onStop_Method(), mdk_runtime_files_FileActorImpl_onMessage_Method(), mdk_runtime_files_FileActorImpl__send_Method()])
        (self).parents = _List([u"mdk_runtime.files.FileActor"])

    def construct(self, args):
        return mdk_runtime.files.FileActorImpl(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files_FileActorImpl.singleton = mdk_runtime_files_FileActorImpl()
class mdk_runtime_files__Subscription_poll_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_runtime_files__Subscription_poll_Method, self).__init__(u"quark.void", u"poll", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_runtime.files._Subscription);
        (obj).poll();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_runtime_files__Subscription(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_runtime_files__Subscription, self).__init__(u"mdk_runtime.files._Subscription");
        (self).name = u"mdk_runtime.files._Subscription"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"path"), quark.reflect.Field(u"mdk_runtime.files.FileActorImpl", u"actor"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"subscriber"), quark.reflect.Field(u"quark.List<quark.String>", u"previous_listing")])
        (self).methods = _List([mdk_runtime_files__Subscription_poll_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_runtime.files._Subscription(_cast((args)[0], lambda: mdk_runtime.files.FileActorImpl), _cast((args)[1], lambda: mdk_runtime.actors.Actor), _cast((args)[2], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_runtime_files__Subscription.singleton = mdk_runtime_files__Subscription()
class mdk_util_WaitForPromise__finished_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_util_WaitForPromise__finished_Method, self).__init__(u"quark.bool", u"_finished", _List([u"quark.Object", u"quark.concurrent.Condition"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_util.WaitForPromise);
        return (obj)._finished((args)[0], _cast((args)[1], lambda: _Condition))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_util_WaitForPromise_wait_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_util_WaitForPromise_wait_Method, self).__init__(u"quark.Object", u"wait", _List([u"mdk_runtime.promise.Promise", u"quark.float", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_util.WaitForPromise);
        return mdk_util.WaitForPromise.wait(_cast((args)[0], lambda: mdk_runtime.promise.Promise), _cast((args)[1], lambda: float), _cast((args)[2], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_util_WaitForPromise(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_util_WaitForPromise, self).__init__(u"mdk_util.WaitForPromise");
        (self).name = u"mdk_util.WaitForPromise"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_util_WaitForPromise__finished_Method(), mdk_util_WaitForPromise_wait_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_util.WaitForPromise()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_util_WaitForPromise.singleton = mdk_util_WaitForPromise()
class mdk_introspection_Supplier_quark_Object__get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_Supplier_quark_Object__get_Method, self).__init__(u"quark.Object", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.Supplier);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_Supplier_quark_Object_(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_Supplier_quark_Object_, self).__init__(u"mdk_introspection.Supplier<quark.Object>");
        (self).name = u"mdk_introspection.Supplier"
        (self).parameters = _List([u"quark.Object"])
        (self).fields = _List([])
        (self).methods = _List([mdk_introspection_Supplier_quark_Object__get_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_Supplier_quark_Object_.singleton = mdk_introspection_Supplier_quark_Object_()
class mdk_introspection_DatawireToken_getToken_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_DatawireToken_getToken_Method, self).__init__(u"quark.String", u"getToken", _List([u"mdk_runtime.EnvironmentVariables"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.DatawireToken);
        return mdk_introspection.DatawireToken.getToken(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_DatawireToken(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_DatawireToken, self).__init__(u"mdk_introspection.DatawireToken");
        (self).name = u"mdk_introspection.DatawireToken"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"TOKEN_VARIABLE_NAME")])
        (self).methods = _List([mdk_introspection_DatawireToken_getToken_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_introspection.DatawireToken()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_DatawireToken.singleton = mdk_introspection_DatawireToken()
class mdk_introspection_Platform_platformType_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_Platform_platformType_Method, self).__init__(u"quark.String", u"platformType", _List([u"mdk_runtime.EnvironmentVariables"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.Platform);
        return mdk_introspection.Platform.platformType(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_Platform_getRoutableHost_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_Platform_getRoutableHost_Method, self).__init__(u"quark.String", u"getRoutableHost", _List([u"mdk_runtime.EnvironmentVariables"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.Platform);
        return mdk_introspection.Platform.getRoutableHost(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_Platform_getRoutablePort_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_Platform_getRoutablePort_Method, self).__init__(u"quark.int", u"getRoutablePort", _List([u"mdk_runtime.EnvironmentVariables", u"quark.int"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.Platform);
        return mdk_introspection.Platform.getRoutablePort(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables), _cast((args)[1], lambda: int))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_Platform(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_Platform, self).__init__(u"mdk_introspection.Platform");
        (self).name = u"mdk_introspection.Platform"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"PLATFORM_TYPE_VARIABLE_NAME"), quark.reflect.Field(u"quark.String", u"PLATFORM_TYPE_EC2"), quark.reflect.Field(u"quark.String", u"PLATFORM_TYPE_GOOGLE_COMPUTE"), quark.reflect.Field(u"quark.String", u"PLATFORM_TYPE_GOOGLE_CONTAINER"), quark.reflect.Field(u"quark.String", u"PLATFORM_TYPE_KUBERNETES"), quark.reflect.Field(u"quark.String", u"ROUTABLE_HOST_VARIABLE_NAME"), quark.reflect.Field(u"quark.String", u"ROUTABLE_PORT_VARIABLE_NAME")])
        (self).methods = _List([mdk_introspection_Platform_platformType_Method(), mdk_introspection_Platform_getRoutableHost_Method(), mdk_introspection_Platform_getRoutablePort_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_introspection.Platform()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_Platform.singleton = mdk_introspection_Platform()
class mdk_introspection_aws_Ec2Host_metadataHost_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_aws_Ec2Host_metadataHost_Method, self).__init__(u"quark.String", u"metadataHost", _List([u"mdk_runtime.EnvironmentVariables"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.aws.Ec2Host);
        return mdk_introspection.aws.Ec2Host.metadataHost(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_aws_Ec2Host_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_aws_Ec2Host_get_Method, self).__init__(u"quark.String", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.aws.Ec2Host);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_aws_Ec2Host(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_aws_Ec2Host, self).__init__(u"mdk_introspection.aws.Ec2Host");
        (self).name = u"mdk_introspection.aws.Ec2Host"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"scope"), quark.reflect.Field(u"mdk_runtime.EnvironmentVariables", u"env")])
        (self).methods = _List([mdk_introspection_aws_Ec2Host_metadataHost_Method(), mdk_introspection_aws_Ec2Host_get_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_introspection.aws.Ec2Host(_cast((args)[0], lambda: mdk_runtime.EnvironmentVariables), _cast((args)[1], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_aws_Ec2Host.singleton = mdk_introspection_aws_Ec2Host()
class mdk_introspection_kubernetes_KubernetesHost_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_kubernetes_KubernetesHost_get_Method, self).__init__(u"quark.String", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.kubernetes.KubernetesHost);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_kubernetes_KubernetesHost(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_kubernetes_KubernetesHost, self).__init__(u"mdk_introspection.kubernetes.KubernetesHost");
        (self).name = u"mdk_introspection.kubernetes.KubernetesHost"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_introspection_kubernetes_KubernetesHost_get_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_introspection.kubernetes.KubernetesHost()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_kubernetes_KubernetesHost.singleton = mdk_introspection_kubernetes_KubernetesHost()
class mdk_introspection_kubernetes_KubernetesPort_get_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_introspection_kubernetes_KubernetesPort_get_Method, self).__init__(u"quark.int", u"get", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_introspection.kubernetes.KubernetesPort);
        return (obj).get()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_introspection_kubernetes_KubernetesPort(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_introspection_kubernetes_KubernetesPort, self).__init__(u"mdk_introspection.kubernetes.KubernetesPort");
        (self).name = u"mdk_introspection.kubernetes.KubernetesPort"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_introspection_kubernetes_KubernetesPort_get_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_introspection.kubernetes.KubernetesPort()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_introspection_kubernetes_KubernetesPort.singleton = mdk_introspection_kubernetes_KubernetesPort()
class mdk_discovery_NodeActive(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_NodeActive, self).__init__(u"mdk_discovery.NodeActive");
        (self).name = u"mdk_discovery.NodeActive"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_discovery.Node", u"node")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.NodeActive(_cast((args)[0], lambda: mdk_discovery.Node))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_NodeActive.singleton = mdk_discovery_NodeActive()
class mdk_discovery_NodeExpired(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_NodeExpired, self).__init__(u"mdk_discovery.NodeExpired");
        (self).name = u"mdk_discovery.NodeExpired"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_discovery.Node", u"node")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.NodeExpired(_cast((args)[0], lambda: mdk_discovery.Node))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_NodeExpired.singleton = mdk_discovery_NodeExpired()
class mdk_discovery_ReplaceCluster(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_ReplaceCluster, self).__init__(u"mdk_discovery.ReplaceCluster");
        (self).name = u"mdk_discovery.ReplaceCluster"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.List<mdk_discovery.Node>", u"nodes"), quark.reflect.Field(u"quark.String", u"cluster")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.ReplaceCluster(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: _List))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_ReplaceCluster.singleton = mdk_discovery_ReplaceCluster()
class mdk_discovery_DiscoverySource_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySource_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoverySource);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoverySource_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySource_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoverySource);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoverySource_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySource_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoverySource);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoverySource(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySource, self).__init__(u"mdk_discovery.DiscoverySource");
        (self).name = u"mdk_discovery.DiscoverySource"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_DiscoverySource_onStart_Method(), mdk_discovery_DiscoverySource_onStop_Method(), mdk_discovery_DiscoverySource_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_DiscoverySource.singleton = mdk_discovery_DiscoverySource()
class mdk_discovery_DiscoverySourceFactory_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySourceFactory_create_Method, self).__init__(u"mdk_discovery.DiscoverySource", u"create", _List([u"mdk_runtime.actors.Actor", u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoverySourceFactory);
        return (obj).create(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoverySourceFactory_isRegistrar_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySourceFactory_isRegistrar_Method, self).__init__(u"quark.bool", u"isRegistrar", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoverySourceFactory);
        return (obj).isRegistrar()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoverySourceFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoverySourceFactory, self).__init__(u"mdk_discovery.DiscoverySourceFactory");
        (self).name = u"mdk_discovery.DiscoverySourceFactory"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_DiscoverySourceFactory_create_Method(), mdk_discovery_DiscoverySourceFactory_isRegistrar_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_DiscoverySourceFactory.singleton = mdk_discovery_DiscoverySourceFactory()
class mdk_discovery__StaticRoutesActor_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery__StaticRoutesActor_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery._StaticRoutesActor);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery__StaticRoutesActor_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery__StaticRoutesActor_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery._StaticRoutesActor);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery__StaticRoutesActor_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery__StaticRoutesActor_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery._StaticRoutesActor);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery__StaticRoutesActor(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery__StaticRoutesActor, self).__init__(u"mdk_discovery._StaticRoutesActor");
        (self).name = u"mdk_discovery._StaticRoutesActor"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"_subscriber"), quark.reflect.Field(u"quark.List<mdk_discovery.Node>", u"_knownNodes")])
        (self).methods = _List([mdk_discovery__StaticRoutesActor_onStart_Method(), mdk_discovery__StaticRoutesActor_onMessage_Method(), mdk_discovery__StaticRoutesActor_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery._StaticRoutesActor(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: _List))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery__StaticRoutesActor.singleton = mdk_discovery__StaticRoutesActor()
class mdk_discovery_StaticRoutes_parseJSON_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_StaticRoutes_parseJSON_Method, self).__init__(u"mdk_discovery.StaticRoutes", u"parseJSON", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.StaticRoutes);
        return mdk_discovery.StaticRoutes.parseJSON(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_StaticRoutes_isRegistrar_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_StaticRoutes_isRegistrar_Method, self).__init__(u"quark.bool", u"isRegistrar", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.StaticRoutes);
        return (obj).isRegistrar()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_StaticRoutes_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_StaticRoutes_create_Method, self).__init__(u"mdk_discovery.DiscoverySource", u"create", _List([u"mdk_runtime.actors.Actor", u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.StaticRoutes);
        return (obj).create(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_StaticRoutes(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_StaticRoutes, self).__init__(u"mdk_discovery.StaticRoutes");
        (self).name = u"mdk_discovery.StaticRoutes"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.List<mdk_discovery.Node>", u"_knownNodes")])
        (self).methods = _List([mdk_discovery_StaticRoutes_parseJSON_Method(), mdk_discovery_StaticRoutes_isRegistrar_Method(), mdk_discovery_StaticRoutes_create_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.StaticRoutes(_cast((args)[0], lambda: _List))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_StaticRoutes.singleton = mdk_discovery_StaticRoutes()
class mdk_discovery_RegisterNode(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_RegisterNode, self).__init__(u"mdk_discovery.RegisterNode");
        (self).name = u"mdk_discovery.RegisterNode"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_discovery.Node", u"node")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.RegisterNode(_cast((args)[0], lambda: mdk_discovery.Node))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_RegisterNode.singleton = mdk_discovery_RegisterNode()
class mdk_discovery_DiscoveryRegistrar_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoveryRegistrar_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoveryRegistrar);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoveryRegistrar_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoveryRegistrar_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoveryRegistrar);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoveryRegistrar_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoveryRegistrar_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.DiscoveryRegistrar);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_DiscoveryRegistrar(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_DiscoveryRegistrar, self).__init__(u"mdk_discovery.DiscoveryRegistrar");
        (self).name = u"mdk_discovery.DiscoveryRegistrar"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_DiscoveryRegistrar_onStart_Method(), mdk_discovery_DiscoveryRegistrar_onStop_Method(), mdk_discovery_DiscoveryRegistrar_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_DiscoveryRegistrar.singleton = mdk_discovery_DiscoveryRegistrar()
class mdk_discovery__Request(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery__Request, self).__init__(u"mdk_discovery._Request");
        (self).name = u"mdk_discovery._Request"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"version"), quark.reflect.Field(u"mdk_runtime.promise.PromiseResolver", u"factory")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery._Request(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.promise.PromiseResolver))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery__Request.singleton = mdk_discovery__Request()
class mdk_discovery_FailurePolicy_success_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicy_success_Method, self).__init__(u"quark.void", u"success", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.FailurePolicy);
        (obj).success();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_FailurePolicy_failure_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicy_failure_Method, self).__init__(u"quark.void", u"failure", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.FailurePolicy);
        (obj).failure();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_FailurePolicy_available_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicy_available_Method, self).__init__(u"quark.bool", u"available", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.FailurePolicy);
        return (obj).available()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_FailurePolicy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicy, self).__init__(u"mdk_discovery.FailurePolicy");
        (self).name = u"mdk_discovery.FailurePolicy"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_FailurePolicy_success_Method(), mdk_discovery_FailurePolicy_failure_Method(), mdk_discovery_FailurePolicy_available_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_FailurePolicy.singleton = mdk_discovery_FailurePolicy()
class mdk_discovery_FailurePolicyFactory_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicyFactory_create_Method, self).__init__(u"mdk_discovery.FailurePolicy", u"create", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.FailurePolicyFactory);
        return (obj).create()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_FailurePolicyFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_FailurePolicyFactory, self).__init__(u"mdk_discovery.FailurePolicyFactory");
        (self).name = u"mdk_discovery.FailurePolicyFactory"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_FailurePolicyFactory_create_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_FailurePolicyFactory.singleton = mdk_discovery_FailurePolicyFactory()
class mdk_discovery_CircuitBreaker_success_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreaker_success_Method, self).__init__(u"quark.void", u"success", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.CircuitBreaker);
        (obj).success();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_CircuitBreaker_failure_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreaker_failure_Method, self).__init__(u"quark.void", u"failure", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.CircuitBreaker);
        (obj).failure();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_CircuitBreaker_available_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreaker_available_Method, self).__init__(u"quark.bool", u"available", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.CircuitBreaker);
        return (obj).available()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_CircuitBreaker(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreaker, self).__init__(u"mdk_discovery.CircuitBreaker");
        (self).name = u"mdk_discovery.CircuitBreaker"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"_log"), quark.reflect.Field(u"quark.int", u"_threshold"), quark.reflect.Field(u"quark.float", u"_delay"), quark.reflect.Field(u"mdk_runtime.Time", u"_time"), quark.reflect.Field(u"quark.concurrent.Lock", u"_mutex"), quark.reflect.Field(u"quark.bool", u"_failed"), quark.reflect.Field(u"quark.int", u"_failures"), quark.reflect.Field(u"quark.float", u"_lastFailure")])
        (self).methods = _List([mdk_discovery_CircuitBreaker_success_Method(), mdk_discovery_CircuitBreaker_failure_Method(), mdk_discovery_CircuitBreaker_available_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.CircuitBreaker(_cast((args)[0], lambda: mdk_runtime.Time), _cast((args)[1], lambda: int), _cast((args)[2], lambda: float))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_CircuitBreaker.singleton = mdk_discovery_CircuitBreaker()
class mdk_discovery_CircuitBreakerFactory_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreakerFactory_create_Method, self).__init__(u"mdk_discovery.FailurePolicy", u"create", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.CircuitBreakerFactory);
        return (obj).create()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_CircuitBreakerFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_CircuitBreakerFactory, self).__init__(u"mdk_discovery.CircuitBreakerFactory");
        (self).name = u"mdk_discovery.CircuitBreakerFactory"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"threshold"), quark.reflect.Field(u"quark.float", u"retestDelay"), quark.reflect.Field(u"mdk_runtime.Time", u"time")])
        (self).methods = _List([mdk_discovery_CircuitBreakerFactory_create_Method()])
        (self).parents = _List([u"mdk_discovery.FailurePolicyFactory"])

    def construct(self, args):
        return mdk_discovery.CircuitBreakerFactory(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_CircuitBreakerFactory.singleton = mdk_discovery_CircuitBreakerFactory()
class mdk_discovery_RecordingFailurePolicy_success_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicy_success_Method, self).__init__(u"quark.void", u"success", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.RecordingFailurePolicy);
        (obj).success();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_RecordingFailurePolicy_failure_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicy_failure_Method, self).__init__(u"quark.void", u"failure", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.RecordingFailurePolicy);
        (obj).failure();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_RecordingFailurePolicy_available_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicy_available_Method, self).__init__(u"quark.bool", u"available", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.RecordingFailurePolicy);
        return (obj).available()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_RecordingFailurePolicy(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicy, self).__init__(u"mdk_discovery.RecordingFailurePolicy");
        (self).name = u"mdk_discovery.RecordingFailurePolicy"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.int", u"successes"), quark.reflect.Field(u"quark.int", u"failures")])
        (self).methods = _List([mdk_discovery_RecordingFailurePolicy_success_Method(), mdk_discovery_RecordingFailurePolicy_failure_Method(), mdk_discovery_RecordingFailurePolicy_available_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.RecordingFailurePolicy()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_RecordingFailurePolicy.singleton = mdk_discovery_RecordingFailurePolicy()
class mdk_discovery_RecordingFailurePolicyFactory_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicyFactory_create_Method, self).__init__(u"mdk_discovery.FailurePolicy", u"create", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.RecordingFailurePolicyFactory);
        return (obj).create()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_RecordingFailurePolicyFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_RecordingFailurePolicyFactory, self).__init__(u"mdk_discovery.RecordingFailurePolicyFactory");
        (self).name = u"mdk_discovery.RecordingFailurePolicyFactory"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_discovery_RecordingFailurePolicyFactory_create_Method()])
        (self).parents = _List([u"mdk_discovery.FailurePolicyFactory"])

    def construct(self, args):
        return mdk_discovery.RecordingFailurePolicyFactory()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_RecordingFailurePolicyFactory.singleton = mdk_discovery_RecordingFailurePolicyFactory()
class mdk_discovery_Cluster_choose_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_choose_Method, self).__init__(u"mdk_discovery.Node", u"choose", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj).choose()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster__copyNode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster__copyNode_Method, self).__init__(u"mdk_discovery.Node", u"_copyNode", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj)._copyNode(_cast((args)[0], lambda: mdk_discovery.Node))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_failurePolicy_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_failurePolicy_Method, self).__init__(u"mdk_discovery.FailurePolicy", u"failurePolicy", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj).failurePolicy(_cast((args)[0], lambda: mdk_discovery.Node))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_chooseVersion_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_chooseVersion_Method, self).__init__(u"mdk_discovery.Node", u"chooseVersion", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj).chooseVersion(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_add_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_add_Method, self).__init__(u"quark.void", u"add", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        (obj).add(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster__addRequest_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster__addRequest_Method, self).__init__(u"quark.void", u"_addRequest", _List([u"quark.String", u"mdk_runtime.promise.PromiseResolver"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        (obj)._addRequest(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: mdk_runtime.promise.PromiseResolver));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_remove_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_remove_Method, self).__init__(u"quark.void", u"remove", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        (obj).remove(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_isEmpty_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_isEmpty_Method, self).__init__(u"quark.bool", u"isEmpty", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj).isEmpty()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Cluster);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Cluster(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_Cluster, self).__init__(u"mdk_discovery.Cluster");
        (self).name = u"mdk_discovery.Cluster"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.List<mdk_discovery.Node>", u"nodes"), quark.reflect.Field(u"quark.List<mdk_discovery._Request>", u"_waiting"), quark.reflect.Field(u"quark.Map<quark.String,mdk_discovery.FailurePolicy>", u"_failurepolicies"), quark.reflect.Field(u"quark.int", u"_counter"), quark.reflect.Field(u"mdk_discovery.FailurePolicyFactory", u"_fpfactory")])
        (self).methods = _List([mdk_discovery_Cluster_choose_Method(), mdk_discovery_Cluster__copyNode_Method(), mdk_discovery_Cluster_failurePolicy_Method(), mdk_discovery_Cluster_chooseVersion_Method(), mdk_discovery_Cluster_add_Method(), mdk_discovery_Cluster__addRequest_Method(), mdk_discovery_Cluster_remove_Method(), mdk_discovery_Cluster_isEmpty_Method(), mdk_discovery_Cluster_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.Cluster(_cast((args)[0], lambda: mdk_discovery.FailurePolicyFactory))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_Cluster.singleton = mdk_discovery_Cluster()
class mdk_discovery_Node_success_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Node_success_Method, self).__init__(u"quark.void", u"success", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Node);
        (obj).success();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Node_failure_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Node_failure_Method, self).__init__(u"quark.void", u"failure", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Node);
        (obj).failure();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Node_available_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Node_available_Method, self).__init__(u"quark.bool", u"available", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Node);
        return (obj).available()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Node_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Node_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Node);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Node(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_Node, self).__init__(u"mdk_discovery.Node");
        (self).name = u"mdk_discovery.Node"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"service"), quark.reflect.Field(u"quark.String", u"version"), quark.reflect.Field(u"quark.String", u"address"), quark.reflect.Field(u"quark.Map<quark.String,quark.Object>", u"properties"), quark.reflect.Field(u"mdk_discovery.FailurePolicy", u"_policy")])
        (self).methods = _List([mdk_discovery_Node_success_Method(), mdk_discovery_Node_failure_Method(), mdk_discovery_Node_available_Method(), mdk_discovery_Node_toString_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.Node()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_Node.singleton = mdk_discovery_Node()
class mdk_discovery_Discovery__lock_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__lock_Method, self).__init__(u"quark.void", u"_lock", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj)._lock();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery__release_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__release_Method, self).__init__(u"quark.void", u"_release", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj)._release();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_register_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_register_Method, self).__init__(u"mdk_discovery.Discovery", u"register", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).register(_cast((args)[0], lambda: mdk_discovery.Node))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_register_service_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_register_service_Method, self).__init__(u"mdk_discovery.Discovery", u"register_service", _List([u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).register_service(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_knownNodes_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_knownNodes_Method, self).__init__(u"quark.List<mdk_discovery.Node>", u"knownNodes", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).knownNodes(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_failurePolicy_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_failurePolicy_Method, self).__init__(u"mdk_discovery.FailurePolicy", u"failurePolicy", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).failurePolicy(_cast((args)[0], lambda: mdk_discovery.Node))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery__resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__resolve_Method, self).__init__(u"mdk_runtime.promise.Promise", u"_resolve", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj)._resolve(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_resolve_Method, self).__init__(u"quark.Object", u"resolve", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).resolve(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_resolve_until_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_resolve_until_Method, self).__init__(u"mdk_discovery.Node", u"resolve_until", _List([u"quark.String", u"quark.String", u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        return (obj).resolve_until(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: float))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery__replace_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__replace_Method, self).__init__(u"quark.void", u"_replace", _List([u"quark.String", u"quark.List<mdk_discovery.Node>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj)._replace(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: _List));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery__active_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__active_Method, self).__init__(u"quark.void", u"_active", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj)._active(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery__expire_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery__expire_Method, self).__init__(u"quark.void", u"_expire", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.Discovery);
        (obj)._expire(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_Discovery(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_Discovery, self).__init__(u"mdk_discovery.Discovery");
        (self).name = u"mdk_discovery.Discovery"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.Map<quark.String,mdk_discovery.Cluster>", u"services"), quark.reflect.Field(u"quark.bool", u"started"), quark.reflect.Field(u"quark.concurrent.Lock", u"mutex"), quark.reflect.Field(u"mdk_runtime.MDKRuntime", u"runtime"), quark.reflect.Field(u"mdk_discovery.FailurePolicyFactory", u"_fpfactory")])
        (self).methods = _List([mdk_discovery_Discovery__lock_Method(), mdk_discovery_Discovery__release_Method(), mdk_discovery_Discovery_onStart_Method(), mdk_discovery_Discovery_onStop_Method(), mdk_discovery_Discovery_register_Method(), mdk_discovery_Discovery_register_service_Method(), mdk_discovery_Discovery_knownNodes_Method(), mdk_discovery_Discovery_failurePolicy_Method(), mdk_discovery_Discovery__resolve_Method(), mdk_discovery_Discovery_resolve_Method(), mdk_discovery_Discovery_resolve_until_Method(), mdk_discovery_Discovery_onMessage_Method(), mdk_discovery_Discovery__replace_Method(), mdk_discovery_Discovery__active_Method(), mdk_discovery_Discovery__expire_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.Discovery(_cast((args)[0], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_Discovery.singleton = mdk_discovery_Discovery()
class mdk_discovery_protocol_DiscoClientFactory_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClientFactory_create_Method, self).__init__(u"mdk_discovery.DiscoverySource", u"create", _List([u"mdk_runtime.actors.Actor", u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClientFactory);
        return (obj).create(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClientFactory_isRegistrar_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClientFactory_isRegistrar_Method, self).__init__(u"quark.bool", u"isRegistrar", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClientFactory);
        return (obj).isRegistrar()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClientFactory(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClientFactory, self).__init__(u"mdk_discovery.protocol.DiscoClientFactory");
        (self).name = u"mdk_discovery.protocol.DiscoClientFactory"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_protocol.WSClient", u"wsclient")])
        (self).methods = _List([mdk_discovery_protocol_DiscoClientFactory_create_Method(), mdk_discovery_protocol_DiscoClientFactory_isRegistrar_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.protocol.DiscoClientFactory(_cast((args)[0], lambda: mdk_protocol.WSClient))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_protocol_DiscoClientFactory.singleton = mdk_discovery_protocol_DiscoClientFactory()
class mdk_discovery_protocol_DiscoClient_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onMessageFromServer_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onMessageFromServer_Method, self).__init__(u"quark.void", u"onMessageFromServer", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onMessageFromServer((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onWSConnected(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onPump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onPump_Method, self).__init__(u"quark.void", u"onPump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onPump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient__register_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient__register_Method, self).__init__(u"quark.void", u"_register", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj)._register(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_active_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_active_Method, self).__init__(u"quark.void", u"active", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).active(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_expire_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_expire_Method, self).__init__(u"quark.void", u"expire", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).expire(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_resolve_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_resolve_Method, self).__init__(u"quark.void", u"resolve", _List([u"mdk_discovery.Node"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).resolve(_cast((args)[0], lambda: mdk_discovery.Node));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onActive_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onActive_Method, self).__init__(u"quark.void", u"onActive", _List([u"mdk_discovery.protocol.Active"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onActive(_cast((args)[0], lambda: mdk_discovery.protocol.Active));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_onExpire_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_onExpire_Method, self).__init__(u"quark.void", u"onExpire", _List([u"mdk_discovery.protocol.Expire"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).onExpire(_cast((args)[0], lambda: mdk_discovery.protocol.Expire));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_heartbeat_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_heartbeat_Method, self).__init__(u"quark.void", u"heartbeat", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).heartbeat();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient_shutdown_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient_shutdown_Method, self).__init__(u"quark.void", u"shutdown", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.DiscoClient);
        (obj).shutdown();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_DiscoClient(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_DiscoClient, self).__init__(u"mdk_discovery.protocol.DiscoClient");
        (self).name = u"mdk_discovery.protocol.DiscoClient"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_discovery.FailurePolicyFactory", u"_failurePolicyFactory"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"_dispatcher"), quark.reflect.Field(u"mdk_runtime.Time", u"_timeService"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"_subscriber"), quark.reflect.Field(u"mdk_protocol.WSClient", u"_wsclient"), quark.reflect.Field(u"quark.Map<quark.String,mdk_discovery.Cluster>", u"registered"), quark.reflect.Field(u"quark.Logger", u"dlog"), quark.reflect.Field(u"quark.long", u"lastHeartbeat"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"sock")])
        (self).methods = _List([mdk_discovery_protocol_DiscoClient_onStart_Method(), mdk_discovery_protocol_DiscoClient_onStop_Method(), mdk_discovery_protocol_DiscoClient_onMessage_Method(), mdk_discovery_protocol_DiscoClient_onMessageFromServer_Method(), mdk_discovery_protocol_DiscoClient_onWSConnected_Method(), mdk_discovery_protocol_DiscoClient_onPump_Method(), mdk_discovery_protocol_DiscoClient__register_Method(), mdk_discovery_protocol_DiscoClient_active_Method(), mdk_discovery_protocol_DiscoClient_expire_Method(), mdk_discovery_protocol_DiscoClient_resolve_Method(), mdk_discovery_protocol_DiscoClient_onActive_Method(), mdk_discovery_protocol_DiscoClient_onExpire_Method(), mdk_discovery_protocol_DiscoClient_heartbeat_Method(), mdk_discovery_protocol_DiscoClient_shutdown_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.protocol.DiscoClient(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_protocol.WSClient), _cast((args)[2], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_protocol_DiscoClient.singleton = mdk_discovery_protocol_DiscoClient()
class mdk_discovery_protocol_Active_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Active_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Active);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Active_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Active_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Active);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Active(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Active, self).__init__(u"mdk_discovery.protocol.Active");
        (self).name = u"mdk_discovery.protocol.Active"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"mdk_discovery.Node", u"node"), quark.reflect.Field(u"quark.float", u"ttl")])
        (self).methods = _List([mdk_discovery_protocol_Active_decodeClassName_Method(), mdk_discovery_protocol_Active_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_discovery.protocol.Active()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_protocol_Active.singleton = mdk_discovery_protocol_Active()
class mdk_discovery_protocol_Expire_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Expire_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Expire);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Expire_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Expire_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Expire);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Expire(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Expire, self).__init__(u"mdk_discovery.protocol.Expire");
        (self).name = u"mdk_discovery.protocol.Expire"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"mdk_discovery.Node", u"node")])
        (self).methods = _List([mdk_discovery_protocol_Expire_decodeClassName_Method(), mdk_discovery_protocol_Expire_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_discovery.protocol.Expire()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_protocol_Expire.singleton = mdk_discovery_protocol_Expire()
class mdk_discovery_protocol_Clear_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Clear_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Clear);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Clear_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Clear_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.protocol.Clear);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_protocol_Clear(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_protocol_Clear, self).__init__(u"mdk_discovery.protocol.Clear");
        (self).name = u"mdk_discovery.protocol.Clear"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type")])
        (self).methods = _List([mdk_discovery_protocol_Clear_decodeClassName_Method(), mdk_discovery_protocol_Clear_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_discovery.protocol.Clear()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_protocol_Clear.singleton = mdk_discovery_protocol_Clear()
class mdk_protocol_Serializable_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Serializable_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Serializable);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Serializable_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Serializable_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Serializable);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Serializable(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_Serializable, self).__init__(u"mdk_protocol.Serializable");
        (self).name = u"mdk_protocol.Serializable"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_protocol_Serializable_decodeClassName_Method(), mdk_protocol_Serializable_encode_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.Serializable()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_Serializable.singleton = mdk_protocol_Serializable()
class mdk_protocol_LamportClock_decode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_decode_Method, self).__init__(u"mdk_protocol.LamportClock", u"decode", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return mdk_protocol.LamportClock.decode(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_key_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_key_Method, self).__init__(u"quark.String", u"key", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return (obj).key()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_enter_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_enter_Method, self).__init__(u"quark.int", u"enter", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return (obj).enter()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_leave_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_leave_Method, self).__init__(u"quark.int", u"leave", _List([u"quark.int"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return (obj).leave(_cast((args)[0], lambda: int))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_tick_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_tick_Method, self).__init__(u"quark.void", u"tick", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        (obj).tick();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.LamportClock);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_LamportClock(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_LamportClock, self).__init__(u"mdk_protocol.LamportClock");
        (self).name = u"mdk_protocol.LamportClock"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.concurrent.Lock", u"_mutex"), quark.reflect.Field(u"quark.List<quark.int>", u"clocks")])
        (self).methods = _List([mdk_protocol_LamportClock_decode_Method(), mdk_protocol_LamportClock_key_Method(), mdk_protocol_LamportClock_toString_Method(), mdk_protocol_LamportClock_enter_Method(), mdk_protocol_LamportClock_leave_Method(), mdk_protocol_LamportClock_tick_Method(), mdk_protocol_LamportClock_decodeClassName_Method(), mdk_protocol_LamportClock_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_protocol.LamportClock()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_LamportClock.singleton = mdk_protocol_LamportClock()
class mdk_protocol_SharedContext_withTraceId_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_withTraceId_Method, self).__init__(u"mdk_protocol.SharedContext", u"withTraceId", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).withTraceId(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_decode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_decode_Method, self).__init__(u"mdk_protocol.SharedContext", u"decode", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return mdk_protocol.SharedContext.decode(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_clockStr_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_clockStr_Method, self).__init__(u"quark.String", u"clockStr", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).clockStr(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_key_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_key_Method, self).__init__(u"quark.String", u"key", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).key()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_tick_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_tick_Method, self).__init__(u"quark.void", u"tick", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        (obj).tick();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_start_span_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_start_span_Method, self).__init__(u"mdk_protocol.SharedContext", u"start_span", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).start_span()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_finish_span_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_finish_span_Method, self).__init__(u"mdk_protocol.SharedContext", u"finish_span", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).finish_span()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_copy_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_copy_Method, self).__init__(u"mdk_protocol.SharedContext", u"copy", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).copy()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.SharedContext);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_SharedContext(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_SharedContext, self).__init__(u"mdk_protocol.SharedContext");
        (self).name = u"mdk_protocol.SharedContext"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"traceId"), quark.reflect.Field(u"mdk_protocol.LamportClock", u"clock"), quark.reflect.Field(u"quark.Map<quark.String,quark.Object>", u"properties"), quark.reflect.Field(u"quark.int", u"_lastEntry")])
        (self).methods = _List([mdk_protocol_SharedContext_withTraceId_Method(), mdk_protocol_SharedContext_decode_Method(), mdk_protocol_SharedContext_clockStr_Method(), mdk_protocol_SharedContext_key_Method(), mdk_protocol_SharedContext_toString_Method(), mdk_protocol_SharedContext_tick_Method(), mdk_protocol_SharedContext_start_span_Method(), mdk_protocol_SharedContext_finish_span_Method(), mdk_protocol_SharedContext_copy_Method(), mdk_protocol_SharedContext_decodeClassName_Method(), mdk_protocol_SharedContext_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_protocol.SharedContext()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_SharedContext.singleton = mdk_protocol_SharedContext()
class mdk_protocol_Open_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Open_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Open);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Open_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Open_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Open);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Open(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_Open, self).__init__(u"mdk_protocol.Open");
        (self).name = u"mdk_protocol.Open"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"quark.String", u"version"), quark.reflect.Field(u"quark.Map<quark.String,quark.String>", u"properties")])
        (self).methods = _List([mdk_protocol_Open_decodeClassName_Method(), mdk_protocol_Open_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_protocol.Open()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_Open.singleton = mdk_protocol_Open()
class mdk_protocol_ProtocolError(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_ProtocolError, self).__init__(u"mdk_protocol.ProtocolError");
        (self).name = u"mdk_protocol.ProtocolError"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"code"), quark.reflect.Field(u"quark.String", u"title"), quark.reflect.Field(u"quark.String", u"detail"), quark.reflect.Field(u"quark.String", u"id")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.ProtocolError()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_ProtocolError.singleton = mdk_protocol_ProtocolError()
class mdk_protocol_Close_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Close_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Close);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Close_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_Close_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.Close);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_Close(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_Close, self).__init__(u"mdk_protocol.Close");
        (self).name = u"mdk_protocol.Close"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"mdk_protocol.ProtocolError", u"error")])
        (self).methods = _List([mdk_protocol_Close_decodeClassName_Method(), mdk_protocol_Close_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_protocol.Close()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_Close.singleton = mdk_protocol_Close()
class mdk_protocol_Pump(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_Pump, self).__init__(u"mdk_protocol.Pump");
        (self).name = u"mdk_protocol.Pump"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.Pump()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_Pump.singleton = mdk_protocol_Pump()
class mdk_protocol_WSConnected(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_WSConnected, self).__init__(u"mdk_protocol.WSConnected");
        (self).name = u"mdk_protocol.WSConnected"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"websock")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.WSConnected(_cast((args)[0], lambda: mdk_runtime.actors.Actor))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_WSConnected.singleton = mdk_protocol_WSConnected()
class mdk_protocol_DecodedMessage(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_DecodedMessage, self).__init__(u"mdk_protocol.DecodedMessage");
        (self).name = u"mdk_protocol.DecodedMessage"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Object", u"message")])
        (self).methods = _List([])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.DecodedMessage((args)[0])

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_DecodedMessage.singleton = mdk_protocol_DecodedMessage()
class mdk_protocol_WSClientSubscriber_onMessageFromServer_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onMessageFromServer_Method, self).__init__(u"quark.void", u"onMessageFromServer", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onMessageFromServer((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onWSConnected(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber_onPump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onPump_Method, self).__init__(u"quark.void", u"onPump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onPump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClientSubscriber);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClientSubscriber(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_WSClientSubscriber, self).__init__(u"mdk_protocol.WSClientSubscriber");
        (self).name = u"mdk_protocol.WSClientSubscriber"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_protocol_WSClientSubscriber_onMessageFromServer_Method(), mdk_protocol_WSClientSubscriber_onWSConnected_Method(), mdk_protocol_WSClientSubscriber_onPump_Method(), mdk_protocol_WSClientSubscriber_onStart_Method(), mdk_protocol_WSClientSubscriber_onStop_Method(), mdk_protocol_WSClientSubscriber_onMessage_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_WSClientSubscriber.singleton = mdk_protocol_WSClientSubscriber()
class mdk_protocol_OpenCloseSubscriber_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onMessageFromServer_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onMessageFromServer_Method, self).__init__(u"quark.void", u"onMessageFromServer", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onMessageFromServer((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onWSConnected(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onPump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onPump_Method, self).__init__(u"quark.void", u"onPump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onPump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onOpen_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onOpen_Method, self).__init__(u"quark.void", u"onOpen", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onOpen();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber_onClose_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber_onClose_Method, self).__init__(u"quark.void", u"onClose", _List([u"mdk_protocol.Close"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.OpenCloseSubscriber);
        (obj).onClose(_cast((args)[0], lambda: mdk_protocol.Close));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_OpenCloseSubscriber(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_OpenCloseSubscriber, self).__init__(u"mdk_protocol.OpenCloseSubscriber");
        (self).name = u"mdk_protocol.OpenCloseSubscriber"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"_dispatcher"), quark.reflect.Field(u"mdk_protocol.WSClient", u"_wsclient")])
        (self).methods = _List([mdk_protocol_OpenCloseSubscriber_onStart_Method(), mdk_protocol_OpenCloseSubscriber_onMessage_Method(), mdk_protocol_OpenCloseSubscriber_onStop_Method(), mdk_protocol_OpenCloseSubscriber_onMessageFromServer_Method(), mdk_protocol_OpenCloseSubscriber_onWSConnected_Method(), mdk_protocol_OpenCloseSubscriber_onPump_Method(), mdk_protocol_OpenCloseSubscriber_onOpen_Method(), mdk_protocol_OpenCloseSubscriber_onClose_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.OpenCloseSubscriber(_cast((args)[0], lambda: mdk_protocol.WSClient))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_OpenCloseSubscriber.singleton = mdk_protocol_OpenCloseSubscriber()
class mdk_protocol_JSONParser_register_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_JSONParser_register_Method, self).__init__(u"quark.void", u"register", _List([u"quark.String", u"quark.reflect.Class"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.JSONParser);
        (obj).register(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: quark.reflect.Class));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_JSONParser_decode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_JSONParser_decode_Method, self).__init__(u"quark.Object", u"decode", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.JSONParser);
        return (obj).decode(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_JSONParser(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_JSONParser, self).__init__(u"mdk_protocol.JSONParser");
        (self).name = u"mdk_protocol.JSONParser"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Map<quark.String,quark.reflect.Class>", u"_typeToClass")])
        (self).methods = _List([mdk_protocol_JSONParser_register_Method(), mdk_protocol_JSONParser_decode_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.JSONParser()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_JSONParser.singleton = mdk_protocol_JSONParser()
class mdk_protocol_WSClient_subscribe_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_subscribe_Method, self).__init__(u"quark.void", u"subscribe", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).subscribe(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_isStarted_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_isStarted_Method, self).__init__(u"quark.bool", u"isStarted", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        return (obj).isStarted()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_isConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_isConnected_Method, self).__init__(u"quark.bool", u"isConnected", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        return (obj).isConnected()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_schedule_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_schedule_Method, self).__init__(u"quark.void", u"schedule", _List([u"quark.float"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).schedule(_cast((args)[0], lambda: float));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_scheduleReconnect_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_scheduleReconnect_Method, self).__init__(u"quark.void", u"scheduleReconnect", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).scheduleReconnect();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onClose_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onClose_Method, self).__init__(u"quark.void", u"onClose", _List([u"quark.bool"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onClose(_cast((args)[0], lambda: bool));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_doBackoff_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_doBackoff_Method, self).__init__(u"quark.void", u"doBackoff", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).doBackoff();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onScheduledEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onScheduledEvent_Method, self).__init__(u"quark.void", u"onScheduledEvent", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onScheduledEvent();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_doOpen_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_doOpen_Method, self).__init__(u"quark.void", u"doOpen", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).doOpen();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_startup_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_startup_Method, self).__init__(u"quark.void", u"startup", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).startup();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_pump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_pump_Method, self).__init__(u"quark.void", u"pump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).pump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"mdk_runtime.WSActor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onWSConnected(_cast((args)[0], lambda: mdk_runtime.WSActor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onWSError_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onWSError_Method, self).__init__(u"quark.void", u"onWSError", _List([u"quark.error.Error"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onWSError(_cast((args)[0], lambda: quark.error.Error));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient_onWSClosed_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient_onWSClosed_Method, self).__init__(u"quark.void", u"onWSClosed", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_protocol.WSClient);
        (obj).onWSClosed();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_protocol_WSClient(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_protocol_WSClient, self).__init__(u"mdk_protocol.WSClient");
        (self).name = u"mdk_protocol.WSClient"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.float", u"firstDelay"), quark.reflect.Field(u"quark.float", u"maxDelay"), quark.reflect.Field(u"quark.float", u"reconnectDelay"), quark.reflect.Field(u"quark.float", u"ttl"), quark.reflect.Field(u"quark.float", u"tick"), quark.reflect.Field(u"mdk_runtime.WSActor", u"sock"), quark.reflect.Field(u"quark.long", u"lastConnectAttempt"), quark.reflect.Field(u"mdk_runtime.Time", u"timeService"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"schedulingActor"), quark.reflect.Field(u"mdk_runtime.WebSockets", u"websockets"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher"), quark.reflect.Field(u"quark.String", u"url"), quark.reflect.Field(u"quark.String", u"token"), quark.reflect.Field(u"quark.List<mdk_runtime.actors.Actor>", u"subscribers"), quark.reflect.Field(u"quark.bool", u"_started"), quark.reflect.Field(u"mdk_protocol.JSONParser", u"_parser")])
        (self).methods = _List([mdk_protocol_WSClient_subscribe_Method(), mdk_protocol_WSClient_isStarted_Method(), mdk_protocol_WSClient_isConnected_Method(), mdk_protocol_WSClient_schedule_Method(), mdk_protocol_WSClient_scheduleReconnect_Method(), mdk_protocol_WSClient_onClose_Method(), mdk_protocol_WSClient_doBackoff_Method(), mdk_protocol_WSClient_onStart_Method(), mdk_protocol_WSClient_onStop_Method(), mdk_protocol_WSClient_onMessage_Method(), mdk_protocol_WSClient_onScheduledEvent_Method(), mdk_protocol_WSClient_doOpen_Method(), mdk_protocol_WSClient_startup_Method(), mdk_protocol_WSClient_pump_Method(), mdk_protocol_WSClient_onWSConnected_Method(), mdk_protocol_WSClient_onWSError_Method(), mdk_protocol_WSClient_onWSClosed_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_protocol.WSClient(_cast((args)[0], lambda: mdk_runtime.MDKRuntime), _cast((args)[1], lambda: mdk_protocol.JSONParser), _cast((args)[2], lambda: unicode), _cast((args)[3], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_protocol_WSClient.singleton = mdk_protocol_WSClient()
class mdk_discovery_synapse_Synapse_create_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse_Synapse_create_Method, self).__init__(u"mdk_discovery.DiscoverySource", u"create", _List([u"mdk_runtime.actors.Actor", u"mdk_runtime.MDKRuntime"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse.Synapse);
        return (obj).create(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: mdk_runtime.MDKRuntime))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse_Synapse_isRegistrar_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse_Synapse_isRegistrar_Method, self).__init__(u"quark.bool", u"isRegistrar", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse.Synapse);
        return (obj).isRegistrar()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse_Synapse(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_synapse_Synapse, self).__init__(u"mdk_discovery.synapse.Synapse");
        (self).name = u"mdk_discovery.synapse.Synapse"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_directory_path")])
        (self).methods = _List([mdk_discovery_synapse_Synapse_create_Method(), mdk_discovery_synapse_Synapse_isRegistrar_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.synapse.Synapse(_cast((args)[0], lambda: unicode))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_synapse_Synapse.singleton = mdk_discovery_synapse_Synapse()
class mdk_discovery_synapse__SynapseSource_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse._SynapseSource);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse__SynapseSource__pathToServiceName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource__pathToServiceName_Method, self).__init__(u"quark.String", u"_pathToServiceName", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse._SynapseSource);
        return (obj)._pathToServiceName(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse__SynapseSource__update_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource__update_Method, self).__init__(u"quark.void", u"_update", _List([u"quark.String", u"quark.List<mdk_discovery.Node>"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse._SynapseSource);
        (obj)._update(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: _List));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse__SynapseSource_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse._SynapseSource);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse__SynapseSource_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_discovery.synapse._SynapseSource);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_discovery_synapse__SynapseSource(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_discovery_synapse__SynapseSource, self).__init__(u"mdk_discovery.synapse._SynapseSource");
        (self).name = u"mdk_discovery.synapse._SynapseSource"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_runtime.actors.Actor", u"subscriber"), quark.reflect.Field(u"quark.String", u"directory_path"), quark.reflect.Field(u"mdk_runtime.files.FileActor", u"files"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"dispatcher")])
        (self).methods = _List([mdk_discovery_synapse__SynapseSource_onStart_Method(), mdk_discovery_synapse__SynapseSource__pathToServiceName_Method(), mdk_discovery_synapse__SynapseSource__update_Method(), mdk_discovery_synapse__SynapseSource_onMessage_Method(), mdk_discovery_synapse__SynapseSource_onStop_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_discovery.synapse._SynapseSource(_cast((args)[0], lambda: mdk_runtime.actors.Actor), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: mdk_runtime.MDKRuntime))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_discovery_synapse__SynapseSource.singleton = mdk_discovery_synapse__SynapseSource()
class mdk_tracing_SharedContextInitializer_getValue_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_SharedContextInitializer_getValue_Method, self).__init__(u"mdk_protocol.SharedContext", u"getValue", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.SharedContextInitializer);
        return (obj).getValue()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_SharedContextInitializer(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_SharedContextInitializer, self).__init__(u"mdk_tracing.SharedContextInitializer");
        (self).name = u"mdk_tracing.SharedContextInitializer"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_tracing_SharedContextInitializer_getValue_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_tracing.SharedContextInitializer()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_SharedContextInitializer.singleton = mdk_tracing_SharedContextInitializer()
class mdk_tracing_Tracer_withURLsAndToken_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_withURLsAndToken_Method, self).__init__(u"mdk_tracing.Tracer", u"withURLsAndToken", _List([u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        return mdk_tracing.Tracer.withURLsAndToken(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_withURLAndToken_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_withURLAndToken_Method, self).__init__(u"mdk_tracing.Tracer", u"withURLAndToken", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        return mdk_tracing.Tracer.withURLAndToken(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_initContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_initContext_Method, self).__init__(u"quark.void", u"initContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).initContext();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_joinContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_joinContext_Method, self).__init__(u"quark.void", u"joinContext", _List([u"mdk_protocol.SharedContext"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).joinContext(_cast((args)[0], lambda: mdk_protocol.SharedContext));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_joinEncodedContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_joinEncodedContext_Method, self).__init__(u"quark.void", u"joinEncodedContext", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).joinEncodedContext(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_getContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_getContext_Method, self).__init__(u"mdk_protocol.SharedContext", u"getContext", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        return (obj).getContext()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_setContext_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_setContext_Method, self).__init__(u"quark.void", u"setContext", _List([u"mdk_protocol.SharedContext"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).setContext(_cast((args)[0], lambda: mdk_protocol.SharedContext));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_start_span_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_start_span_Method, self).__init__(u"quark.void", u"start_span", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).start_span();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_finish_span_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_finish_span_Method, self).__init__(u"quark.void", u"finish_span", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).finish_span();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_log_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_log_Method, self).__init__(u"quark.void", u"log", _List([u"quark.String", u"quark.String", u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).log(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode), _cast((args)[2], lambda: unicode), _cast((args)[3], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer_subscribe_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer_subscribe_Method, self).__init__(u"quark.void", u"subscribe", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.Tracer);
        (obj).subscribe(_cast((args)[0], lambda: quark.UnaryCallable));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_Tracer(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_Tracer, self).__init__(u"mdk_tracing.Tracer");
        (self).name = u"mdk_tracing.Tracer"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.Logger", u"logger"), quark.reflect.Field(u"quark.long", u"lastPoll"), quark.reflect.Field(u"quark.concurrent.TLS<mdk_protocol.SharedContext>", u"_context"), quark.reflect.Field(u"mdk_tracing.protocol.TracingClient", u"_client"), quark.reflect.Field(u"mdk_runtime.MDKRuntime", u"runtime")])
        (self).methods = _List([mdk_tracing_Tracer_withURLsAndToken_Method(), mdk_tracing_Tracer_withURLAndToken_Method(), mdk_tracing_Tracer_onStart_Method(), mdk_tracing_Tracer_onStop_Method(), mdk_tracing_Tracer_onMessage_Method(), mdk_tracing_Tracer_initContext_Method(), mdk_tracing_Tracer_joinContext_Method(), mdk_tracing_Tracer_joinEncodedContext_Method(), mdk_tracing_Tracer_getContext_Method(), mdk_tracing_Tracer_setContext_Method(), mdk_tracing_Tracer_start_span_Method(), mdk_tracing_Tracer_finish_span_Method(), mdk_tracing_Tracer_log_Method(), mdk_tracing_Tracer_subscribe_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_tracing.Tracer(_cast((args)[0], lambda: mdk_runtime.MDKRuntime), _cast((args)[1], lambda: mdk_protocol.WSClient))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_Tracer.singleton = mdk_tracing_Tracer()
class mdk_tracing_api_ApiHandler_getLogEvents_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_ApiHandler_getLogEvents_Method, self).__init__(u"mdk_tracing.api.GetLogEventsResult", u"getLogEvents", _List([u"mdk_tracing.api.GetLogEventsRequest"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.ApiHandler);
        return (obj).getLogEvents(_cast((args)[0], lambda: mdk_tracing.api.GetLogEventsRequest))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_ApiHandler(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_api_ApiHandler, self).__init__(u"mdk_tracing.api.ApiHandler");
        (self).name = u"mdk_tracing.api.ApiHandler"
        (self).parameters = _List([])
        (self).fields = _List([])
        (self).methods = _List([mdk_tracing_api_ApiHandler_getLogEvents_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return None

    def isAbstract(self):
        return True

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_api_ApiHandler.singleton = mdk_tracing_api_ApiHandler()
class mdk_tracing_api_GetLogEventsRequest_decode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsRequest_decode_Method, self).__init__(u"mdk_tracing.api.GetLogEventsRequest", u"decode", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsRequest);
        return mdk_tracing.api.GetLogEventsRequest.decode(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsRequest_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsRequest_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsRequest);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsRequest_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsRequest_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsRequest);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsRequest(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsRequest, self).__init__(u"mdk_tracing.api.GetLogEventsRequest");
        (self).name = u"mdk_tracing.api.GetLogEventsRequest"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.long", u"startTime"), quark.reflect.Field(u"quark.long", u"endTime")])
        (self).methods = _List([mdk_tracing_api_GetLogEventsRequest_decode_Method(), mdk_tracing_api_GetLogEventsRequest_decodeClassName_Method(), mdk_tracing_api_GetLogEventsRequest_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_tracing.api.GetLogEventsRequest()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_api_GetLogEventsRequest.singleton = mdk_tracing_api_GetLogEventsRequest()
class mdk_tracing_api_GetLogEventsResult_decode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsResult_decode_Method, self).__init__(u"mdk_tracing.api.GetLogEventsResult", u"decode", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsResult);
        return mdk_tracing.api.GetLogEventsResult.decode(_cast((args)[0], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsResult_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsResult_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsResult);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsResult_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsResult_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.api.GetLogEventsResult);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_api_GetLogEventsResult(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_api_GetLogEventsResult, self).__init__(u"mdk_tracing.api.GetLogEventsResult");
        (self).name = u"mdk_tracing.api.GetLogEventsResult"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.List<mdk_tracing.protocol.LogEvent>", u"result")])
        (self).methods = _List([mdk_tracing_api_GetLogEventsResult_decode_Method(), mdk_tracing_api_GetLogEventsResult_decodeClassName_Method(), mdk_tracing_api_GetLogEventsResult_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_tracing.api.GetLogEventsResult()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_api_GetLogEventsResult.singleton = mdk_tracing_api_GetLogEventsResult()
class mdk_tracing_protocol_LogEvent_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogEvent_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogEvent);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogEvent_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogEvent_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogEvent);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogEvent_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogEvent_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogEvent);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogEvent(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogEvent, self).__init__(u"mdk_tracing.protocol.LogEvent");
        (self).name = u"mdk_tracing.protocol.LogEvent"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"mdk_protocol.SharedContext", u"context"), quark.reflect.Field(u"quark.long", u"timestamp"), quark.reflect.Field(u"quark.String", u"node"), quark.reflect.Field(u"quark.String", u"level"), quark.reflect.Field(u"quark.String", u"category"), quark.reflect.Field(u"quark.String", u"contentType"), quark.reflect.Field(u"quark.String", u"text"), quark.reflect.Field(u"quark.long", u"sequence"), quark.reflect.Field(u"quark.int", u"sync")])
        (self).methods = _List([mdk_tracing_protocol_LogEvent_toString_Method(), mdk_tracing_protocol_LogEvent_decodeClassName_Method(), mdk_tracing_protocol_LogEvent_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_tracing.protocol.LogEvent()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_protocol_LogEvent.singleton = mdk_tracing_protocol_LogEvent()
class mdk_tracing_protocol_Subscribe_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_Subscribe_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.Subscribe);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_Subscribe_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_Subscribe_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.Subscribe);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_Subscribe_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_Subscribe_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.Subscribe);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_Subscribe(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_Subscribe, self).__init__(u"mdk_tracing.protocol.Subscribe");
        (self).name = u"mdk_tracing.protocol.Subscribe"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type")])
        (self).methods = _List([mdk_tracing_protocol_Subscribe_toString_Method(), mdk_tracing_protocol_Subscribe_decodeClassName_Method(), mdk_tracing_protocol_Subscribe_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_tracing.protocol.Subscribe()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_protocol_Subscribe.singleton = mdk_tracing_protocol_Subscribe()
class mdk_tracing_protocol_LogAck_toString_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogAck_toString_Method, self).__init__(u"quark.String", u"toString", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogAck);
        return (obj).toString()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogAck_decodeClassName_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogAck_decodeClassName_Method, self).__init__(u"mdk_protocol.Serializable", u"decodeClassName", _List([u"quark.String", u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogAck);
        return mdk_protocol.Serializable.decodeClassName(_cast((args)[0], lambda: unicode), _cast((args)[1], lambda: unicode))

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogAck_encode_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogAck_encode_Method, self).__init__(u"quark.String", u"encode", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.LogAck);
        return (obj).encode()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_LogAck(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_LogAck, self).__init__(u"mdk_tracing.protocol.LogAck");
        (self).name = u"mdk_tracing.protocol.LogAck"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"quark.String", u"_json_type"), quark.reflect.Field(u"quark.long", u"sequence")])
        (self).methods = _List([mdk_tracing_protocol_LogAck_toString_Method(), mdk_tracing_protocol_LogAck_decodeClassName_Method(), mdk_tracing_protocol_LogAck_encode_Method()])
        (self).parents = _List([u"mdk_protocol.Serializable"])

    def construct(self, args):
        return mdk_tracing.protocol.LogAck()

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_protocol_LogAck.singleton = mdk_tracing_protocol_LogAck()
class mdk_tracing_protocol_TracingClient__debug_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient__debug_Method, self).__init__(u"quark.void", u"_debug", _List([u"quark.String"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj)._debug(_cast((args)[0], lambda: unicode));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_subscribe_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_subscribe_Method, self).__init__(u"quark.void", u"subscribe", _List([u"quark.UnaryCallable"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).subscribe(_cast((args)[0], lambda: quark.UnaryCallable));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onStart_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onStart_Method, self).__init__(u"quark.void", u"onStart", _List([u"mdk_runtime.actors.MessageDispatcher"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onStart(_cast((args)[0], lambda: mdk_runtime.actors.MessageDispatcher));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onStop_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onStop_Method, self).__init__(u"quark.void", u"onStop", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onStop();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onMessage_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onMessage_Method, self).__init__(u"quark.void", u"onMessage", _List([u"mdk_runtime.actors.Actor", u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onMessage(_cast((args)[0], lambda: mdk_runtime.actors.Actor), (args)[1]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onWSConnected_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onWSConnected_Method, self).__init__(u"quark.void", u"onWSConnected", _List([u"mdk_runtime.actors.Actor"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onWSConnected(_cast((args)[0], lambda: mdk_runtime.actors.Actor));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onPump_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onPump_Method, self).__init__(u"quark.void", u"onPump", _List([]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onPump();
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onMessageFromServer_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onMessageFromServer_Method, self).__init__(u"quark.void", u"onMessageFromServer", _List([u"quark.Object"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onMessageFromServer((args)[0]);
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onLogEvent_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onLogEvent_Method, self).__init__(u"quark.void", u"onLogEvent", _List([u"mdk_tracing.protocol.LogEvent"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onLogEvent(_cast((args)[0], lambda: mdk_tracing.protocol.LogEvent));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_onLogAck_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_onLogAck_Method, self).__init__(u"quark.void", u"onLogAck", _List([u"mdk_tracing.protocol.LogAck"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).onLogAck(_cast((args)[0], lambda: mdk_tracing.protocol.LogAck));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient_log_Method(quark.reflect.Method):
    def _init(self):
        quark.reflect.Method._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient_log_Method, self).__init__(u"quark.void", u"log", _List([u"mdk_tracing.protocol.LogEvent"]));

    def invoke(self, object, args):
        obj = _cast(object, lambda: mdk_tracing.protocol.TracingClient);
        (obj).log(_cast((args)[0], lambda: mdk_tracing.protocol.LogEvent));
        return None

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

class mdk_tracing_protocol_TracingClient(quark.reflect.Class):
    def _init(self):
        quark.reflect.Class._init(self)

    def __init__(self):
        super(mdk_tracing_protocol_TracingClient, self).__init__(u"mdk_tracing.protocol.TracingClient");
        (self).name = u"mdk_tracing.protocol.TracingClient"
        (self).parameters = _List([])
        (self).fields = _List([quark.reflect.Field(u"mdk_tracing.Tracer", u"_tracer"), quark.reflect.Field(u"quark.bool", u"_started"), quark.reflect.Field(u"quark.concurrent.Lock", u"_mutex"), quark.reflect.Field(u"quark.UnaryCallable", u"_handler"), quark.reflect.Field(u"mdk_runtime.actors.MessageDispatcher", u"_dispatcher"), quark.reflect.Field(u"quark.long", u"_syncRequestPeriod"), quark.reflect.Field(u"quark.int", u"_syncInFlightMax"), quark.reflect.Field(u"quark.List<mdk_tracing.protocol.LogEvent>", u"_buffered"), quark.reflect.Field(u"quark.List<mdk_tracing.protocol.LogEvent>", u"_inFlight"), quark.reflect.Field(u"quark.long", u"_logged"), quark.reflect.Field(u"quark.long", u"_sent"), quark.reflect.Field(u"quark.long", u"_failedSends"), quark.reflect.Field(u"quark.long", u"_recorded"), quark.reflect.Field(u"quark.long", u"_lastSyncTime"), quark.reflect.Field(u"mdk_protocol.WSClient", u"_wsclient"), quark.reflect.Field(u"mdk_runtime.actors.Actor", u"_sock"), quark.reflect.Field(u"quark.Logger", u"_myLog")])
        (self).methods = _List([mdk_tracing_protocol_TracingClient__debug_Method(), mdk_tracing_protocol_TracingClient_subscribe_Method(), mdk_tracing_protocol_TracingClient_onStart_Method(), mdk_tracing_protocol_TracingClient_onStop_Method(), mdk_tracing_protocol_TracingClient_onMessage_Method(), mdk_tracing_protocol_TracingClient_onWSConnected_Method(), mdk_tracing_protocol_TracingClient_onPump_Method(), mdk_tracing_protocol_TracingClient_onMessageFromServer_Method(), mdk_tracing_protocol_TracingClient_onLogEvent_Method(), mdk_tracing_protocol_TracingClient_onLogAck_Method(), mdk_tracing_protocol_TracingClient_log_Method()])
        (self).parents = _List([u"quark.Object"])

    def construct(self, args):
        return mdk_tracing.protocol.TracingClient(_cast((args)[0], lambda: mdk_tracing.Tracer), _cast((args)[1], lambda: mdk_protocol.WSClient))

    def isAbstract(self):
        return False

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
mdk_tracing_protocol_TracingClient.singleton = mdk_tracing_protocol_TracingClient()
class Root(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def _getClass(self):
        return _cast(None, lambda: unicode)

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
Root.mdk_MDK_md = mdk_MDK.singleton
Root.mdk_Session_md = mdk_Session.singleton
Root.mdk_MDKImpl_md = mdk_MDKImpl.singleton
Root.mdk__TLSInit_md = mdk__TLSInit.singleton
Root.mdk_SessionImpl_md = mdk_SessionImpl.singleton
Root.quark_Task_md = quark_Task.singleton
Root.quark_Runtime_md = quark_Runtime.singleton
Root.quark_Maybe_quark_Object__md = quark_Maybe_quark_Object_.singleton
Root.quark_ParsedNumber_quark_int__md = quark_ParsedNumber_quark_int_.singleton
Root.quark_ParsedNumber_quark_long__md = quark_ParsedNumber_quark_long_.singleton
Root.quark_ParsedInt_md = quark_ParsedInt.singleton
Root.quark_ParsedLong_md = quark_ParsedLong.singleton
Root.quark_ListUtil_quark_Object__md = quark_ListUtil_quark_Object_.singleton
Root.quark_ListUtil_mdk_discovery_Node__md = quark_ListUtil_mdk_discovery_Node_.singleton
Root.quark_List_quark_List_mdk_discovery_Node___md = quark_List_quark_List_mdk_discovery_Node__.singleton
Root.quark_List_mdk_discovery_Node__md = quark_List_mdk_discovery_Node_.singleton
Root.quark_List_quark_Map_quark_String_quark_String___md = quark_List_quark_Map_quark_String_quark_String__.singleton
Root.quark_List_quark_String__md = quark_List_quark_String_.singleton
Root.quark_List_quark_Object__md = quark_List_quark_Object_.singleton
Root.quark_List_quark_concurrent_FutureCompletion__md = quark_List_quark_concurrent_FutureCompletion_.singleton
Root.quark_List_quark_test_Test__md = quark_List_quark_test_Test_.singleton
Root.quark_List_quark_mock_MockMessage__md = quark_List_quark_mock_MockMessage_.singleton
Root.quark_List_quark_mock_MockEvent__md = quark_List_quark_mock_MockEvent_.singleton
Root.quark_List_quark_mock_MockTask__md = quark_List_quark_mock_MockTask_.singleton
Root.quark_List_quark_bool__md = quark_List_quark_bool_.singleton
Root.quark_List_quark__Callback__md = quark_List_quark__Callback_.singleton
Root.quark_List_mdk_runtime_WSActor__md = quark_List_mdk_runtime_WSActor_.singleton
Root.quark_List_mdk_runtime_FakeWSActor__md = quark_List_mdk_runtime_FakeWSActor_.singleton
Root.quark_List_quark_long__md = quark_List_quark_long_.singleton
Root.quark_List_mdk_runtime_actors__QueuedMessage__md = quark_List_mdk_runtime_actors__QueuedMessage_.singleton
Root.quark_List_mdk_runtime_promise__Callback__md = quark_List_mdk_runtime_promise__Callback_.singleton
Root.quark_List_mdk_runtime_files__Subscription__md = quark_List_mdk_runtime_files__Subscription_.singleton
Root.quark_List_mdk_discovery__Request__md = quark_List_mdk_discovery__Request_.singleton
Root.quark_List_quark_int__md = quark_List_quark_int_.singleton
Root.quark_List_mdk_runtime_actors_Actor__md = quark_List_mdk_runtime_actors_Actor_.singleton
Root.quark_List_mdk_tracing_protocol_LogEvent__md = quark_List_mdk_tracing_protocol_LogEvent_.singleton
Root.quark_Map_quark_String_quark_Object__md = quark_Map_quark_String_quark_Object_.singleton
Root.quark_Map_quark_String_quark_int__md = quark_Map_quark_String_quark_int_.singleton
Root.quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String____md = quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String___.singleton
Root.quark_Map_quark_String_quark_String__md = quark_Map_quark_String_quark_String_.singleton
Root.quark_Map_quark_Object_quark_Object__md = quark_Map_quark_Object_quark_Object_.singleton
Root.quark_Map_quark_String_quark_ServiceInstance__md = quark_Map_quark_String_quark_ServiceInstance_.singleton
Root.quark_Map_quark_String_quark_mock_SocketEvent__md = quark_Map_quark_String_quark_mock_SocketEvent_.singleton
Root.quark_Map_quark_long_mdk_runtime__FakeTimeRequest__md = quark_Map_quark_long_mdk_runtime__FakeTimeRequest_.singleton
Root.quark_Map_quark_String_mdk_discovery_FailurePolicy__md = quark_Map_quark_String_mdk_discovery_FailurePolicy_.singleton
Root.quark_Map_quark_String_mdk_discovery_Cluster__md = quark_Map_quark_String_mdk_discovery_Cluster_.singleton
Root.quark_UnaryCallable_md = quark_UnaryCallable.singleton
Root.quark_error_Error_md = quark_error_Error.singleton
Root.quark_logging_Appender_md = quark_logging_Appender.singleton
Root.quark_logging_Config_md = quark_logging_Config.singleton
Root.quark_ServletError_md = quark_ServletError.singleton
Root.quark_Servlet_md = quark_Servlet.singleton
Root.quark_Resolver_md = quark_Resolver.singleton
Root.quark_ResponseHolder_md = quark_ResponseHolder.singleton
Root.quark_Service_md = quark_Service.singleton
Root.quark_BaseService_md = quark_BaseService.singleton
Root.quark_ServiceInstance_md = quark_ServiceInstance.singleton
Root.quark_DegenerateResolver_md = quark_DegenerateResolver.singleton
Root.quark_Client_md = quark_Client.singleton
Root.quark_ServerResponder_md = quark_ServerResponder.singleton
Root.quark_Server_quark_Object__md = quark_Server_quark_Object_.singleton
Root.quark_behaviors_RPCError_md = quark_behaviors_RPCError.singleton
Root.quark_behaviors_RPC_md = quark_behaviors_RPC.singleton
Root.quark_behaviors_RPCRequest_md = quark_behaviors_RPCRequest.singleton
Root.quark_behaviors_CircuitBreaker_md = quark_behaviors_CircuitBreaker.singleton
Root.quark_concurrent_Event_md = quark_concurrent_Event.singleton
Root.quark_concurrent_FutureListener_md = quark_concurrent_FutureListener.singleton
Root.quark_concurrent_FutureCompletion_md = quark_concurrent_FutureCompletion.singleton
Root.quark_concurrent_EventContext_md = quark_concurrent_EventContext.singleton
Root.quark_concurrent_Future_md = quark_concurrent_Future.singleton
Root.quark_concurrent_FutureWait_md = quark_concurrent_FutureWait.singleton
Root.quark_concurrent_Queue_quark_concurrent_Event__md = quark_concurrent_Queue_quark_concurrent_Event_.singleton
Root.quark_concurrent_CollectorExecutor_md = quark_concurrent_CollectorExecutor.singleton
Root.quark_concurrent_Collector_md = quark_concurrent_Collector.singleton
Root.quark_concurrent_TimeoutListener_md = quark_concurrent_TimeoutListener.singleton
Root.quark_concurrent_TimeoutExpiry_md = quark_concurrent_TimeoutExpiry.singleton
Root.quark_concurrent_Timeout_md = quark_concurrent_Timeout.singleton
Root.quark_concurrent_TLSContextInitializer_md = quark_concurrent_TLSContextInitializer.singleton
Root.quark_concurrent_Context_md = quark_concurrent_Context.singleton
Root.quark_HTTPError_md = quark_HTTPError.singleton
Root.quark_HTTPHandler_md = quark_HTTPHandler.singleton
Root.quark_HTTPRequest_md = quark_HTTPRequest.singleton
Root.quark_HTTPResponse_md = quark_HTTPResponse.singleton
Root.quark_HTTPServlet_md = quark_HTTPServlet.singleton
Root.quark_WSError_md = quark_WSError.singleton
Root.quark_WSHandler_md = quark_WSHandler.singleton
Root.quark_WebSocket_md = quark_WebSocket.singleton
Root.quark_WSServlet_md = quark_WSServlet.singleton
Root.quark_test_TestInitializer_md = quark_test_TestInitializer.singleton
Root.quark_test_Test_md = quark_test_Test.singleton
Root.quark_test_SafeMethodCaller_md = quark_test_SafeMethodCaller.singleton
Root.quark_test_MethodTest_md = quark_test_MethodTest.singleton
Root.quark_test_Harness_md = quark_test_Harness.singleton
Root.quark_URL_md = quark_URL.singleton
Root.quark_spi_RuntimeSpi_md = quark_spi_RuntimeSpi.singleton
Root.quark_spi_RuntimeFactory_md = quark_spi_RuntimeFactory.singleton
Root.quark_spi_api_ServletProxy_md = quark_spi_api_ServletProxy.singleton
Root.quark_spi_api_HTTPServletProxy_md = quark_spi_api_HTTPServletProxy.singleton
Root.quark_spi_api_WSServletProxy_md = quark_spi_api_WSServletProxy.singleton
Root.quark_spi_api_TaskProxy_md = quark_spi_api_TaskProxy.singleton
Root.quark_spi_api_RuntimeProxy_md = quark_spi_api_RuntimeProxy.singleton
Root.quark_spi_api_tracing_Identificator_md = quark_spi_api_tracing_Identificator.singleton
Root.quark_spi_api_tracing_Identifiable_md = quark_spi_api_tracing_Identifiable.singleton
Root.quark_spi_api_tracing_ServletProxy_md = quark_spi_api_tracing_ServletProxy.singleton
Root.quark_spi_api_tracing_HTTPRequestProxy_md = quark_spi_api_tracing_HTTPRequestProxy.singleton
Root.quark_spi_api_tracing_HTTPResponseProxy_md = quark_spi_api_tracing_HTTPResponseProxy.singleton
Root.quark_spi_api_tracing_HTTPServletProxy_md = quark_spi_api_tracing_HTTPServletProxy.singleton
Root.quark_spi_api_tracing_WSServletProxy_md = quark_spi_api_tracing_WSServletProxy.singleton
Root.quark_spi_api_tracing_TaskProxy_md = quark_spi_api_tracing_TaskProxy.singleton
Root.quark_spi_api_tracing_WebSocketProxy_md = quark_spi_api_tracing_WebSocketProxy.singleton
Root.quark_spi_api_tracing_WSHandlerProxy_md = quark_spi_api_tracing_WSHandlerProxy.singleton
Root.quark_spi_api_tracing_HTTPHandlerProxy_md = quark_spi_api_tracing_HTTPHandlerProxy.singleton
Root.quark_spi_api_tracing_RuntimeProxy_md = quark_spi_api_tracing_RuntimeProxy.singleton
Root.quark_os_OSError_md = quark_os_OSError.singleton
Root.quark_os_FileContents_md = quark_os_FileContents.singleton
Root.quark_os_Environment_md = quark_os_Environment.singleton
Root.quark_mock_MockEvent_md = quark_mock_MockEvent.singleton
Root.quark_mock_SocketEvent_md = quark_mock_SocketEvent.singleton
Root.quark_mock_MockMessage_md = quark_mock_MockMessage.singleton
Root.quark_mock_TextMessage_md = quark_mock_TextMessage.singleton
Root.quark_mock_BinaryMessage_md = quark_mock_BinaryMessage.singleton
Root.quark_mock_MockSocket_md = quark_mock_MockSocket.singleton
Root.quark_mock_RequestEvent_md = quark_mock_RequestEvent.singleton
Root.quark_mock_MockResponse_md = quark_mock_MockResponse.singleton
Root.quark_mock_MockTask_md = quark_mock_MockTask.singleton
Root.quark_mock_MockRuntime_md = quark_mock_MockRuntime.singleton
Root.quark_mock_MockRuntimeTest_md = quark_mock_MockRuntimeTest.singleton
Root.quark__ChainPromise_md = quark__ChainPromise.singleton
Root.quark__CallbackEvent_md = quark__CallbackEvent.singleton
Root.quark__Callback_md = quark__Callback.singleton
Root.quark__Passthrough_md = quark__Passthrough.singleton
Root.quark__CallIfIsInstance_md = quark__CallIfIsInstance.singleton
Root.quark_PromiseValue_md = quark_PromiseValue.singleton
Root.quark_Promise_md = quark_Promise.singleton
Root.quark_PromiseFactory_md = quark_PromiseFactory.singleton
Root.quark__BoundMethod_md = quark__BoundMethod.singleton
Root.quark__IOScheduleTask_md = quark__IOScheduleTask.singleton
Root.quark__IOHTTPHandler_md = quark__IOHTTPHandler.singleton
Root.quark_IO_md = quark_IO.singleton
Root.mdk_runtime_Dependencies_md = mdk_runtime_Dependencies.singleton
Root.mdk_runtime_MDKRuntime_md = mdk_runtime_MDKRuntime.singleton
Root.mdk_runtime_Time_md = mdk_runtime_Time.singleton
Root.mdk_runtime_SchedulingActor_md = mdk_runtime_SchedulingActor.singleton
Root.mdk_runtime_WebSockets_md = mdk_runtime_WebSockets.singleton
Root.mdk_runtime_WSConnectError_md = mdk_runtime_WSConnectError.singleton
Root.mdk_runtime_WSActor_md = mdk_runtime_WSActor.singleton
Root.mdk_runtime_WSMessage_md = mdk_runtime_WSMessage.singleton
Root.mdk_runtime_WSClose_md = mdk_runtime_WSClose.singleton
Root.mdk_runtime_WSClosed_md = mdk_runtime_WSClosed.singleton
Root.mdk_runtime_QuarkRuntimeWSActor_md = mdk_runtime_QuarkRuntimeWSActor.singleton
Root.mdk_runtime_QuarkRuntimeWebSockets_md = mdk_runtime_QuarkRuntimeWebSockets.singleton
Root.mdk_runtime_FakeWSActor_md = mdk_runtime_FakeWSActor.singleton
Root.mdk_runtime_FakeWebSockets_md = mdk_runtime_FakeWebSockets.singleton
Root.mdk_runtime_Schedule_md = mdk_runtime_Schedule.singleton
Root.mdk_runtime_Happening_md = mdk_runtime_Happening.singleton
Root.mdk_runtime__ScheduleTask_md = mdk_runtime__ScheduleTask.singleton
Root.mdk_runtime_QuarkRuntimeTime_md = mdk_runtime_QuarkRuntimeTime.singleton
Root.mdk_runtime__FakeTimeRequest_md = mdk_runtime__FakeTimeRequest.singleton
Root.mdk_runtime_FakeTime_md = mdk_runtime_FakeTime.singleton
Root.mdk_runtime_EnvironmentVariable_md = mdk_runtime_EnvironmentVariable.singleton
Root.mdk_runtime_EnvironmentVariables_md = mdk_runtime_EnvironmentVariables.singleton
Root.mdk_runtime_RealEnvVars_md = mdk_runtime_RealEnvVars.singleton
Root.mdk_runtime_FakeEnvVars_md = mdk_runtime_FakeEnvVars.singleton
Root.mdk_runtime_actors_Actor_md = mdk_runtime_actors_Actor.singleton
Root.mdk_runtime_actors__QueuedMessage_md = mdk_runtime_actors__QueuedMessage.singleton
Root.mdk_runtime_actors__InFlightMessage_md = mdk_runtime_actors__InFlightMessage.singleton
Root.mdk_runtime_actors__StartStopActor_md = mdk_runtime_actors__StartStopActor.singleton
Root.mdk_runtime_actors_MessageDispatcher_md = mdk_runtime_actors_MessageDispatcher.singleton
Root.mdk_runtime_promise__ChainPromise_md = mdk_runtime_promise__ChainPromise.singleton
Root.mdk_runtime_promise__CallbackEvent_md = mdk_runtime_promise__CallbackEvent.singleton
Root.mdk_runtime_promise__Callback_md = mdk_runtime_promise__Callback.singleton
Root.mdk_runtime_promise__Passthrough_md = mdk_runtime_promise__Passthrough.singleton
Root.mdk_runtime_promise__CallIfIsInstance_md = mdk_runtime_promise__CallIfIsInstance.singleton
Root.mdk_runtime_promise_PromiseValue_md = mdk_runtime_promise_PromiseValue.singleton
Root.mdk_runtime_promise_Promise_md = mdk_runtime_promise_Promise.singleton
Root.mdk_runtime_promise_PromiseResolver_md = mdk_runtime_promise_PromiseResolver.singleton
Root.mdk_runtime_files_SubscribeChanges_md = mdk_runtime_files_SubscribeChanges.singleton
Root.mdk_runtime_files_FileContents_md = mdk_runtime_files_FileContents.singleton
Root.mdk_runtime_files_FileDeleted_md = mdk_runtime_files_FileDeleted.singleton
Root.mdk_runtime_files_FileActor_md = mdk_runtime_files_FileActor.singleton
Root.mdk_runtime_files_FileActorImpl_md = mdk_runtime_files_FileActorImpl.singleton
Root.mdk_runtime_files__Subscription_md = mdk_runtime_files__Subscription.singleton
Root.mdk_util_WaitForPromise_md = mdk_util_WaitForPromise.singleton
Root.mdk_introspection_Supplier_quark_Object__md = mdk_introspection_Supplier_quark_Object_.singleton
Root.mdk_introspection_DatawireToken_md = mdk_introspection_DatawireToken.singleton
Root.mdk_introspection_Platform_md = mdk_introspection_Platform.singleton
Root.mdk_introspection_aws_Ec2Host_md = mdk_introspection_aws_Ec2Host.singleton
Root.mdk_introspection_kubernetes_KubernetesHost_md = mdk_introspection_kubernetes_KubernetesHost.singleton
Root.mdk_introspection_kubernetes_KubernetesPort_md = mdk_introspection_kubernetes_KubernetesPort.singleton
Root.mdk_discovery_NodeActive_md = mdk_discovery_NodeActive.singleton
Root.mdk_discovery_NodeExpired_md = mdk_discovery_NodeExpired.singleton
Root.mdk_discovery_ReplaceCluster_md = mdk_discovery_ReplaceCluster.singleton
Root.mdk_discovery_DiscoverySource_md = mdk_discovery_DiscoverySource.singleton
Root.mdk_discovery_DiscoverySourceFactory_md = mdk_discovery_DiscoverySourceFactory.singleton
Root.mdk_discovery__StaticRoutesActor_md = mdk_discovery__StaticRoutesActor.singleton
Root.mdk_discovery_StaticRoutes_md = mdk_discovery_StaticRoutes.singleton
Root.mdk_discovery_RegisterNode_md = mdk_discovery_RegisterNode.singleton
Root.mdk_discovery_DiscoveryRegistrar_md = mdk_discovery_DiscoveryRegistrar.singleton
Root.mdk_discovery__Request_md = mdk_discovery__Request.singleton
Root.mdk_discovery_FailurePolicy_md = mdk_discovery_FailurePolicy.singleton
Root.mdk_discovery_FailurePolicyFactory_md = mdk_discovery_FailurePolicyFactory.singleton
Root.mdk_discovery_CircuitBreaker_md = mdk_discovery_CircuitBreaker.singleton
Root.mdk_discovery_CircuitBreakerFactory_md = mdk_discovery_CircuitBreakerFactory.singleton
Root.mdk_discovery_RecordingFailurePolicy_md = mdk_discovery_RecordingFailurePolicy.singleton
Root.mdk_discovery_RecordingFailurePolicyFactory_md = mdk_discovery_RecordingFailurePolicyFactory.singleton
Root.mdk_discovery_Cluster_md = mdk_discovery_Cluster.singleton
Root.mdk_discovery_Node_md = mdk_discovery_Node.singleton
Root.mdk_discovery_Discovery_md = mdk_discovery_Discovery.singleton
Root.mdk_discovery_protocol_DiscoClientFactory_md = mdk_discovery_protocol_DiscoClientFactory.singleton
Root.mdk_discovery_protocol_DiscoClient_md = mdk_discovery_protocol_DiscoClient.singleton
Root.mdk_discovery_protocol_Active_md = mdk_discovery_protocol_Active.singleton
Root.mdk_discovery_protocol_Expire_md = mdk_discovery_protocol_Expire.singleton
Root.mdk_discovery_protocol_Clear_md = mdk_discovery_protocol_Clear.singleton
Root.mdk_protocol_Serializable_md = mdk_protocol_Serializable.singleton
Root.mdk_protocol_LamportClock_md = mdk_protocol_LamportClock.singleton
Root.mdk_protocol_SharedContext_md = mdk_protocol_SharedContext.singleton
Root.mdk_protocol_Open_md = mdk_protocol_Open.singleton
Root.mdk_protocol_ProtocolError_md = mdk_protocol_ProtocolError.singleton
Root.mdk_protocol_Close_md = mdk_protocol_Close.singleton
Root.mdk_protocol_Pump_md = mdk_protocol_Pump.singleton
Root.mdk_protocol_WSConnected_md = mdk_protocol_WSConnected.singleton
Root.mdk_protocol_DecodedMessage_md = mdk_protocol_DecodedMessage.singleton
Root.mdk_protocol_WSClientSubscriber_md = mdk_protocol_WSClientSubscriber.singleton
Root.mdk_protocol_OpenCloseSubscriber_md = mdk_protocol_OpenCloseSubscriber.singleton
Root.mdk_protocol_JSONParser_md = mdk_protocol_JSONParser.singleton
Root.mdk_protocol_WSClient_md = mdk_protocol_WSClient.singleton
Root.mdk_discovery_synapse_Synapse_md = mdk_discovery_synapse_Synapse.singleton
Root.mdk_discovery_synapse__SynapseSource_md = mdk_discovery_synapse__SynapseSource.singleton
Root.mdk_tracing_SharedContextInitializer_md = mdk_tracing_SharedContextInitializer.singleton
Root.mdk_tracing_Tracer_md = mdk_tracing_Tracer.singleton
Root.mdk_tracing_api_ApiHandler_md = mdk_tracing_api_ApiHandler.singleton
Root.mdk_tracing_api_GetLogEventsRequest_md = mdk_tracing_api_GetLogEventsRequest.singleton
Root.mdk_tracing_api_GetLogEventsResult_md = mdk_tracing_api_GetLogEventsResult.singleton
Root.mdk_tracing_protocol_LogEvent_md = mdk_tracing_protocol_LogEvent.singleton
Root.mdk_tracing_protocol_Subscribe_md = mdk_tracing_protocol_Subscribe.singleton
Root.mdk_tracing_protocol_LogAck_md = mdk_tracing_protocol_LogAck.singleton
Root.mdk_tracing_protocol_TracingClient_md = mdk_tracing_protocol_TracingClient.singleton

def _lazy_import_mdk():
    import mdk
    globals().update(locals())
_lazyImport("import mdk", _lazy_import_mdk)

def _lazy_import_quark():
    import quark
    globals().update(locals())
_lazyImport("import quark", _lazy_import_quark)

def _lazy_import_mdk_runtime():
    import mdk_runtime
    globals().update(locals())
_lazyImport("import mdk_runtime", _lazy_import_mdk_runtime)

def _lazy_import_mdk_discovery():
    import mdk_discovery
    globals().update(locals())
_lazyImport("import mdk_discovery", _lazy_import_mdk_discovery)

def _lazy_import_quark_concurrent():
    import quark.concurrent
    globals().update(locals())
_lazyImport("import quark.concurrent", _lazy_import_quark_concurrent)

def _lazy_import_quark_test():
    import quark.test
    globals().update(locals())
_lazyImport("import quark.test", _lazy_import_quark_test)

def _lazy_import_quark_mock():
    import quark.mock
    globals().update(locals())
_lazyImport("import quark.mock", _lazy_import_quark_mock)

def _lazy_import_mdk_runtime_actors():
    import mdk_runtime.actors
    globals().update(locals())
_lazyImport("import mdk_runtime.actors", _lazy_import_mdk_runtime_actors)

def _lazy_import_mdk_runtime_promise():
    import mdk_runtime.promise
    globals().update(locals())
_lazyImport("import mdk_runtime.promise", _lazy_import_mdk_runtime_promise)

def _lazy_import_mdk_runtime_files():
    import mdk_runtime.files
    globals().update(locals())
_lazyImport("import mdk_runtime.files", _lazy_import_mdk_runtime_files)

def _lazy_import_mdk_tracing_protocol():
    import mdk_tracing.protocol
    globals().update(locals())
_lazyImport("import mdk_tracing.protocol", _lazy_import_mdk_tracing_protocol)

def _lazy_import_quark_error():
    import quark.error
    globals().update(locals())
_lazyImport("import quark.error", _lazy_import_quark_error)

def _lazy_import_quark_logging():
    import quark.logging
    globals().update(locals())
_lazyImport("import quark.logging", _lazy_import_quark_logging)

def _lazy_import_quark_behaviors():
    import quark.behaviors
    globals().update(locals())
_lazyImport("import quark.behaviors", _lazy_import_quark_behaviors)

def _lazy_import_quark_spi():
    import quark.spi
    globals().update(locals())
_lazyImport("import quark.spi", _lazy_import_quark_spi)

def _lazy_import_quark_spi_api():
    import quark.spi_api
    globals().update(locals())
_lazyImport("import quark.spi_api", _lazy_import_quark_spi_api)

def _lazy_import_quark_spi_api_tracing():
    import quark.spi_api_tracing
    globals().update(locals())
_lazyImport("import quark.spi_api_tracing", _lazy_import_quark_spi_api_tracing)

def _lazy_import_quark_os():
    import quark.os
    globals().update(locals())
_lazyImport("import quark.os", _lazy_import_quark_os)

def _lazy_import_mdk_util():
    import mdk_util
    globals().update(locals())
_lazyImport("import mdk_util", _lazy_import_mdk_util)

def _lazy_import_mdk_introspection():
    import mdk_introspection
    globals().update(locals())
_lazyImport("import mdk_introspection", _lazy_import_mdk_introspection)

def _lazy_import_mdk_introspection_aws():
    import mdk_introspection.aws
    globals().update(locals())
_lazyImport("import mdk_introspection.aws", _lazy_import_mdk_introspection_aws)

def _lazy_import_mdk_introspection_kubernetes():
    import mdk_introspection.kubernetes
    globals().update(locals())
_lazyImport("import mdk_introspection.kubernetes", _lazy_import_mdk_introspection_kubernetes)

def _lazy_import_mdk_discovery_protocol():
    import mdk_discovery.protocol
    globals().update(locals())
_lazyImport("import mdk_discovery.protocol", _lazy_import_mdk_discovery_protocol)

def _lazy_import_mdk_protocol():
    import mdk_protocol
    globals().update(locals())
_lazyImport("import mdk_protocol", _lazy_import_mdk_protocol)

def _lazy_import_mdk_discovery_synapse():
    import mdk_discovery.synapse
    globals().update(locals())
_lazyImport("import mdk_discovery.synapse", _lazy_import_mdk_discovery_synapse)

def _lazy_import_mdk_tracing():
    import mdk_tracing
    globals().update(locals())
_lazyImport("import mdk_tracing", _lazy_import_mdk_tracing)

def _lazy_import_mdk_tracing_api():
    import mdk_tracing.api
    globals().update(locals())
_lazyImport("import mdk_tracing.api", _lazy_import_mdk_tracing_api)



_lazyImport.pump("datawire_mdk_md.mdk_MDK_start_Method")
