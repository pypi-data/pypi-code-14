# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.spi")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark
import quark.logging
import quark.spi_api_tracing
import quark.spi_api


class RuntimeSpi(object):
    pass
RuntimeSpi.quark_spi_RuntimeSpi_ref = None
class RuntimeFactory(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def makeRuntime(self):
        spi = _RuntimeFactory.create();
        api = None;
        if (not (RuntimeFactory.env_checked)):
            RuntimeFactory.enable_tracing = (quark.logging.Config._getOverrideIfExists()) != (None)
            RuntimeFactory.env_checked = True

        if (RuntimeFactory.enable_tracing):
            api = quark.spi_api_tracing.RuntimeProxy(spi)
        else:
            api = quark.spi_api.RuntimeProxy(spi)

        return api

    def _getClass(self):
        return u"quark.spi.RuntimeFactory"

    def _getField(self, name):
        if ((name) == (u"factory")):
            return RuntimeFactory.factory

        if ((name) == (u"enable_tracing")):
            return RuntimeFactory.enable_tracing

        if ((name) == (u"env_checked")):
            return RuntimeFactory.env_checked

        return None

    def _setField(self, name, value):
        if ((name) == (u"factory")):
            RuntimeFactory.factory = _cast(value, lambda: RuntimeFactory)

        if ((name) == (u"enable_tracing")):
            RuntimeFactory.enable_tracing = _cast(value, lambda: bool)

        if ((name) == (u"env_checked")):
            RuntimeFactory.env_checked = _cast(value, lambda: bool)


RuntimeFactory.factory = RuntimeFactory()
RuntimeFactory.enable_tracing = True
RuntimeFactory.env_checked = False
RuntimeFactory.quark_spi_RuntimeFactory_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.spi")
