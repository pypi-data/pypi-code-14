# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_discovery.synapse")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_discovery
import mdk_runtime.actors
import mdk_runtime
import mdk_runtime.files


class Synapse(_QObject):
    """
    AirBnB Synapse discovery source.

    Reads Synapse-generated files (https://github.com/airbnb/synapse#file) and
    generates discovery events.

    Usage:

    m = mdk.init()
    m.registerDiscoverySource(Synapse('/path/to/synapse/files'))
    m.start()

    All resulting Node instances will have version '1.0' hardcoded, and an
    address of the form 'host:port'.

    The original object from Synpase will be attached as the Node's properties.

    """
    def _init(self):
        self._directory_path = None

    def __init__(self, directory_path):
        self._init()
        (self)._directory_path = directory_path

    def create(self, subscriber, runtime):
        return _SynapseSource(subscriber, (self)._directory_path, runtime)

    def isRegistrar(self):
        return False

    def _getClass(self):
        return u"mdk_discovery.synapse.Synapse"

    def _getField(self, name):
        if ((name) == (u"_directory_path")):
            return (self)._directory_path

        return None

    def _setField(self, name, value):
        if ((name) == (u"_directory_path")):
            (self)._directory_path = _cast(value, lambda: unicode)


Synapse.mdk_discovery_synapse_Synapse_ref = None
class _SynapseSource(_QObject):
    """
    Implementation of the Synapse discovery source.
    """
    def _init(self):
        self.subscriber = None
        self.directory_path = None
        self.files = None
        self.dispatcher = None

    def __init__(self, subscriber, directory_path, runtime):
        self._init()
        (self).subscriber = subscriber
        (self).directory_path = directory_path
        (self).files = (runtime).getFileService()

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher
        ((self).dispatcher).tell(self, mdk_runtime.files.SubscribeChanges((self).directory_path), (self).files);

    def _pathToServiceName(self, filename):
        """
        Convert '/path/to/service_name.json' to 'service_name'.
        """
        parts = (filename).split(u"/");
        service = (parts)[(len(parts)) - (1)];
        return (service)[(0):((len(service)) - (5))]

    def _update(self, service, nodes):
        """
        Send an appropriate update to the subscriber for this DiscoverySource.
        """
        ((self).dispatcher).tell(self, mdk_discovery.ReplaceCluster(service, nodes), (self).subscriber);

    def onMessage(self, origin, message):
        typeId = (quark.reflect.Class.get(_getClass(message))).id;
        service = None;
        if ((typeId) == (u"mdk_runtime.files.FileContents")):
            contents = _cast(message, lambda: mdk_runtime.files.FileContents);
            if (not (((contents).path).endswith(u".json"))):
                return

            service = (self)._pathToServiceName((contents).path)
            json = _JSONObject.parse((contents).contents);
            nodes = _List([]);
            idx = 0;
            while ((idx) < ((json).size())):
                entry = (json).getListItem(idx);
                node = mdk_discovery.Node();
                (node).service = service
                (node).version = u"1.0"
                host = ((entry).getObjectItem(u"host")).getString();
                port = _toString(int(round(((entry).getObjectItem(u"port")).getNumber())));
                (node).address = ((host) + (u":")) + (port)
                (nodes).append(node);
                idx = (idx) + (1)

            (self)._update(service, nodes);
            return

        if ((typeId) == (u"mdk_runtime.files.FileDeleted")):
            deleted = _cast(message, lambda: mdk_runtime.files.FileDeleted);
            service = (self)._pathToServiceName((deleted).path)
            (self)._update(service, _List([]));
            return

    def _getClass(self):
        return u"mdk_discovery.synapse._SynapseSource"

    def _getField(self, name):
        if ((name) == (u"subscriber")):
            return (self).subscriber

        if ((name) == (u"directory_path")):
            return (self).directory_path

        if ((name) == (u"files")):
            return (self).files

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        return None

    def _setField(self, name, value):
        if ((name) == (u"subscriber")):
            (self).subscriber = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"directory_path")):
            (self).directory_path = _cast(value, lambda: unicode)

        if ((name) == (u"files")):
            (self).files = _cast(value, lambda: mdk_runtime.files.FileActor)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass
_SynapseSource.mdk_discovery_synapse__SynapseSource_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_discovery.synapse")
