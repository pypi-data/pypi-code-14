# Quark 1.0.452 run at 2016-10-13 16:26:58.627837
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.error")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect


class Error(_QObject):
    def _init(self):
        self.message = None

    def __init__(self, message):
        self._init()
        (self).message = message

    def getMessage(self):
        return self.message

    def toString(self):
        return ((u"Error(") + ((self).message)) + (u")")

    def _getClass(self):
        return u"quark.error.Error"

    def _getField(self, name):
        if ((name) == (u"message")):
            return (self).message

        return None

    def _setField(self, name, value):
        if ((name) == (u"message")):
            (self).message = _cast(value, lambda: unicode)


Error.quark_error_Error_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.error")
