# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_discovery")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime.actors
import mdk_runtime
import quark
import mdk_runtime.promise
import mdk_util
import mdk_discovery.protocol
import mdk_discovery.synapse


class NodeActive(_QObject):
    """
    Message from DiscoverySource: a node has become active.
    """
    def _init(self):
        self.node = None

    def __init__(self, node):
        self._init()
        (self).node = node

    def _getClass(self):
        return u"mdk_discovery.NodeActive"

    def _getField(self, name):
        if ((name) == (u"node")):
            return (self).node

        return None

    def _setField(self, name, value):
        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: Node)


NodeActive.mdk_discovery_NodeActive_ref = None
class NodeExpired(_QObject):
    """
    Message from DiscoverySource: a node has expired.
    """
    def _init(self):
        self.node = None

    def __init__(self, node):
        self._init()
        (self).node = node

    def _getClass(self):
        return u"mdk_discovery.NodeExpired"

    def _getField(self, name):
        if ((name) == (u"node")):
            return (self).node

        return None

    def _setField(self, name, value):
        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: Node)


NodeExpired.mdk_discovery_NodeExpired_ref = None
class ReplaceCluster(_QObject):
    """
    Message from DiscoverySource: replace all nodes in a particular Cluster.
    """
    def _init(self):
        self.nodes = None
        self.cluster = None

    def __init__(self, cluster, nodes):
        self._init()
        (self).nodes = nodes
        (self).cluster = cluster

    def _getClass(self):
        return u"mdk_discovery.ReplaceCluster"

    def _getField(self, name):
        if ((name) == (u"nodes")):
            return (self).nodes

        if ((name) == (u"cluster")):
            return (self).cluster

        return None

    def _setField(self, name, value):
        if ((name) == (u"nodes")):
            (self).nodes = _cast(value, lambda: _List)

        if ((name) == (u"cluster")):
            (self).cluster = _cast(value, lambda: unicode)


ReplaceCluster.mdk_discovery_ReplaceCluster_ref = None
class DiscoverySource(object):
    """
    A source of discovery information.

    Sends ReplaceCluster, NodeActive and NodeExpired messages to a
    subscriber.

    """
    pass
DiscoverySource.mdk_discovery_DiscoverySource_ref = None
class DiscoverySourceFactory(object):
    """
    A factory for DiscoverySource instances.
    """

    def create(self, subscriber, runtime):
        """
        Create a new instance
        """
        raise NotImplementedError('`DiscoverySourceFactory.create` is an abstract method')

    def isRegistrar(self):
        """
        If true, the returned DiscoverySource is also a DiscoveryRegistrar.

        """
        raise NotImplementedError('`DiscoverySourceFactory.isRegistrar` is an abstract method')

DiscoverySourceFactory.mdk_discovery_DiscoverySourceFactory_ref = None
class _StaticRoutesActor(_QObject):
    """
    Discovery actor for hard-coded static routes.
    """
    def _init(self):
        self._subscriber = None
        self._knownNodes = None

    def __init__(self, subscriber, knownNodes):
        self._init()
        (self)._subscriber = subscriber
        (self)._knownNodes = knownNodes

    def onStart(self, dispatcher):
        idx = 0;
        while ((idx) < (len((self)._knownNodes))):
            (dispatcher).tell(self, NodeActive(((self)._knownNodes)[idx]), (self)._subscriber);
            idx = (idx) + (1)

    def onMessage(self, origin, message):
        pass

    def onStop(self):
        pass

    def _getClass(self):
        return u"mdk_discovery._StaticRoutesActor"

    def _getField(self, name):
        if ((name) == (u"_subscriber")):
            return (self)._subscriber

        if ((name) == (u"_knownNodes")):
            return (self)._knownNodes

        return None

    def _setField(self, name, value):
        if ((name) == (u"_subscriber")):
            (self)._subscriber = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"_knownNodes")):
            (self)._knownNodes = _cast(value, lambda: _List)


_StaticRoutesActor.mdk_discovery__StaticRoutesActor_ref = None
class StaticRoutes(_QObject):
    """
    Create a DiscoverySource with hard-coded static routes.
    """
    def _init(self):
        self._knownNodes = None

    def __init__(self, knowNodes):
        self._init()
        (self)._knownNodes = knowNodes

    @staticmethod
    def parseJSON(json_encoded):
        nodes = _List([]);
        quark.fromJSON(quark.reflect.Class.get(u"quark.List<mdk_discovery.Node>"), nodes, _JSONObject.parse(json_encoded));
        return StaticRoutes(nodes)

    def isRegistrar(self):
        return False

    def create(self, subscriber, runtime):
        return _StaticRoutesActor(subscriber, (self)._knownNodes)

    def _getClass(self):
        return u"mdk_discovery.StaticRoutes"

    def _getField(self, name):
        if ((name) == (u"_knownNodes")):
            return (self)._knownNodes

        return None

    def _setField(self, name, value):
        if ((name) == (u"_knownNodes")):
            (self)._knownNodes = _cast(value, lambda: _List)


StaticRoutes.mdk_discovery_StaticRoutes_ref = None
class RegisterNode(_QObject):
    """
    Message sent to DiscoveryRegistrar Actor to register a node.
    """
    def _init(self):
        self.node = None

    def __init__(self, node):
        self._init()
        (self).node = node

    def _getClass(self):
        return u"mdk_discovery.RegisterNode"

    def _getField(self, name):
        if ((name) == (u"node")):
            return (self).node

        return None

    def _setField(self, name, value):
        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: Node)


RegisterNode.mdk_discovery_RegisterNode_ref = None
class DiscoveryRegistrar(object):
    """
    Allow registration of services.

    Send this an actor a RegisterNode message to do so.

    """
    pass
DiscoveryRegistrar.mdk_discovery_DiscoveryRegistrar_ref = None
class _Request(_QObject):
    def _init(self):
        self.version = None
        self.factory = None

    def __init__(self, version, factory):
        self._init()
        (self).version = version
        (self).factory = factory

    def _getClass(self):
        return u"mdk_discovery._Request"

    def _getField(self, name):
        if ((name) == (u"version")):
            return (self).version

        if ((name) == (u"factory")):
            return (self).factory

        return None

    def _setField(self, name, value):
        if ((name) == (u"version")):
            (self).version = _cast(value, lambda: unicode)

        if ((name) == (u"factory")):
            (self).factory = _cast(value, lambda: mdk_runtime.promise.PromiseResolver)


_Request.mdk_discovery__Request_ref = None
class FailurePolicy(object):
    """
    A policy for choosing how to deal with failures.
    """

    def success(self):
        """
        Record a success for the Node this policy is managing.
        """
        raise NotImplementedError('`FailurePolicy.success` is an abstract method')

    def failure(self):
        """
        Record a failure for the Node this policy is managing.
        """
        raise NotImplementedError('`FailurePolicy.failure` is an abstract method')

    def available(self):
        """
        Return whether the Node should be accessed.
        """
        raise NotImplementedError('`FailurePolicy.available` is an abstract method')

FailurePolicy.mdk_discovery_FailurePolicy_ref = None
class FailurePolicyFactory(_QObject):
    """
    A factory for FailurePolicy.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def create(self):
        """
        Create a new FailurePolicy.
        """
        raise NotImplementedError('`FailurePolicyFactory.create` is an abstract method')

    def _getClass(self):
        return u"mdk_discovery.FailurePolicyFactory"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
FailurePolicyFactory.mdk_discovery_FailurePolicyFactory_ref = None
class CircuitBreaker(_QObject):
    """
    Default circuit breaker policy.
    """
    def _init(self):
        self._log = quark._getLogger(u"mdk.breaker")
        self._threshold = None
        self._delay = None
        self._time = None
        self._mutex = _Lock()
        self._failed = False
        self._failures = 0
        self._lastFailure = 0.0

    def __init__(self, time, threshold, retestDelay):
        self._init()
        self._threshold = threshold
        self._delay = retestDelay
        self._time = time

    def success(self):
        (self._mutex).acquire();
        self._failed = False
        self._failures = 0
        self._lastFailure = 0.0
        (self._mutex).release();

    def failure(self):
        (self._mutex).acquire();
        self._failures = (self._failures) + (1)
        self._lastFailure = (self._time).time()
        if (((self._threshold) != (0)) and ((self._failures) >= (self._threshold))):
            (self._log).info(u"BREAKER TRIPPED.");
            self._failed = True

        (self._mutex).release();

    def available(self):
        if (self._failed):
            (self._mutex).acquire();
            result = (((self._time).time()) - (self._lastFailure)) > (self._delay);
            (self._mutex).release();
            if (result):
                (self._log).info(u"BREAKER RETEST.");

            return result
        else:
            return True

    def _getClass(self):
        return u"mdk_discovery.CircuitBreaker"

    def _getField(self, name):
        if ((name) == (u"_log")):
            return (self)._log

        if ((name) == (u"_threshold")):
            return (self)._threshold

        if ((name) == (u"_delay")):
            return (self)._delay

        if ((name) == (u"_time")):
            return (self)._time

        if ((name) == (u"_mutex")):
            return (self)._mutex

        if ((name) == (u"_failed")):
            return (self)._failed

        if ((name) == (u"_failures")):
            return (self)._failures

        if ((name) == (u"_lastFailure")):
            return (self)._lastFailure

        return None

    def _setField(self, name, value):
        if ((name) == (u"_log")):
            (self)._log = value

        if ((name) == (u"_threshold")):
            (self)._threshold = _cast(value, lambda: int)

        if ((name) == (u"_delay")):
            (self)._delay = _cast(value, lambda: float)

        if ((name) == (u"_time")):
            (self)._time = _cast(value, lambda: mdk_runtime.Time)

        if ((name) == (u"_mutex")):
            (self)._mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"_failed")):
            (self)._failed = _cast(value, lambda: bool)

        if ((name) == (u"_failures")):
            (self)._failures = _cast(value, lambda: int)

        if ((name) == (u"_lastFailure")):
            (self)._lastFailure = _cast(value, lambda: float)


CircuitBreaker.mdk_discovery_CircuitBreaker_ref = None
class CircuitBreakerFactory(FailurePolicyFactory):
    """
    Create CircuitBreaker instances.
    """
    def _init(self):
        FailurePolicyFactory._init(self)
        self.threshold = 3
        self.retestDelay = 30.0
        self.time = None

    def __init__(self, runtime):
        super(CircuitBreakerFactory, self).__init__();
        (self).time = (runtime).getTimeService()

    def create(self):
        return CircuitBreaker(self.time, self.threshold, self.retestDelay)

    def _getClass(self):
        return u"mdk_discovery.CircuitBreakerFactory"

    def _getField(self, name):
        if ((name) == (u"threshold")):
            return (self).threshold

        if ((name) == (u"retestDelay")):
            return (self).retestDelay

        if ((name) == (u"time")):
            return (self).time

        return None

    def _setField(self, name, value):
        if ((name) == (u"threshold")):
            (self).threshold = _cast(value, lambda: int)

        if ((name) == (u"retestDelay")):
            (self).retestDelay = _cast(value, lambda: float)

        if ((name) == (u"time")):
            (self).time = _cast(value, lambda: mdk_runtime.Time)


CircuitBreakerFactory.mdk_discovery_CircuitBreakerFactory_ref = None
class RecordingFailurePolicy(_QObject):
    """
    FailurePolicy that records failures and successes.
    """
    def _init(self):
        self.successes = 0
        self.failures = 0

    def __init__(self): self._init()

    def success(self):
        (self).successes = ((self).successes) + (1)

    def failure(self):
        (self).failures = ((self).failures) + (1)

    def available(self):
        return True

    def _getClass(self):
        return u"mdk_discovery.RecordingFailurePolicy"

    def _getField(self, name):
        if ((name) == (u"successes")):
            return (self).successes

        if ((name) == (u"failures")):
            return (self).failures

        return None

    def _setField(self, name, value):
        if ((name) == (u"successes")):
            (self).successes = _cast(value, lambda: int)

        if ((name) == (u"failures")):
            (self).failures = _cast(value, lambda: int)


RecordingFailurePolicy.mdk_discovery_RecordingFailurePolicy_ref = None
class RecordingFailurePolicyFactory(FailurePolicyFactory):
    """
    Factory for FailurePolicy useful for testing.
    """
    def _init(self):
        FailurePolicyFactory._init(self)

    def __init__(self):
        super(RecordingFailurePolicyFactory, self).__init__();

    def create(self):
        return RecordingFailurePolicy()

    def _getClass(self):
        return u"mdk_discovery.RecordingFailurePolicyFactory"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
RecordingFailurePolicyFactory.mdk_discovery_RecordingFailurePolicyFactory_ref = None
class Cluster(_QObject):
    """
    A Cluster is a group of providers of (possibly different versions of)
    a single service. Each service provider is represented by a Node.
    """
    def _init(self):
        self.nodes = _List([])
        self._waiting = _List([])
        self._failurepolicies = {}
        self._counter = 0
        self._fpfactory = None

    def __init__(self, fpfactory):
        self._init()
        (self)._fpfactory = fpfactory

    def choose(self):
        """
        Choose a single Node to talk to. At present this is a simple round
        robin.
        """
        return self.chooseVersion(None)

    def _copyNode(self, node):
        """
        Create a Node for external use.
        """
        result = Node();
        (result).address = (node).address
        (result).version = (node).version
        (result).service = (node).service
        (result).properties = (node).properties
        (result)._policy = (self).failurePolicy(node)
        return result

    def failurePolicy(self, node):
        """
        Get the FailurePolicy for a Node.
        """
        return ((self)._failurepolicies).get((node).address)

    def chooseVersion(self, version):
        """
        Choose a compatible version of a service to talk to.
        """
        if ((len(self.nodes)) == (0)):
            return _cast(None, lambda: Node)

        start = (self._counter) % (len(self.nodes));
        self._counter = (self._counter) + (1)
        count = 0;
        while ((count) < (len(self.nodes))):
            choice = ((start) + (count)) % (len(self.nodes));
            candidate = (self.nodes)[choice];
            policy = ((self)._failurepolicies).get((candidate).address);
            if ((mdk_util.versionMatch(version, (candidate).version)) and ((policy).available())):
                return (self)._copyNode(candidate)

            count = (count) + (1)

        return _cast(None, lambda: Node)

    def add(self, node):
        """
        Add a Node to the cluster (or, if it's already present in the cluster,
        update its properties).  At present, this involves a linear search, so
        very large Clusters are unlikely to perform well.
        """
        if (not (((node).address) in (self._failurepolicies))):
            (self._failurepolicies)[(node).address] = (((self)._fpfactory).create());

        if ((len((self)._waiting)) > (0)):
            waiting = (self)._waiting;
            (self)._waiting = _List([])
            jdx = 0;
            while ((jdx) < (len(waiting))):
                req = (waiting)[jdx];
                if (mdk_util.versionMatch((req).version, (node).version)):
                    ((req).factory).resolve((self)._copyNode(node));
                else:
                    ((self)._waiting).append(req);

                jdx = (jdx) + (1)

        idx = 0;
        while ((idx) < (len(self.nodes))):
            if ((((self.nodes)[idx]).address) == ((node).address)):
                (self.nodes)[idx] = (node);
                return

            idx = (idx) + (1)

        (self.nodes).append(node);

    def _addRequest(self, version, factory):
        (self._waiting).append(_Request(version, factory));

    def remove(self, node):
        """
        Remove a Node from the cluster, if it's present. If it's not present, do
        nothing. Note that it is possible to remove all the Nodes and be left with
        an empty cluster.
        """
        idx = 0;
        while ((idx) < (len(self.nodes))):
            ep = (self.nodes)[idx];
            if ((((ep).address) == (None)) or (((ep).address) == ((node).address))):
                (self.nodes).pop(idx);
                return

            idx = (idx) + (1)

    def isEmpty(self):
        """
        Returns true if and only if this Cluster contains no Nodes.
        """
        return (len(self.nodes)) <= (0)

    def toString(self):
        """
        Return a string representation of the Cluster.

        WARNING: every Node is represented in the string. Large Clusters will
        produce unusably large strings.
        """
        result = u"Cluster(";
        idx = 0;
        while ((idx) < (len(self.nodes))):
            if ((idx) > (0)):
                result = (result) + (u", ")

            result = (result) + (((self.nodes)[idx]).toString())
            idx = (idx) + (1)

        result = (result) + (u")")
        return result

    def _getClass(self):
        return u"mdk_discovery.Cluster"

    def _getField(self, name):
        if ((name) == (u"nodes")):
            return (self).nodes

        if ((name) == (u"_waiting")):
            return (self)._waiting

        if ((name) == (u"_failurepolicies")):
            return (self)._failurepolicies

        if ((name) == (u"_counter")):
            return (self)._counter

        if ((name) == (u"_fpfactory")):
            return (self)._fpfactory

        return None

    def _setField(self, name, value):
        if ((name) == (u"nodes")):
            (self).nodes = _cast(value, lambda: _List)

        if ((name) == (u"_waiting")):
            (self)._waiting = _cast(value, lambda: _List)

        if ((name) == (u"_failurepolicies")):
            (self)._failurepolicies = _cast(value, lambda: _Map)

        if ((name) == (u"_counter")):
            (self)._counter = _cast(value, lambda: int)

        if ((name) == (u"_fpfactory")):
            (self)._fpfactory = _cast(value, lambda: FailurePolicyFactory)


Cluster.quark_List_mdk_discovery__Request__ref = None
Cluster.quark_Map_quark_String_mdk_discovery_FailurePolicy__ref = None
Cluster.mdk_discovery_Cluster_ref = None
class Node(_QObject):
    """
    The Node class captures address and metadata information about a
    server functioning as a service instance.
    """
    def _init(self):
        self.service = None
        self.version = None
        self.address = None
        self.properties = {}
        self._policy = None

    def __init__(self): self._init()

    def success(self):
        (self._policy).success();

    def failure(self):
        (self._policy).failure();

    def available(self):
        return (self._policy).available()

    def toString(self):
        """
        Return a string representation of the Node.
        """
        result = u"Node(";
        if ((self.service) == (None)):
            result = (result) + (u"<unnamed>")
        else:
            result = (result) + (self.service)

        result = (result) + (u": ")
        if ((self.address) == (None)):
            result = (result) + (u"<unlocated>")
        else:
            result = (result) + (self.address)

        if ((self.version) != (None)):
            result = ((result) + (u", ")) + (self.version)

        result = (result) + (u")")
        if ((self.properties) != (None)):
            result = ((result) + (u" ")) + (_toString(self.properties))

        return result

    def _getClass(self):
        return u"mdk_discovery.Node"

    def _getField(self, name):
        if ((name) == (u"service")):
            return (self).service

        if ((name) == (u"version")):
            return (self).version

        if ((name) == (u"address")):
            return (self).address

        if ((name) == (u"properties")):
            return (self).properties

        if ((name) == (u"_policy")):
            return (self)._policy

        return None

    def _setField(self, name, value):
        if ((name) == (u"service")):
            (self).service = _cast(value, lambda: unicode)

        if ((name) == (u"version")):
            (self).version = _cast(value, lambda: unicode)

        if ((name) == (u"address")):
            (self).address = _cast(value, lambda: unicode)

        if ((name) == (u"properties")):
            (self).properties = _cast(value, lambda: _Map)

        if ((name) == (u"_policy")):
            (self)._policy = _cast(value, lambda: FailurePolicy)


Node.mdk_discovery_Node_ref = None
class Discovery(_QObject):
    """
    The Discovery class functions as a conduit to a source of discovery information.
    Using it, a provider can register itself as providing a particular service
    (see the register method) and a consumer can locate a provider for a
    particular service (see the resolve method).
    """
    def _init(self):
        self.logger = quark._getLogger(u"discovery")
        self.services = _Map()
        self.started = False
        self.mutex = _Lock()
        self.runtime = None
        self._fpfactory = None

    def __init__(self, runtime):
        self._init()
        (self.logger).info(u"Discovery created!");
        (self).runtime = runtime
        (self)._fpfactory = _cast(((runtime).dependencies).getService(u"failurepolicy_factory"), lambda: FailurePolicyFactory)

    def _lock(self):
        """
        Lock.
        """
        (self.mutex).acquire();

    def _release(self):
        (self.mutex).release();

    def onStart(self, dispatcher):
        """
        Start the uplink to the discovery service.
        """
        (self)._lock();
        if (not (self.started)):
            self.started = True

        (self)._release();

    def onStop(self):
        """
        Stop the uplink to the discovery service.
        """
        (self)._lock();
        if (self.started):
            self.started = False

        (self)._release();

    def register(self, node):
        """
        Register info about a service node with a discovery source of truth. You must
        usually start the uplink before this will do much; see start().
        """
        registrar = None;
        if (((self.runtime).dependencies).hasService(u"discovery_registrar")):
            registrar = _cast(((self.runtime).dependencies).getService(u"discovery_registrar"), lambda: DiscoveryRegistrar)
        else:
            raise Exception(u"Registration not supported as no Discovery Registrar was setup.");

        (((self).runtime).dispatcher).tell(self, RegisterNode(node), registrar);
        return self

    def register_service(self, service, address, version):
        """
        Register info about a service node with the discovery service. You must
        usually start the uplink before this will do much; see start().
        """
        node = Node();
        (node).service = service
        (node).address = address
        (node).version = version
        return (self).register(node)

    def knownNodes(self, service):
        """
        Return the current known Nodes for a service, if any.
        """
        if (not ((service) in (self.services))):
            return _List([])

        return ((self.services).get(service)).nodes

    def failurePolicy(self, node):
        """
        Get the FailurePolicy for a Node.
        """
        return ((self.services).get((node).service)).failurePolicy(node)

    def _resolve(self, service, version):
        """
        Resolve a service name into an available service node. You must
        usually start the uplink before this will do much; see start().
        The returned Promise will end up with a Node as its value.
        """
        factory = mdk_runtime.promise.PromiseResolver((self.runtime).dispatcher);
        (self)._lock();
        if (not ((service) in (self.services))):
            (self.services)[service] = (Cluster((self)._fpfactory));

        result = ((self.services).get(service)).chooseVersion(version);
        if ((result) == (None)):
            ((self.services).get(service))._addRequest(version, factory);
            (self)._release();
        else:
            (self)._release();
            (factory).resolve(result);

        return (factory).promise

    def resolve(self, service, version):
        """
        Resolve a service; return a (Bluebird) Promise on Javascript. Does not work elsewhere.
        """
        return mdk_util.toNativePromise(self._resolve(service, version))

    def resolve_until(self, service, version, timeout):
        """
        Wait for service name to resolve into an available service node, or fail
        appropriately (typically by raising an exception if the language
        supports it). This should only be used in blocking runtimes (e.g.
        you do not want to use this in Javascript).
        """
        return _cast(mdk_util.WaitForPromise.wait((self)._resolve(service, version), timeout, (u"service ") + (service)), lambda: Node)

    def onMessage(self, origin, message):
        klass = (quark.reflect.Class.get(_getClass(message))).id;
        if ((klass) == (u"mdk_discovery.NodeActive")):
            active = _cast(message, lambda: NodeActive);
            (self)._active((active).node);
            return

        if ((klass) == (u"mdk_discovery.NodeExpired")):
            expire = _cast(message, lambda: NodeExpired);
            (self)._expire((expire).node);
            return

        if ((klass) == (u"mdk_discovery.ReplaceCluster")):
            replace = _cast(message, lambda: ReplaceCluster);
            (self)._replace((replace).cluster, (replace).nodes);
            return

    def _replace(self, service, nodes):
        (self)._lock();
        (self.logger).info((((u"replacing all nodes for ") + (service)) + (u" with ")) + (_toString(nodes)));
        if (not ((service) in (self.services))):
            (self.services)[service] = (Cluster((self)._fpfactory));

        cluster = (self.services).get(service);
        currentNodes = (quark.ListUtil()).slice((cluster).nodes, 0, len((cluster).nodes));
        idx = 0;
        while ((idx) < (len(currentNodes))):
            (cluster).remove((currentNodes)[idx]);
            idx = (idx) + (1)

        idx = 0
        while ((idx) < (len(nodes))):
            (cluster).add((nodes)[idx]);
            idx = (idx) + (1)

        (self)._release();

    def _active(self, node):
        (self)._lock();
        service = (node).service;
        (self.logger).info((u"adding ") + ((node).toString()));
        if (not ((service) in (self.services))):
            (self.services)[service] = (Cluster((self)._fpfactory));

        cluster = (self.services).get(service);
        (cluster).add(node);
        (self)._release();

    def _expire(self, node):
        (self)._lock();
        service = (node).service;
        if ((service) in (self.services)):
            cluster = (self.services).get(service);
            (self.logger).info(((u"removing ") + ((node).toString())) + (u" from cluster"));
            (cluster).remove(node);

        (self)._release();

    def _getClass(self):
        return u"mdk_discovery.Discovery"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"services")):
            return (self).services

        if ((name) == (u"started")):
            return (self).started

        if ((name) == (u"mutex")):
            return (self).mutex

        if ((name) == (u"runtime")):
            return (self).runtime

        if ((name) == (u"_fpfactory")):
            return (self)._fpfactory

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"services")):
            (self).services = _cast(value, lambda: _Map)

        if ((name) == (u"started")):
            (self).started = _cast(value, lambda: bool)

        if ((name) == (u"mutex")):
            (self).mutex = _cast(value, lambda: _Lock)

        if ((name) == (u"runtime")):
            (self).runtime = _cast(value, lambda: mdk_runtime.MDKRuntime)

        if ((name) == (u"_fpfactory")):
            (self)._fpfactory = _cast(value, lambda: FailurePolicyFactory)


Discovery.quark_ListUtil_mdk_discovery_Node__ref = None
Discovery.quark_Map_quark_String_mdk_discovery_Cluster__ref = None
Discovery.mdk_discovery_Discovery_ref = None



def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_discovery")
