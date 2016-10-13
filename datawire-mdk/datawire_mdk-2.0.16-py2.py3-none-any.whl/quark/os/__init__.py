# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.os")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark.error
import quark.concurrent


class OSError(quark.error.Error):
    def _init(self):
        quark.error.Error._init(self)

    def __init__(self, message):
        super(OSError, self).__init__(message);

    def _getClass(self):
        return u"quark.os.OSError"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


OSError.quark_os_OSError_ref = None
class FileContents(quark.concurrent.Future):
    def _init(self):
        quark.concurrent.Future._init(self)
        self.value = None

    def __init__(self):
        super(FileContents, self).__init__();

    def _getClass(self):
        return u"quark.os.FileContents"

    def _getField(self, name):
        if ((name) == (u"_context")):
            return (self)._context

        if ((name) == (u"_finished")):
            return (self)._finished

        if ((name) == (u"_error")):
            return (self)._error

        if ((name) == (u"_callbacks")):
            return (self)._callbacks

        if ((name) == (u"_lock")):
            return (self)._lock

        if ((name) == (u"value")):
            return (self).value

        return None

    def _setField(self, name, value):
        if ((name) == (u"_context")):
            (self)._context = _cast(value, lambda: quark.concurrent.Context)

        if ((name) == (u"_finished")):
            (self)._finished = _cast(value, lambda: bool)

        if ((name) == (u"_error")):
            (self)._error = _cast(value, lambda: quark.error.Error)

        if ((name) == (u"_callbacks")):
            (self)._callbacks = _cast(value, lambda: _List)

        if ((name) == (u"_lock")):
            (self)._lock = _cast(value, lambda: _Lock)

        if ((name) == (u"value")):
            (self).value = _cast(value, lambda: unicode)


FileContents.quark_os_FileContents_ref = None

def readFileAsString(path):
    """
    Read the entire contents of a file into a String. Assume UTF-8 encoding.
    Returns a FileContents Future instance.
    if result.getError() is null then result.value has the file contents.
    """
    result = FileContents();
    _get_file_contents((path), (result));
    return result


def getUserHomeDir():
    """
    Return the path to the current user's home directory
    """
    return os.path.expanduser("~")

class Environment(_QObject):
    """
    Class for interacting with the process environment
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def getEnvironment():
        """
        Retrieve the Environment singleton
        """
        return Environment.ENV

    def _q__get__(self, key):
        """
        Fetch the value of an environment variable.
        Returns null if the variable is not set.
        """
        return os.environ.get(key)

    def get(self, key, default_value):
        """
        Fetch the value of an environment variable.
        Returns the specified default if the variable is not set.
        """
        value = os.environ.get(key);
        if ((value) == (None)):
            return default_value

        return value

    @staticmethod
    def getUser():
        """
        Fetch the value of $USER
        """
        return os.environ.get(u"USER")

    def _getClass(self):
        return u"quark.os.Environment"

    def _getField(self, name):
        if ((name) == (u"ENV")):
            return Environment.ENV

        return None

    def _setField(self, name, value):
        if ((name) == (u"ENV")):
            Environment.ENV = _cast(value, lambda: Environment)


Environment.ENV = Environment()
Environment.quark_os_Environment_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.os")
