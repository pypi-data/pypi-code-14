# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_runtime.files")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime.actors
import mdk_runtime


class SubscribeChanges(_QObject):
    """
    Message to FileActor asking to be notified of files' changing contents and
    deletions for the given directory or file path.

    """
    def _init(self):
        self.path = None

    def __init__(self, path):
        self._init()
        (self).path = path

    def _getClass(self):
        return u"mdk_runtime.files.SubscribeChanges"

    def _getField(self, name):
        if ((name) == (u"path")):
            return (self).path

        return None

    def _setField(self, name, value):
        if ((name) == (u"path")):
            (self).path = _cast(value, lambda: unicode)


SubscribeChanges.mdk_runtime_files_SubscribeChanges_ref = None
class FileContents(_QObject):
    """
    Message from FileActor with contents of a file.
    """
    def _init(self):
        self.path = None
        self.contents = None

    def __init__(self, path, contents):
        self._init()
        (self).path = path
        (self).contents = contents

    def _getClass(self):
        return u"mdk_runtime.files.FileContents"

    def _getField(self, name):
        if ((name) == (u"path")):
            return (self).path

        if ((name) == (u"contents")):
            return (self).contents

        return None

    def _setField(self, name, value):
        if ((name) == (u"path")):
            (self).path = _cast(value, lambda: unicode)

        if ((name) == (u"contents")):
            (self).contents = _cast(value, lambda: unicode)


FileContents.mdk_runtime_files_FileContents_ref = None
class FileDeleted(_QObject):
    """
    Message from FileActor indicating a file was deleted.
    """
    def _init(self):
        self.path = None

    def __init__(self, path):
        self._init()
        (self).path = path

    def _getClass(self):
        return u"mdk_runtime.files.FileDeleted"

    def _getField(self, name):
        if ((name) == (u"path")):
            return (self).path

        return None

    def _setField(self, name, value):
        if ((name) == (u"path")):
            (self).path = _cast(value, lambda: unicode)


FileDeleted.mdk_runtime_files_FileDeleted_ref = None
class FileActor(_QObject):
    """
    File interactions.

    Accepts:
    - SubscribeChanges messages, which result in FileContents and FiledDeleted
    messages being sent to original subscriber.

    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def mktempdir(self):
        """
        Create a temporary directory and return its path.
        """
        raise NotImplementedError('`FileActor.mktempdir` is an abstract method')

    def write(self, path, contents):
        """
        Write a file with UTF-8 encoded text.
        """
        raise NotImplementedError('`FileActor.write` is an abstract method')

    def delete(self, path):
        """
        Delete a file.
        """
        raise NotImplementedError('`FileActor.delete` is an abstract method')

    def _getClass(self):
        return u"mdk_runtime.files.FileActor"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass

    def onStop(self):
        """
        The Actor should begin shutting down.
        """
        pass
FileActor.mdk_runtime_files_FileActor_ref = None
class FileActorImpl(FileActor):
    """
    Polling-based subscriptions.

    Should switch to inotify later on.

    Shim over native implementations. Need better way to do this.

    """
    def _init(self):
        FileActor._init(self)
        self.scheduling = None
        self.dispatcher = None
        self.subscriptions = _List([])
        self.stopped = False

    def __init__(self, runtime):
        super(FileActorImpl, self).__init__();
        (self).scheduling = (runtime).getScheduleService()

    def mktempdir(self):
        return __import__("mdk_runtime_files")._mdk_mktempdir()

    def write(self, path, contents):
        __import__("mdk_runtime_files")._mdk_writefile(path, contents);

    def delete(self, path):
        __import__("mdk_runtime_files")._mdk_deletefile(path);

    def _checkSubscriptions(self):
        if ((self).stopped):
            return

        ((self).dispatcher).tell(self, mdk_runtime.Schedule(u"poll", 1.0), (self).scheduling);
        idx = 0;
        while ((idx) < (len((self).subscriptions))):
            (((self).subscriptions)[idx]).poll();
            idx = (idx) + (1)

    def onStart(self, dispatcher):
        (self).dispatcher = dispatcher
        (self)._checkSubscriptions();

    def onStop(self):
        (self).stopped = True

    def onMessage(self, origin, message):
        typeId = (quark.reflect.Class.get(_getClass(message))).id;
        if ((typeId) == (u"mdk_runtime.Happening")):
            (self)._checkSubscriptions();
            return

        if ((typeId) == (u"mdk_runtime.files.SubscribeChanges")):
            subscribe = _cast(message, lambda: SubscribeChanges);
            ((self).subscriptions).append(_Subscription(self, origin, (subscribe).path));
            return

    def _send(self, message, destination):
        ((self).dispatcher).tell(self, message, destination);

    def _getClass(self):
        return u"mdk_runtime.files.FileActorImpl"

    def _getField(self, name):
        if ((name) == (u"scheduling")):
            return (self).scheduling

        if ((name) == (u"dispatcher")):
            return (self).dispatcher

        if ((name) == (u"subscriptions")):
            return (self).subscriptions

        if ((name) == (u"stopped")):
            return (self).stopped

        return None

    def _setField(self, name, value):
        if ((name) == (u"scheduling")):
            (self).scheduling = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"dispatcher")):
            (self).dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)

        if ((name) == (u"subscriptions")):
            (self).subscriptions = _cast(value, lambda: _List)

        if ((name) == (u"stopped")):
            (self).stopped = _cast(value, lambda: bool)


FileActorImpl.quark_List_mdk_runtime_files__Subscription__ref = None
FileActorImpl.mdk_runtime_files_FileActorImpl_ref = None
class _Subscription(_QObject):
    """
    A specific file notification subscription.
    """
    def _init(self):
        self.path = None
        self.actor = None
        self.subscriber = None
        self.previous_listing = _List([])

    def __init__(self, actor, subscriber, path):
        self._init()
        (self).subscriber = subscriber
        (self).actor = actor
        (self).path = path

    def poll(self):
        new_listing = __import__("mdk_runtime_files")._mdk_file_contents((self).path);
        idx = 0;
        while ((idx) < (len(new_listing))):
            ((self).actor)._send(FileContents((new_listing)[idx], __import__("mdk_runtime_files")._mdk_readfile((new_listing)[idx])), (self).subscriber);
            idx = (idx) + (1)

        idx = 0
        jdx = None;
        found = None;
        while ((idx) < (len(self.previous_listing))):
            jdx = 0
            found = False
            while ((jdx) < (len(new_listing))):
                if (((self.previous_listing)[idx]) == ((new_listing)[jdx])):
                    found = True
                    break;

                jdx = (jdx) + (1)

            if (not (found)):
                ((self).actor)._send(FileDeleted((self.previous_listing)[idx]), (self).subscriber);

            idx = (idx) + (1)

        (self).previous_listing = new_listing

    def _getClass(self):
        return u"mdk_runtime.files._Subscription"

    def _getField(self, name):
        if ((name) == (u"path")):
            return (self).path

        if ((name) == (u"actor")):
            return (self).actor

        if ((name) == (u"subscriber")):
            return (self).subscriber

        if ((name) == (u"previous_listing")):
            return (self).previous_listing

        return None

    def _setField(self, name, value):
        if ((name) == (u"path")):
            (self).path = _cast(value, lambda: unicode)

        if ((name) == (u"actor")):
            (self).actor = _cast(value, lambda: FileActorImpl)

        if ((name) == (u"subscriber")):
            (self).subscriber = _cast(value, lambda: mdk_runtime.actors.Actor)

        if ((name) == (u"previous_listing")):
            (self).previous_listing = _cast(value, lambda: _List)


_Subscription.mdk_runtime_files__Subscription_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_runtime.files")
