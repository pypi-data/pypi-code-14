# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_runtime.actors")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.concurrent


class Actor(object):
    """
    A store of some state. Emits events and handles events.
    """

    def onStart(self, dispatcher):
        """
        The Actor should start operating.
        """
        raise NotImplementedError('`Actor.onStart` is an abstract method')

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass

    def onMessage(self, origin, message):
        """
        Called on incoming one-way message from another actor sent via tell().
        """
        raise NotImplementedError('`Actor.onMessage` is an abstract method')

Actor.mdk_runtime_actors_Actor_ref = None
class _QueuedMessage(object):
    """
    A message that can be queued for delivery in a MessageDispatcher.
    """

    def deliver(self):
        raise NotImplementedError('`_QueuedMessage.deliver` is an abstract method')

_QueuedMessage.mdk_runtime_actors__QueuedMessage_ref = None
class _InFlightMessage(_QObject):
    """
    A message that queued for delivery by a MessageDispatcher.
    """
    def _init(self):
        self.origin = None
        self.msg = None
        self.destination = None

    def __init__(self, origin, msg, destination):
        self._init()
        (self).origin = origin
        (self).msg = msg
        (self).destination = destination

    def deliver(self):
        """
        Deliver the message.
        """
        ((self).destination).onMessage((self).origin, (self).msg);

    def toString(self):
        return ((((((u"{") + (_toString(self.origin))) + (u"->")) + (_toString(self.destination))) + (u": ")) + (_toString(self.msg))) + (u"}")

    def _getClass(self):
        return u"mdk_runtime.actors._InFlightMessage"

    def _getField(self, name):
        if ((name) == (u"origin")):
            return (self).origin

        if ((name) == (u"msg")):
            return (self).msg

        if ((name) == (u"destination")):
            return (self).destination

        return None

    def _setField(self, name, value):
        if ((name) == (u"origin")):
            (self).origin = _cast(value, lambda: Actor)

        if ((name) == (u"msg")):
            (self).msg = value

        if ((name) == (u"destination")):
            (self).destination = _cast(value, lambda: Actor)


_InFlightMessage.mdk_runtime_actors__InFlightMessage_ref = None
class _StartStopActor(_QObject):
    """
    Start or stop an Actor.
    """
    def _init(self):
        self.actor = None
        self.dispatcher = None
        self.start = None

    def __init__(self, actor, dispatcher, start):
        self._init()
        (self).actor = actor
        (self).dispatcher = dispatcher
        (self).start = start

    def toString(self):
        result = u"stopping";
        if ((self).start):
            result = u"starting"

        return ((result) + (u" ")) + (_toString((self).actor))

    def deliver(self):
        if ((self).start):
            ((self).actor).onStart((self).dispatcher);
        else:
            ((self).actor).onStop();

    def _getClass(self):
        return u"mdk_runtime.actors._StartStopActor"

    def _getField(self, name):
        if ((name) == (u"actor")):
            return (self).actor

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"start")):
            return (self).start

        return None

    def _setField(self, name, value):
        if ((name) == (u"actor")):
            (self).actor = _cast(value, lambda: Actor)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: MessageDispatcher)

        if ((name) == (u"start")):
            (self).start = _cast(value, lambda: bool)


_StartStopActor.mdk_runtime_actors__StartStopActor_ref = None
class MessageDispatcher(_QObject):
    """
    Manage a group of related Actors.

    Each Actor should only be started and used by one MessageDispatcher.

    Reduce accidental re-entrancy by making sure messages are run asynchronously.

    """
    def _init(self):
        self.logger = quark._getLogger(u"actors")
        self._queued = _List([])
        self._delivering = False
        self._lock = _Lock()

    def __init__(self): self._init()

    def tell(self, origin, message, destination):
        """
        Queue a message from origin to destination, and trigger delivery if necessary.
        """
        inFlight = _InFlightMessage(origin, message, destination);
        (self)._queue(inFlight);

    def startActor(self, actor):
        """
        Start an Actor.
        """
        (self)._queue(_StartStopActor(actor, self, True));

    def stopActor(self, actor):
        """
        Stop an Actor.
        """
        (self)._queue(_StartStopActor(actor, self, False));

    def _callQueuedMessage(self, ignore, message):
        (message).deliver();
        return True

    def _queue(self, inFlight):
        """
        Queue a message for delivery.
        """
        (self.logger).debug((u"Queued ") + (_toString(inFlight)));
        ((self)._lock).acquire();
        ((self)._queued).append(inFlight);
        if ((self)._delivering):
            ((self)._lock).release();
            return

        (self)._delivering = True
        while ((len((self)._queued)) > (0)):
            toDeliver = (self)._queued;
            (self)._queued = _List([])
            ((self)._lock).release();
            idx = 0;
            while ((idx) < (len(toDeliver))):
                (self.logger).debug((u"Delivering ") + (_toString((toDeliver)[idx])));
                deliver = quark._BoundMethod(self, u"_callQueuedMessage", _List([(toDeliver)[idx]]));
                (quark.concurrent.Context.runtime()).callSafely(deliver, False);
                idx = (idx) + (1)

            ((self)._lock).acquire();

        (self)._delivering = False
        ((self)._lock).release();

    def _getClass(self):
        return u"mdk_runtime.actors.MessageDispatcher"

    def _getField(self, name):
        if ((name) == (u"logger")):
            return (self).logger

        if ((name) == (u"_queued")):
            return (self)._queued

        if ((name) == (u"_delivering")):
            return (self)._delivering

        if ((name) == (u"_lock")):
            return (self)._lock

        return None

    def _setField(self, name, value):
        if ((name) == (u"logger")):
            (self).logger = value

        if ((name) == (u"_queued")):
            (self)._queued = _cast(value, lambda: _List)

        if ((name) == (u"_delivering")):
            (self)._delivering = _cast(value, lambda: bool)

        if ((name) == (u"_lock")):
            (self)._lock = _cast(value, lambda: _Lock)


MessageDispatcher.quark_List_mdk_runtime_actors__QueuedMessage__ref = None
MessageDispatcher.mdk_runtime_actors_MessageDispatcher_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_runtime.actors")
