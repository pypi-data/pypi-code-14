# Quark 1.0.452 run at 2016-10-27 16:23:20.395751
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_metrics")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_protocol
import quark.concurrent
import mdk_discovery
import mdk_runtime.actors


class InteractionEvent(mdk_protocol.Serializable):
    """
    Wire protocol message for reporting interaction results to MCP.
    """
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.timestamp = None
        self.uuid = (quark.concurrent.Context.runtime()).uuid()
        self.session = None
        self.node = None
        self.results = {}

    def __init__(self):
        super(InteractionEvent, self).__init__();

    def getTimestamp(self):
        return (self).timestamp

    def addNode(self, destination, success):
        """
        Add the result of communicating with a specific node.
        """
        value = 0;
        if (success):
            value = 1

        ((self).results)[_cast(((destination).properties).get(u"datawire_nodeId"), lambda: unicode)] = (value);

    def _getClass(self):
        return u"mdk_metrics.InteractionEvent"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return InteractionEvent._json_type

        if ((name) == (u"timestamp")):
            return (self).timestamp

        if ((name) == (u"uuid")):
            return (self).uuid

        if ((name) == (u"session")):
            return (self).session

        if ((name) == (u"node")):
            return (self).node

        if ((name) == (u"results")):
            return (self).results

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            InteractionEvent._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"timestamp")):
            (self).timestamp = _cast(value, lambda: int)

        if ((name) == (u"uuid")):
            (self).uuid = _cast(value, lambda: unicode)

        if ((name) == (u"session")):
            (self).session = _cast(value, lambda: unicode)

        if ((name) == (u"node")):
            (self).node = _cast(value, lambda: unicode)

        if ((name) == (u"results")):
            (self).results = _cast(value, lambda: _Map)


InteractionEvent._json_type = u"interaction_event"
InteractionEvent.mdk_metrics_InteractionEvent_ref = None
class InteractionAck(mdk_protocol.Serializable):
    """
    Wire protocol message for MCP to acknowledge InteractionEvent receipt.
    """
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.sequence = None

    def __init__(self):
        super(InteractionAck, self).__init__();

    def _getClass(self):
        return u"mdk_metrics.InteractionAck"

    def _getField(self, name):
        if ((name) == (u"_json_type")):
            return InteractionAck._json_type

        if ((name) == (u"sequence")):
            return (self).sequence

        return None

    def _setField(self, name, value):
        if ((name) == (u"_json_type")):
            InteractionAck._json_type = _cast(value, lambda: unicode)

        if ((name) == (u"sequence")):
            (self).sequence = _cast(value, lambda: int)


InteractionAck._json_type = u"interaction_ack"
InteractionAck.mdk_metrics_InteractionAck_ref = None
class MetricsClient(_QObject):
    """
    Mini-protocol for sending metrics to MCP.
    """
    def _init(self):
        self._dispatcher = None
        self._sock = None
        self._sendWithAcks = mdk_protocol.SendWithAcks()

    def __init__(self, wsclient):
        self._init()
        (wsclient).subscribe(self);

    def sendInteraction(self, evt):
        """
        Queue info about interaction to be sent to the MCP.
        """
        ((self)._sendWithAcks).send(InteractionEvent._json_type, evt);

    def onStart(self, dispatcher):
        (self)._dispatcher = dispatcher

    def onStop(self):
        pass

    def onMessage(self, origin, message):
        mdk_protocol._subscriberDispatch(self, message);

    def onWSConnected(self, websock):
        (self)._sock = websock
        ((self)._sendWithAcks).onConnected(self, (self)._dispatcher, websock);

    def onPump(self):
        ((self)._sendWithAcks).onPump(self, (self)._dispatcher, (self)._sock);

    def onMessageFromServer(self, message):
        type = (quark.reflect.Class.get(_getClass(message))).id;
        if ((type) == (u"metrics.InteractionAck")):
            ack = _cast(message, lambda: InteractionAck);
            ((self)._sendWithAcks).onAck((ack).sequence);
            return

    def _getClass(self):
        return u"mdk_metrics.MetricsClient"

    def _getField(self, name):
        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        if ((name) == (u"_sock")):
            return (self)._sock

        if ((name) == (u"_sendWithAcks")):
            return (self)._sendWithAcks

        return None

    def _setField(self, name, value):
        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"_sock")):
            (self)._sock = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"_sendWithAcks")):
            (self)._sendWithAcks = _cast(value, lambda: mdk_protocol.SendWithAcks)


MetricsClient.mdk_metrics_MetricsClient_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_metrics")
