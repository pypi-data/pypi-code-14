# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
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
import mdk_protocol
import mdk_runtime.actors
import mdk_runtime
import quark


class DiscoClientFactory(_QObject):
    """
    Create a Discovery service client using standard MDK env variables and
    register it with the MDK.

    """
    def _init(self):
        self.wsclient = None

    def __init__(self, wsclient):
        self._init()
        (self).wsclient = wsclient

    def create(self, subscriber, runtime):
        return DiscoClient(subscriber, self.wsclient, runtime)

    def isRegistrar(self):
        return True

    def _getClass(self):
        return u"mdk_discovery.protocol.DiscoClientFactory"

    def _getField(self, name):
        if ((name) == (u"wsclient")):
            return (self).wsclient

        return None

    def _setField(self, name, value):
        if ((name) == (u"wsclient")):
            (self).wsclient = _cast(value, lambda: mdk_protocol.WSClient)


DiscoClientFactory.mdk_discovery_protocol_DiscoClientFactory_ref = None
class DiscoClient(_QObject):
    """
    A source of discovery information that talks to Datawire Discovery server.

    Also supports registering discovery information with the server.

    """
    def _init(self):
        self._failurePolicyFactory = None
        self._dispatcher = None
        self._timeService = None
        self._subscriber = None
        self._wsclient = None
        self.registered = _Map()
        self.dlog = quark._getLogger(u"discovery")
        self.lastHeartbeat = 0
        self.sock = None

    def __init__(self, disco_subscriber, wsclient, runtime):
        self._init()
        (self)._subscriber = disco_subscriber
        (self)._wsclient = wsclient
        ((self)._wsclient).subscribe(self);
        (self)._failurePolicyFactory = _cast(((runtime).dependencies).getService(u"failurepolicy_factory"), lambda: mdk_discovery.FailurePolicyFactory)
        (self)._timeService = (runtime).getTimeService()

    def onStart(self, dispatcher):
        (self)._dispatcher = dispatcher

    def onStop(self):
        self.shutdown();

    def onMessage(self, origin, message):
        klass = (quark.reflect.Class.get(_getClass(message))).id;
        if ((klass) == (u"mdk_discovery.RegisterNode")):
            register = _cast(message, lambda: mdk_discovery.RegisterNode);
            self._register((register).node);
            return

        mdk_protocol._subscriberDispatch(self, message);

    def onMessageFromServer(self, message):
        type = (quark.reflect.Class.get(_getClass(message))).id;
        if ((type) == (u"mdk_discovery.protocol.Active")):
            active = _cast(message, lambda: Active);
            self.onActive(active);
            return

        if ((type) == (u"mdk_discovery.protocol.Expire")):
            expire = _cast(message, lambda: Expire);
            (self).onExpire(expire);
            return

    def onWSConnected(self, websocket):
        (self).sock = websocket
        self.heartbeat();

    def onPump(self):
        rightNow = int(round((((self)._timeService).time()) * (1000.0)));
        heartbeatInterval = int(round((float(((self)._wsclient).ttl) / float(2.0)) * (1000.0)));
        if (((rightNow) - ((self).lastHeartbeat)) >= (heartbeatInterval)):
            (self).lastHeartbeat = rightNow
            self.heartbeat();

    def _register(self, node):
        """
        Register a node with the remote Discovery server.
        """
        service = (node).service;
        if (not ((service) in (self.registered))):
            (self.registered)[service] = (mdk_discovery.Cluster((self)._failurePolicyFactory));

        ((self.registered).get(service)).add(node);
        if (((self)._wsclient).isConnected()):
            self.active(node);

    def active(self, node):
        active = Active();
        (active).node = node
        (active).ttl = ((self)._wsclient).ttl
        ((self)._dispatcher).tell(self, (active).encode(), (self).sock);
        (self.dlog).info((u"active ") + ((node).toString()));

    def expire(self, node):
        expire = Expire();
        (expire).node = node
        ((self)._dispatcher).tell(self, (expire).encode(), (self).sock);
        (self.dlog).info((u"expire ") + ((node).toString()));

    def resolve(self, node):
        pass

    def onActive(self, active):
        ((self)._dispatcher).tell(self, mdk_discovery.NodeActive((active).node), (self)._subscriber);

    def onExpire(self, expire):
        ((self)._dispatcher).tell(self, mdk_discovery.NodeExpired((expire).node), (self)._subscriber);

    def heartbeat(self):
        """
        Send all registered services.
        """
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

    def _getClass(self):
        return u"mdk_discovery.protocol.DiscoClient"

    def _getField(self, name):
        if ((name) == (u"_failurePolicyFactory")):
            return (self)._failurePolicyFactory

        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        if ((name) == (u"_timeService")):
            return (self)._timeService

        if ((name) == (u"_subscriber")):
            return (self)._subscriber

        if ((name) == (u"_wsclient")):
            return (self)._wsclient

        if ((name) == (u"registered")):
            return (self).registered

        if ((name) == (u"dlog")):
            return (self).dlog

        if ((name) == (u"lastHeartbeat")):
            return (self).lastHeartbeat

        if ((name) == (u"sock")):
            return (self).sock

        return None

    def _setField(self, name, value):
        if ((name) == (u"_failurePolicyFactory")):
            (self)._failurePolicyFactory = _cast(value, lambda: mdk_discovery.FailurePolicyFactory)

        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_timeService")):
            (self)._timeService = _cast(value, lambda: mdk_runtime.Time)

        if ((name) == (u"_subscriber")):
            (self)._subscriber = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"_wsclient")):
            (self)._wsclient = _cast(value, lambda: mdk_protocol.WSClient)

        if ((name) == (u"registered")):
            (self).registered = _cast(value, lambda: _Map)

        if ((name) == (u"dlog")):
            (self).dlog = value

        if ((name) == (u"lastHeartbeat")):
            (self).lastHeartbeat = _cast(value, lambda: int)

        if ((name) == (u"sock")):
            (self).sock = _cast(value, lambda: mdk_runtime.actors.Actor)


DiscoClient.mdk_discovery_protocol_DiscoClient_ref = None
class Active(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.node = None
        self.ttl = None

    def __init__(self):
        super(Active, self).__init__();

    def _getClass(self):
        return u"mdk_discovery.protocol.Active"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Active._json_type

        if ((name) == (u"node")):
            return (self).node

        if ((name) == (u"ttl")):
            return (self).ttl

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Active._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: mdk_discovery.Node)

        if ((name) == (u"ttl")):
            (self).ttl = _cast(value, lambda: float)


Active._json_type = u"active"
Active.mdk_discovery_protocol_Active_ref = None
class Expire(mdk_protocol.Serializable):
    """
    Expire a node.
    """
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.node = None

    def __init__(self):
        super(Expire, self).__init__();

    def _getClass(self):
        return u"mdk_discovery.protocol.Expire"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Expire._json_type

        if ((name) == (u"node")):
            return (self).node

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Expire._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: mdk_discovery.Node)


Expire._json_type = u"expire"
Expire.mdk_discovery_protocol_Expire_ref = None
class Clear(mdk_protocol.Serializable):
    """
    Expire all nodes.
    """
    def _init(self):
        mdk_protocol.Serializable._init(self)

    def __init__(self):
        super(Clear, self).__init__();

    def _getClass(self):
        return u"mdk_discovery.protocol.Clear"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return Clear._json_type

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            Clear._json_type = _cast(value, lambda: unicode)


Clear._json_type = u"clear"
Clear.mdk_discovery_protocol_Clear_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_discovery.protocol")
