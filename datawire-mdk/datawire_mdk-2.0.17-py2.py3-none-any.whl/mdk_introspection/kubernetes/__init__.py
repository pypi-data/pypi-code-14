# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_introspection.kubernetes")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_introspection


class KubernetesHost(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def get(self):
        return _cast(None, lambda: unicode)

    def _getClass(self):
        return u"mdk_introspection.kubernetes.KubernetesHost"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
KubernetesHost.mdk_introspection_kubernetes_KubernetesHost_ref = None
class KubernetesPort(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def get(self):
        return _cast(None, lambda: int)

    def _getClass(self):
        return u"mdk_introspection.kubernetes.KubernetesPort"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
KubernetesPort.mdk_introspection_kubernetes_KubernetesPort_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_introspection.kubernetes")
