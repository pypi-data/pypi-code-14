# Quark 1.0.443 run at 2016-10-05 18:08:41.189562
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_discovery.protocol")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_discovery
import mdk_runtime.actors
import mdk_runtime
import mdk_protocol
import quark


class DiscoClientFactory(_QObject):
    """
    Create a Discovery service client using standard MDK env variables and
    register it with the MDK.

    """
    def _init(self):
        self.token = None

    def __init__(self, token):
        self._init()
        (self).token = token

    def create(self, subscriber, runtime):
        ddu = ((runtime).getEnvVarsService()).var(u"MDK_DISCOVERY_URL");
        url = (ddu).orElseGet(u"wss://discovery.datawire.io/ws/v1");
        return DiscoClient(subscriber, self.token, url, runtime)

    def isRegistrar(self):
        return True

    def _getClass(self):
        return u"mdk_discovery.protocol.DiscoClientFactory"

    def _getField(self, name):
        if ((name) == (u"token")):
            return (self).token

        return None

    def _setField(self, name, value):
        if ((name) == (u"token")):
            (self).token = _cast(value, lambda: unicode)


DiscoClientFactory.mdk_discovery_protocol_DiscoClientFactory_ref = None
class DiscoClient(mdk_protocol.WSClient):
    """
    A source of discovery information that talks to Datawire Discovery server.

    Also supports registering discovery information with the server.

    """
    def _init(self):
        mdk_protocol.WSClient._init(self)
        self._started = False
        self._token = None
        self._url = None
        self._failurePolicyFactory = None
        self._dispatcher = None
        self._subscriber = None
        self.registered = _Map()
        self.dlog = quark._getLogger(u"discovery")

    def __init__(self, subscriber, token, url, runtime):
        super(DiscoClient, self).__init__(runtime);
        (self)._subscriber = subscriber
        (self)._failurePolicyFactory = _cast(((runtime).dependencies).getService(u"failurepolicy_factory"), lambda: mdk_discovery.FailurePolicyFactory)
        (self)._token = token
        (self)._url = url

    def onStart(self, dispatcher):
        (self)._dispatcher = dispatcher
        (self)._started = True
        super(DiscoClient, self).onStart(dispatcher);

    def onStop(self):
        (self)._started = False
        super(DiscoClient, self).onStop();

    def onMessage(self, origin, message):
        if (((quark.reflect.Class.get(_getClass(message))).id) == (u"mdk_discovery.RegisterNode")):
            register = _cast(message, lambda: mdk_discovery.RegisterNode);
            self._register((register).node);
            return

        super(DiscoClient, self).onMessage(origin, message);

    def url(self):
        return (self)._url

    def token(self):
        return (self)._token

    def isStarted(self):
        return (self)._started

    def _register(self, node):
        """
        Register a node with the remote Discovery server.
        """
        service = (node).service;
        if (not ((service) in (self.registered))):
            (self.registered)[service] = (mdk_discovery.Cluster((self)._failurePolicyFactory));

        ((self.registered).get(service)).add(node);
        if ((self).isConnected()):
            self.active(node);

    def active(self, node):
        active = Active();
        (active).node = node
        (active).ttl = (self).ttl
        ((self).dispatcher).tell(self, (active).encode(), (self).sock);
        (self.dlog).info((u"active ") + ((node).toString()));

    def expire(self, node):
        expire = Expire();
        (expire).node = node
        ((self).dispatcher).tell(self, (expire).encode(), (self).sock);
        (self.dlog).info((u"expire ") + ((node).toString()));

    def resolve(self, node):
        pass

    def onActive(self, active):
        ((self)._dispatcher).tell(self, mdk_discovery.NodeActive((active).node), (self)._subscriber);

    def onExpire(self, expire):
        ((self)._dispatcher).tell(self, mdk_discovery.NodeExpired((expire).node), (self)._subscriber);

    def onClear(self, reset):
        pass

    def startup(self):
        self.heartbeat();

    def heartbeat(self):
        services = _List(list(((self).registered).keys()));
        idx = 0;
        while ((idx) < (len(services))):
            jdx = 0;
            nodes = (((self).registered).get((services)[idx])).nodes;
            while ((jdx) < (len(nodes))):
                self.active((nodes)[jdx]);
                jdx = (jdx) + (1)

            idx = (idx) + (1)

    def shutdown(self):
        services = _List(list(((self).registered).keys()));
        idx = 0;
        while ((idx) < (len(services))):
            jdx = 0;
            nodes = (((self).registered).get((services)[idx])).nodes;
            while ((jdx) < (len(nodes))):
                self.expire((nodes)[jdx]);
                jdx = (jdx) + (1)

            idx = (idx) + (1)

    def onWSMessage(self, message):
        event = DiscoveryEvent.decode(message);
        if ((event) == (None)):
            return

        (event).dispatch(self);

    def _getClass(self):
        return u"mdk_discovery.protocol.DiscoClient"

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

        if ((name) == (u"_started")):
            return (self)._started

        if ((name) == (u"_token")):
            return (self)._token

        if ((name) == (u"_url")):
            return (self)._url

        if ((name) == (u"_failurePolicyFactory")):
            return (self)._failurePolicyFactory

        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        if ((name) == (u"_subscriber")):
            return (self)._subscriber

        if ((name) == (u"registered")):
            return (self).registered

        if ((name) == (u"dlog")):
            return (self).dlog

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

        if ((name) == (u"_started")):
            (self)._started = _cast(value, lambda: bool)

        if ((name) == (u"_token")):
            (self)._token = _cast(value, lambda: unicode)

        if ((name) == (u"_url")):
            (self)._url = _cast(value, lambda: unicode)

        if ((name) == (u"_failurePolicyFactory")):
            (self)._failurePolicyFactory = _cast(value, lambda: mdk_discovery.FailurePolicyFactory)

        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_subscriber")):
            (self)._subscriber = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"registered")):
            (self).registered = _cast(value, lambda: _Map)

        if ((name) == (u"dlog")):
            (self).dlog = value


DiscoClient.mdk_discovery_protocol_DiscoClient_ref = None
class DiscoHandler(object):

    def onActive(self, active):
        raise NotImplementedError('`DiscoHandler.onActive` is an abstract method')

    def onExpire(self, expire):
        raise NotImplementedError('`DiscoHandler.onExpire` is an abstract method')

    def onClear(self, reset):
        raise NotImplementedError('`DiscoHandler.onClear` is an abstract method')

DiscoHandler.mdk_discovery_protocol_DiscoHandler_ref = None
class DiscoveryEvent(mdk_protocol.ProtocolEvent):
    def _init(self):
        mdk_protocol.ProtocolEvent._init(self)

    def __init__(self):
        super(DiscoveryEvent, self).__init__();

    @staticmethod
    def construct(type):
        result = mdk_protocol.ProtocolEvent.construct(type);
        if ((result) != (None)):
            return result

        if ((Active._discriminator).matches(type)):
            return Active()

        if ((Expire._discriminator).matches(type)):
            return Expire()

        if ((Clear._discriminator).matches(type)):
            return Clear()

        return _cast(None, lambda: mdk_protocol.ProtocolEvent)

    @staticmethod
    def decode(message):
        return _cast(mdk_protocol.Serializable.decodeClassName(u"mdk_discovery.protocol.DiscoveryEvent", message), lambda: mdk_protocol.ProtocolEvent)

    def dispatch(self, handler):
        self.dispatchDiscoveryEvent(_cast(handler, lambda: DiscoHandler));

    def dispatchDiscoveryEvent(self, handler):
        raise NotImplementedError('`DiscoveryEvent.dispatchDiscoveryEvent` is an abstract method')

    def _getClass(self):
        return u"mdk_discovery.protocol.DiscoveryEvent"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
DiscoveryEvent.mdk_discovery_protocol_DiscoveryEvent_ref = None
class Active(DiscoveryEvent):
    def _init(self):
        DiscoveryEvent._init(self)
        self.node = None
        self.ttl = None

    def __init__(self):
        super(Active, self).__init__();

    def dispatchDiscoveryEvent(self, handler):
        (handler).onActive(self);

    def _getClass(self):
        return u"mdk_discovery.protocol.Active"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Active._discriminator

        if ((name) == (u"node")):
            return (self).node

        if ((name) == (u"ttl")):
            return (self).ttl

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Active._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: mdk_discovery.Node)

        if ((name) == (u"ttl")):
            (self).ttl = _cast(value, lambda: float)


Active._discriminator = mdk_protocol.anyof(_List([u"active", u"discovery.protocol.Active"]))
Active.mdk_discovery_protocol_Active_ref = None
class Expire(DiscoveryEvent):
    """
    Expire a node.
    """
    def _init(self):
        DiscoveryEvent._init(self)
        self.node = None

    def __init__(self):
        super(Expire, self).__init__();

    def dispatchDiscoveryEvent(self, handler):
        (handler).onExpire(self);

    def _getClass(self):
        return u"mdk_discovery.protocol.Expire"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Expire._discriminator

        if ((name) == (u"node")):
            return (self).node

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Expire._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: mdk_discovery.Node)


Expire._discriminator = mdk_protocol.anyof(_List([u"expire", u"discovery.protocol.Expire"]))
Expire.mdk_discovery_protocol_Expire_ref = None
class Clear(DiscoveryEvent):
    """
    Expire all nodes.
    """
    def _init(self):
        DiscoveryEvent._init(self)

    def __init__(self):
        super(Clear, self).__init__();

    def dispatchDiscoveryEvent(self, handler):
        (handler).onClear(self);

    def _getClass(self):
        return u"mdk_discovery.protocol.Clear"

    def _getField(self, name):
        if ((name) == (u"_discriminator")):
            return Clear._discriminator

        return None

    def _setField(self, name, value):
        if ((name) == (u"_discriminator")):
            Clear._discriminator = _cast(value, lambda: mdk_protocol.Discriminator)


Clear._discriminator = mdk_protocol.anyof(_List([u"clear", u"discovery.protocol.Clear"]))
Clear.mdk_discovery_protocol_Clear_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_discovery.protocol")
