# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
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
    extend(reqparts, u"0", 3);
    extend(actparts, u"0", 3);
    if (((reqparts)[0]) != ((actparts)[0])):
        return False

    if (((actparts)[1]) > ((reqparts)[1])):
        return True

    if (((actparts)[1]) < ((reqparts)[1])):
        return False

    return ((actparts)[2]) >= ((reqparts)[2])


def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_util")
