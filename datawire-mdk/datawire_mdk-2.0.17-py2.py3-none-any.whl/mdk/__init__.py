# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime
import mdk_discovery
import quark
import mdk_protocol
import mdk_tracing
import quark.concurrent
import mdk_introspection
import mdk_discovery.protocol
import mdk_discovery.synapse
import mdk_rtp
import mdk_runtime.promise
import mdk_util



def _get(env, name, value):
    return ((env).var(name)).orElseGet(value)


def init():
    """
    Create an unstarted instance of the MDK.
    """
    return MDKImpl(mdk_runtime.defaultRuntime())


def start():
    """
    Create a started instance of the MDK. This is equivalent to
    calling init() followed by start() on the resulting instance.

    """
    m = init();
    (m).start();
    return m

class MDK(object):
    """
    The MDK API consists of two interfaces: MDK and Session. The
    MDK interface holds globally scoped APIs and state associated
    with the microservice. The Session interface holds locally
    scoped APIs and state. A Session must be used sequentially.

    The MDK instance is responsible for communicating with
    foundational services like discovery and tracing.

    There will typically be one MDK instance for the entire
    process, and one instance of the Session object per
    thread/channel/request depending on how the MDK is integrated
    and used within the application framework of choice.

    """

    def start(self):
        """
        Start the MDK. An MDK instance will not communicate with
        foundational services unless it is started.

        """
        raise NotImplementedError('`MDK.start` is an abstract method')

    def stop(self):
        """
        Stop the MDK. When the MDK stops unregisters any service
        endpoints from the discovery system. This should always
        be done prior to process exit in order to propogate node
        shutdowns in realtime rather than waiting for heartbeats
        to detect node departures.

        """
        raise NotImplementedError('`MDK.stop` is an abstract method')

    def register(self, service, version, address):
        """
        Registers a service endpoint with the discovery
        system. This can be called at any point, however
        registered endpoints will not be advertised to the
        discovery system until the MDK is started.

        """
        raise NotImplementedError('`MDK.register` is an abstract method')

    def setDefaultTimeout(self, seconds):
        """
        Set the default timeout for MDK sessions.

        This is the maximum timeout; if a joined session has a lower
        timeout that will be used.

        """
        raise NotImplementedError('`MDK.setDefaultTimeout` is an abstract method')

    def session(self):
        """
        Creates a new Session. A Session created in this way will
        result in a new distributed trace. This should therefore
        be used primarily by edge services. Intermediary and
        foundational services should make use of
        join(encodedContext) in order to preserve distributed
        traces.

        """
        raise NotImplementedError('`MDK.session` is an abstract method')

    def join(self, encodedContext):
        """
        Create a new Session and join it to a distributed trace.

        """
        raise NotImplementedError('`MDK.join` is an abstract method')

MDK.CONTEXT_HEADER = u"X-MDK-Context"
MDK.mdk_MDK_ref = None
class Session(object):
    """
    A session provides a lightweight sequential context that a
    microservice can use in the context of any application
    framework in order to manage its interactions with other
    microservices. It provides simple APIs for service
    resolution, distributed tracing, and circuit breakers.

    A microservices architecture enables small self contained
    units of business logic to be implemented by separate teams
    working on isolated services based on the languages and
    frameworks best suited for their problem domain.

    Any given microservice will contain sequential business logic
    implemented in a variety of ways depending on the application
    framework chosen. For example it may be a long running
    thread, a simple blocking request handler, or a chained
    series of reactive handlers in an async environment.

    For the most part this business logic can be implemented
    exactly as prescribed by the application framework of choice,
    however in a microservices architecture, some special care
    needs to be taken when this business logic interacts with
    other microservices.

    Because microservices are updated with much higher frequency
    than normal web applications, the interactions between them
    form key points that require extra care beyond normal web
    interactions in order to avoid creating a system that is both
    extremely fragile, unreliable, and opaque.

    Realtime service resolution, distributed tracing, and
    resilience heuristics such as circuit breakers provide the
    foundational behavior required at these interaction
    points. These capabilites must be combined with the defensive
    coding practice of intelligent fallback behavior when remote
    services are unavailable or misbehaving, in order to build a
    robust microservice application.

    Because of this, a session is expected to be created and made
    available to all business logic within a given microservice,
    e.g. on a per request basis, as a thread local, part of a
    context object, etc depending on the application framework of
    choice.

    """

    def inject(self):
        """
        Grabs the encoded context.
        """
        raise NotImplementedError('`Session.inject` is an abstract method')

    def externalize(self):
        """
        Returns an externalized representation of the distributed session.
        """
        raise NotImplementedError('`Session.externalize` is an abstract method')

    def critical(self, category, text):
        """
        Record a log entry at the CRITICAL logging level.
        """
        raise NotImplementedError('`Session.critical` is an abstract method')

    def error(self, category, text):
        """
        Record a log entry at the ERROR logging level.
        """
        raise NotImplementedError('`Session.error` is an abstract method')

    def warn(self, category, text):
        """
        Record a log entry at the WARN logging level.
        """
        raise NotImplementedError('`Session.warn` is an abstract method')

    def info(self, category, text):
        """
        Record a log entry at the INFO logging level.
        """
        raise NotImplementedError('`Session.info` is an abstract method')

    def debug(self, category, text):
        """
        Record a log entry at the DEBUG logging level.
        """
        raise NotImplementedError('`Session.debug` is an abstract method')

    def trace(self, level):
        """
        EXPERIMENTAL: Set the logging level for the session.
        """
        raise NotImplementedError('`Session.trace` is an abstract method')

    def route(self, service, version, target, targetVersion):
        """
        EXPERIMENTAL; requires MDK_EXPERIMENTAL=1 environment variable to
        function.

        Override service resolution for the current distributed
        session. All attempts to resolve *service*, *version*
        will be replaced with an attempt to resolve *target*,
        *targetVersion*. This effect will be propogated to any
        downstream services involved in the distributed session.

        """
        raise NotImplementedError('`Session.route` is an abstract method')

    def resolve(self, service, version):
        """
        Locate a compatible service instance.

        Uses a minimum of 10 seconds and the timeout set on the session.

        """
        raise NotImplementedError('`Session.resolve` is an abstract method')

    def resolve_until(self, service, version, timeout):
        """
        Locate a compatible service instance with a non-default timeout.

        """
        raise NotImplementedError('`Session.resolve_until` is an abstract method')

    def resolve_async(self, service, version):
        """
        Locate a compatible service instance asynchronously. The result is returned as a promise.

        """
        raise NotImplementedError('`Session.resolve_async` is an abstract method')

    def start_interaction(self):
        """
        Start an interaction with a remote service.

        The session tracks any nodes resolved during an
        interactin with a remote service.

        The service resolution API permits a compatible instance
        of the service to be located. In addition, it tracks
        which exact instances are in use during any
        interaction. Should the interaction fail, circuit breaker
        state is updated for those nodes, and all involved
        instances involved are reported to the tracing services.

        This permits realtime reporting of integration issues
        when services are updated, and also allows circuit
        breakers to mitigate the impact of any such issues.

        """
        raise NotImplementedError('`Session.start_interaction` is an abstract method')

    def fail_interaction(self, message):
        """
        Record an interaction as failed.

        This will update circuit breaker state for the remote
        nodes, as well as reporting all nodes involved to the
        tracing system.

        """
        raise NotImplementedError('`Session.fail_interaction` is an abstract method')

    def finish_interaction(self):
        """
        Finish an interaction.

        This marks an interaction as completed.

        """
        raise NotImplementedError('`Session.finish_interaction` is an abstract method')

    def interact(self, callable):
        """
        This is a convenience API that will perform
        start_interaction() followed by callable(ssn) followed by
        finish_interaction().

        """
        raise NotImplementedError('`Session.interact` is an abstract method')

    def setTimeout(self, seconds):
        """
        Set how many seconds the session is expected to live from this point.

        If a timeout has previously been set the new timeout will only be
        used if it is lower than the existing timeout.

        The MDK will not enforce the timeout. Rather, it provides the
        information to any process or server in the same session (even if
        they are on different machines). By passing this timeout to
        blocking APIs you can ensure timeouts are enforced across a whole
        distributed session.

        """
        raise NotImplementedError('`Session.setTimeout` is an abstract method')

    def getRemainingTime(self):
        """
        Return how many seconds until the session ought to end.

        This will only be accurate across multiple servers insofar as their
        clocks are in sync.

        If a timeout has not been set the result will be null.

        """
        raise NotImplementedError('`Session.getRemainingTime` is an abstract method')

Session.mdk_Session_ref = None
class MDKImpl(_QObject):
    def _init(self):
        self.logger = quark._getLogger(u"mdk")
        self._reflection_hack = None
        self._runtime = None
        self._wsclient = None
        self._openclose = None
        self._disco = None
        self._discoSource = None
        self._tracer = None
        self.procUUID = (quark.concurrent.Context.runtime()).uuid()
        self._running = False
        self._defaultTimeout = None

    def __init__(self, runtime):
        self._init()
        self._reflection_hack = _Map()
        self._runtime = runtime
        if (not (((runtime).dependencies).hasService(u"failurepolicy_factory"))):
            ((runtime).dependencies).registerService(u"failurepolicy_factory", self.getFailurePolicy(runtime));

        self._disco = mdk_discovery.Discovery(runtime)
        self._wsclient = self.getWSClient(runtime)
        if ((self._wsclient) != (None)):
            self._openclose = mdk_protocol.OpenCloseSubscriber(self._wsclient)

        env = (runtime).getEnvVarsService();
        discoFactory = self.getDiscoveryFactory(env);
        self._discoSource = (discoFactory).create(self._disco, runtime)
        if ((discoFactory).isRegistrar()):
            ((runtime).dependencies).registerService(u"discovery_registrar", self._discoSource);

        if ((self._wsclient) != (None)):
            self._tracer = mdk_tracing.Tracer(runtime, self._wsclient)
            (self._tracer).initContext();

    def getDiscoveryFactory(self, env):
        """
        Choose DiscoverySource based on environment variables.
        """
        config = ((env).var(u"MDK_DISCOVERY_SOURCE")).orElseGet(u"");
        if ((config) == (u"")):
            config = (u"datawire:") + (mdk_introspection.DatawireToken.getToken(env))

        result = _cast(None, lambda: mdk_discovery.DiscoverySourceFactory);
        if ((config).startswith(u"datawire:")):
            result = mdk_discovery.protocol.DiscoClientFactory(self._wsclient)
        else:
            if ((config).startswith(u"synapse:path=")):
                result = mdk_discovery.synapse.Synapse((config)[(13):(len(config))])
            else:
                if ((config).startswith(u"static:nodes=")):
                    json = (config)[(13):(len(config))];
                    result = mdk_discovery.StaticRoutes.parseJSON(json)
                else:
                    raise Exception((u"Unknown MDK discovery source: ") + (config));

        return result

    def getFailurePolicy(self, runtime):
        """
        Choose FailurePolicy based on environment variables.
        """
        config = (((runtime).getEnvVarsService()).var(u"MDK_FAILURE_POLICY")).orElseGet(u"");
        if ((config) == (u"recording")):
            return mdk_discovery.RecordingFailurePolicyFactory()
        else:
            return mdk_discovery.CircuitBreakerFactory(runtime)

    def getWSClient(self, runtime):
        """
        Get a WSClient, unless env variables suggest the user doesn't want one.
        """
        env = (runtime).getEnvVarsService();
        token = ((env).var(u"DATAWIRE_TOKEN")).orElseGet(u"");
        disco_config = ((env).var(u"MDK_DISCOVERY_SOURCE")).orElseGet(u"");
        if ((token) == (u"")):
            if ((disco_config).startswith(u"datawire:")):
                token = (disco_config)[(9):(len(disco_config))]
            else:
                return _cast(None, lambda: mdk_protocol.WSClient)

        ddu = (env).var(u"MDK_SERVER_URL");
        url = (ddu).orElseGet(u"wss://mcp.datawire.io/rtp");
        return mdk_protocol.WSClient(runtime, mdk_rtp.getRTPParser(), url, token)

    def _timeout(self):
        return 10.0

    def start(self):
        (self)._running = True
        if ((self._wsclient) != (None)):
            ((self._runtime).dispatcher).startActor(self._wsclient);
            ((self._runtime).dispatcher).startActor(self._openclose);
            ((self._runtime).dispatcher).startActor(self._tracer);

        ((self._runtime).dispatcher).startActor(self._disco);
        ((self._runtime).dispatcher).startActor(self._discoSource);

    def stop(self):
        (self)._running = False
        ((self._runtime).dispatcher).stopActor(self._discoSource);
        ((self._runtime).dispatcher).stopActor(self._disco);
        if ((self._wsclient) != (None)):
            ((self._runtime).dispatcher).stopActor(self._tracer);
            ((self._runtime).dispatcher).stopActor(self._openclose);
            ((self._runtime).dispatcher).stopActor(self._wsclient);

        (self._runtime).stop();

    def register(self, service, version, address):
        node = mdk_discovery.Node();
        (node).service = service
        (node).version = version
        (node).address = address
        (node).properties = {u"datawire_nodeId": self.procUUID}
        (self._disco).register(node);

    def setDefaultTimeout(self, seconds):
        (self)._defaultTimeout = seconds

    def session(self):
        session = SessionImpl(self, None);
        if ((self._defaultTimeout) != (None)):
            (session).setTimeout(self._defaultTimeout);

        return session

    def join(self, encodedContext):
        session = SessionImpl(self, encodedContext);
        if ((self._defaultTimeout) != (None)):
            (session).setTimeout(self._defaultTimeout);

        return session

    def _getClass(self):
        return u"mdk.MDKImpl"

    def _getField(self, name):
        if ((name) == (u"CONTEXT_HEADER")):
            return MDK.CONTEXT_HEADER

        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"_reflection_hack")):
            return (self)._reflection_hack

        if ((name) == (u"_runtime")):
            return (self)._runtime

        if ((name) == (u"_wsclient")):
            return (self)._wsclient

        if ((name) == (u"_openclose")):
            return (self)._openclose

        if ((name) == (u"_disco")):
            return (self)._disco

        if ((name) == (u"_discoSource")):
            return (self)._discoSource

        if ((name) == (u"_tracer")):
            return (self)._tracer

        if ((name) == (u"procUUID")):
            return (self).procUUID

        if ((name) == (u"_running")):
            return (self)._running

        if ((name) == (u"_defaultTimeout")):
            return (self)._defaultTimeout

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"_reflection_hack")):
            (self)._reflection_hack = _cast(value, lambda: _Map)

        if ((name) == (u"_runtime")):
            (self)._runtime = _cast(value, lambda: mdk_runtime.MDKRuntime)

        if ((name) == (u"_wsclient")):
            (self)._wsclient = _cast(value, lambda: mdk_protocol.WSClient)

        if ((name) == (u"_openclose")):
            (self)._openclose = _cast(value, lambda: mdk_protocol.OpenCloseSubscriber)

        if ((name) == (u"_disco")):
            (self)._disco = _cast(value, lambda: mdk_discovery.Discovery)

        if ((name) == (u"_discoSource")):
            (self)._discoSource = _cast(value, lambda: mdk_discovery.DiscoverySource)

        if ((name) == (u"_tracer")):
            (self)._tracer = _cast(value, lambda: mdk_tracing.Tracer)

        if ((name) == (u"procUUID")):
            (self).procUUID = _cast(value, lambda: unicode)

        if ((name) == (u"_running")):
            (self)._running = _cast(value, lambda: bool)

        if ((name) == (u"_defaultTimeout")):
            (self)._defaultTimeout = _cast(value, lambda: float)


MDKImpl.mdk_MDKImpl_ref = None
MDKImpl.quark_Map_quark_String_quark_Object__ref = None
MDKImpl.CONTEXT_HEADER = u"X-MDK-Context"
class _TLSInit(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def getValue(self):
        return False

    def _getClass(self):
        return u"mdk._TLSInit"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
_TLSInit.mdk__TLSInit_ref = None
class SessionImpl(_QObject):
    def _init(self):
        self._mdk = None
        self._resolved = _List([_List([])])
        self._context = None
        self._experimental = False

    def __init__(self, mdk, encodedContext):
        self._init()
        self._experimental = (((((mdk)._runtime).getEnvVarsService()).var(u"MDK_EXPERIMENTAL")).orElseGet(u"")) != (u"")
        self._mdk = mdk
        encodedContext = _cast(encodedContext, lambda: unicode)
        if (((encodedContext) == (None)) or ((encodedContext) == (u""))):
            self._context = mdk_protocol.SharedContext()
        else:
            ctx = mdk_protocol.SharedContext.decode(encodedContext);
            self._context = (ctx).start_span()

    def get(self, property):
        return ((self._context).properties).get(property)

    def set(self, property, value):
        ((self._context).properties)[property] = (value);

    def has(self, property):
        return (property) in ((self._context).properties)

    def setTimeout(self, timeout):
        current = self.getRemainingTime();
        if ((current) == (None)):
            current = timeout

        if ((timeout) > (current)):
            timeout = current

        self.set(u"timeout", ((((self._mdk)._runtime).getTimeService()).time()) + (timeout));

    def getRemainingTime(self):
        deadline = _cast(self.get(u"timeout"), lambda: float);
        if ((deadline) == (None)):
            return _cast(None, lambda: float)

        return (deadline) - ((((self._mdk)._runtime).getTimeService()).time())

    def route(self, service, version, target, targetVersion):
        routes = None;
        if (not (self.has(u"routes"))):
            routes = {}
            self.set(u"routes", routes);
        else:
            routes = _cast(self.get(u"routes"), lambda: _Map)

        targets = None;
        if ((service) in (routes)):
            targets = (routes).get(service)
        else:
            targets = _List([])
            (routes)[service] = (targets);

        (targets).append({u"version": version, u"target": target, u"targetVersion": targetVersion});

    def trace(self, level):
        self.set(u"trace", level);

    @staticmethod
    def _level(level):
        if ((level) in (SessionImpl._levels)):
            return (SessionImpl._levels).get(level)
        else:
            return 0

    def _enabled(self, level):
        ilevel = SessionImpl._level(u"INFO");
        if (self.has(u"trace")):
            ilevel = SessionImpl._level(_cast(self.get(u"trace"), lambda: unicode))

        return (SessionImpl._level(level)) <= (ilevel)

    def _log(self, level, category, text):
        if (((self._mdk)._tracer) != (None)):
            if ((SessionImpl._inLogging).getValue()):
                return

            (SessionImpl._inLogging).setValue(True);
            ((self._mdk)._tracer).setContext(self._context);
            ((self._mdk)._tracer).log((self._mdk).procUUID, level, category, text);
            (SessionImpl._inLogging).setValue(False);

    def critical(self, category, text):
        if (self._enabled(u"CRITICAL")):
            self._log(u"CRITICAL", category, text);

    def error(self, category, text):
        if (self._enabled(u"ERROR")):
            self._log(u"ERROR", category, text);

    def warn(self, category, text):
        if (self._enabled(u"WARN")):
            self._log(u"WARN", category, text);

    def info(self, category, text):
        if (self._enabled(u"INFO")):
            self._log(u"INFO", category, text);

    def debug(self, category, text):
        if (self._enabled(u"DEBUG")):
            self._log(u"DEBUG", category, text);

    def _resolve(self, service, version):
        if (self._experimental):
            routes = _cast(self.get(u"routes"), lambda: _Map);
            if (((routes) != (None)) and ((service) in (routes))):
                targets = (routes).get(service);
                idx = 0;
                while ((idx) < (len(targets))):
                    target = (targets)[idx];
                    if (mdk_util.versionMatch((target).get(u"version"), version)):
                        service = (target).get(u"target")
                        version = (target).get(u"targetVersion")
                        break;

                    idx = (idx) + (1)

        return (((self._mdk)._disco)._resolve(service, version)).andThen(quark._BoundMethod(self, u"_resolvedCallback", _List([])))

    def resolve_async(self, service, version):
        return mdk_util.toNativePromise(self._resolve(service, version))

    def resolve(self, service, version):
        timeout = (self._mdk)._timeout();
        session_timeout = (self).getRemainingTime();
        if (((session_timeout) != (None)) and ((session_timeout) < (timeout))):
            timeout = session_timeout

        return self.resolve_until(service, version, timeout)

    def resolve_until(self, service, version, timeout):
        return _cast(mdk_util.WaitForPromise.wait((self)._resolve(service, version), timeout, ((((u"service ") + (service)) + (u"(")) + (version)) + (u")")), lambda: mdk_discovery.Node)

    def _resolvedCallback(self, result):
        (self._current_interaction()).append(result);
        return result

    def _current_interaction(self):
        return (self._resolved)[(len(self._resolved)) - (1)]

    def start_interaction(self):
        (self._resolved).append(_List([]));

    def inject(self):
        return self.externalize()

    def externalize(self):
        result = (self._context).encode();
        (self._context).tick();
        return result

    def fail_interaction(self, message):
        suspects = self._current_interaction();
        (self._resolved)[(len(self._resolved)) - (1)] = (_List([]));
        involved = _List([]);
        idx = 0;
        while ((idx) < (len(suspects))):
            node = (suspects)[idx];
            idx = (idx) + (1)
            (involved).append((node).toString());
            (node).failure();

        text = (((u"involved: ") + ((u", ").join(involved))) + (u"\n\n")) + (message);
        (self).error(u"interaction failure", text);

    def finish_interaction(self):
        nodes = self._current_interaction();
        (self._resolved).pop((len(self._resolved)) - (1));
        idx = 0;
        while ((idx) < (len(nodes))):
            node = (nodes)[idx];
            (node).success();
            idx = (idx) + (1)

    def interact(self, cmd):
        self.start_interaction();
        (cmd)(self) if callable(cmd) else (cmd).call(self);
        self.finish_interaction();

    def _getClass(self):
        return u"mdk.SessionImpl"

    def _getField(self, name):
        if ((name) == (u"_levels")):
            return SessionImpl._levels

        if ((name) == (u"_inLogging")):
            return SessionImpl._inLogging

        if ((name) == (u"_mdk")):
            return (self)._mdk

        if ((name) == (u"_resolved")):
            return (self)._resolved

        if ((name) == (u"_context")):
            return (self)._context

        if ((name) == (u"_experimental")):
            return (self)._experimental

        return None

    def _setField(self, name, value):
        if ((name) == (u"_levels")):
            SessionImpl._levels = _cast(value, lambda: _Map)

        if ((name) == (u"_inLogging")):
            SessionImpl._inLogging = _cast(value, lambda: _TLS)

        if ((name) == (u"_mdk")):
            (self)._mdk = _cast(value, lambda: MDKImpl)

        if ((name) == (u"_resolved")):
            (self)._resolved = _cast(value, lambda: _List)

        if ((name) == (u"_context")):
            (self)._context = _cast(value, lambda: mdk_protocol.SharedContext)

        if ((name) == (u"_experimental")):
            (self)._experimental = _cast(value, lambda: bool)


SessionImpl._levels = {u"CRITICAL": 0, u"ERROR": 1, u"WARN": 2, u"INFO": 3, u"DEBUG": 4}
SessionImpl._inLogging = _TLS(_TLSInit())
SessionImpl.mdk_SessionImpl_ref = None
SessionImpl.quark_List_quark_List_mdk_discovery_Node___ref = None
SessionImpl.quark_List_mdk_discovery_Node__ref = None
SessionImpl.quark_List_quark_Map_quark_String_quark_String___ref = None
SessionImpl.quark_List_quark_String__ref = None
SessionImpl.quark_Map_quark_String_quark_int__ref = None
SessionImpl.quark_Map_quark_String_quark_List_quark_Map_quark_String_quark_String____ref = None
SessionImpl.quark_Map_quark_String_quark_String__ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk")
