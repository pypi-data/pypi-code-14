# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_rtp")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_protocol



def getRTPParser():
    """
    Create a JSONParser that can read all messages to/from the MCP.
    """
    parser = mdk_protocol.JSONParser();
    (parser).register(u"open", quark.reflect.Class.get(u"mdk_protocol.Open"));
    (parser).register(u"mdk.protocol.Open", quark.reflect.Class.get(u"mdk_protocol.Open"));
    (parser).register(u"close", quark.reflect.Class.get(u"mdk_protocol.Close"));
    (parser).register(u"mdk.protocol.Close", quark.reflect.Class.get(u"mdk_protocol.Close"));
    (parser).register(u"discovery.protocol.Close", quark.reflect.Class.get(u"mdk_protocol.Close"));
    (parser).register(u"active", quark.reflect.Class.get(u"mdk_discovery.protocol.Active"));
    (parser).register(u"discovery.protocol.Expire", quark.reflect.Class.get(u"mdk_discovery.protocol.Expire"));
    (parser).register(u"expire", quark.reflect.Class.get(u"mdk_discovery.protocol.Expire"));
    (parser).register(u"discovery.protocol.Expire", quark.reflect.Class.get(u"mdk_discovery.protocol.Expire"));
    (parser).register(u"clear", quark.reflect.Class.get(u"mdk_discovery.protocol.Clear"));
    (parser).register(u"discovery.protocol.Clear", quark.reflect.Class.get(u"mdk_discovery.protocol.Clear"));
    (parser).register(u"log", quark.reflect.Class.get(u"mdk_tracing.protocol.LogEvent"));
    (parser).register(u"logack", quark.reflect.Class.get(u"mdk_tracing.protocol.LogAck"));
    (parser).register(u"mdk_tracing.protocol.LogAckEvent", quark.reflect.Class.get(u"mdk_tracing.protocol.LogAck"));
    (parser).register(u"subscribe", quark.reflect.Class.get(u"mdk_tracing.protocol.Subscribe"));
    return parser

_lazyImport.pump("mdk_rtp")
