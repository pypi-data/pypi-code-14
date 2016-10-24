# Quark 1.0.452 run at 2016-10-24 14:33:24.783025
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_util")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime.promise
import quark


class WaitForPromise(_QObject):
    """
    Utility to blockingly wait for a Promise to get a value.
    """
    def _init(self):
        pass
    def __init__(self): self._init()

    def _finished(self, value, done):
        (done).acquire();
        (done).wakeup();
        (done).release();
        return True

    @staticmethod
    def wait(p, timeout, description):
        snapshot = (p).value();
        if ((snapshot).hasValue()):
            return (snapshot).getValue()

        done = _Condition();
        waiter = WaitForPromise();
        (p).andThen(quark._BoundMethod(waiter, u"_finished", _List([done])));
        msTimeout = int(round((timeout) * (1000.0)));
        (done).acquire();
        (done).waitWakeup(msTimeout);
        (done).release();
        snapshot = (p).value()
        if (not ((snapshot).hasValue())):
            raise Exception((u"Timeout waiting for ") + (description));

        return (snapshot).getValue()

    def _getClass(self):
        return u"mdk_util.WaitForPromise"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
WaitForPromise.mdk_util_WaitForPromise_ref = None

def toNativePromise(p):
    if (not (False)):
        raise Exception(u"This method only works on Javascript.");

    return


def extend(list, value, size):
    while ((len(list)) < (size)):
        (list).append(value);



def versionMatch(requested, actual):
    if ((requested) == (None)):
        return True

    reqparts = (requested).split(u".");
    actparts = (actual).split(u".");
    extend(reqparts, u"0", 2);
    extend(actparts, u"0", 2);
    reqmajor = (quark.ParsedInt(((reqparts)[0]).strip())).getValue();
    actmajor = (quark.ParsedInt(((actparts)[0]).strip())).getValue();
    reqminor = (quark.ParsedInt(((reqparts)[1]).strip())).getValue();
    actminor = (quark.ParsedInt(((actparts)[1]).strip())).getValue();
    if ((reqmajor) != (actmajor)):
        return False

    if ((actminor) >= (reqminor)):
        return True

    return False


def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_util")
