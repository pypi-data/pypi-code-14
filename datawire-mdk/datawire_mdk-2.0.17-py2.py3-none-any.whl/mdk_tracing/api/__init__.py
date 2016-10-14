# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_tracing.api")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_protocol
import quark
import mdk_tracing.protocol


class ApiHandler(object):

    def getLogEvents(self, request):
        """
        Retrieves zero or more events based on the provided request parameters.
        """
        raise NotImplementedError('`ApiHandler.getLogEvents` is an abstract method')

ApiHandler.mdk_tracing_api_ApiHandler_ref = None
class GetLogEventsRequest(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.startTime = 0
        self.endTime = quark.now()

    def __init__(self):
        super(GetLogEventsRequest, self).__init__();

    @staticmethod
    def decode(encoded):
        return _cast(mdk_protocol.Serializable.decodeClassName(u"mdk_tracing.api.GetLogEventsRequest", encoded), lambda: GetLogEventsRequest)

    def _getClass(self):
        return u"mdk_tracing.api.GetLogEventsRequest"

    def _getField(self, name):
        if ((name) == (u"startTime")):
            return (self).startTime

        if ((name) == (u"endTime")):
            return (self).endTime

        return None

    def _setField(self, name, value):
        if ((name) == (u"startTime")):
            (self).startTime = _cast(value, lambda: int)

        if ((name) == (u"endTime")):
            (self).endTime = _cast(value, lambda: int)


GetLogEventsRequest.mdk_tracing_api_GetLogEventsRequest_ref = None
class GetLogEventsResult(mdk_protocol.Serializable):
    def _init(self):
        mdk_protocol.Serializable._init(self)
        self.result = None

    def __init__(self):
        super(GetLogEventsResult, self).__init__();

    @staticmethod
    def decode(encoded):
        return _cast(mdk_protocol.Serializable.decodeClassName(u"mdk_tracing.api.GetLogEventsResult", encoded), lambda: GetLogEventsResult)

    def _getClass(self):
        return u"mdk_tracing.api.GetLogEventsResult"

    def _getField(self, name):
        if ((name) == (u"result")):
            return (self).result

        return None

    def _setField(self, name, value):
        if ((name) == (u"result")):
            (self).result = _cast(value, lambda: _List)


GetLogEventsResult.quark_List_mdk_tracing_protocol_LogEvent__ref = None
GetLogEventsResult.mdk_tracing_api_GetLogEventsResult_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_tracing.api")
