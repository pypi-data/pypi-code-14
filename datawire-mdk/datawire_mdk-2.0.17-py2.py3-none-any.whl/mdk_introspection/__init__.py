# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_introspection")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import mdk_runtime
import quark.concurrent
import quark
import mdk_introspection.aws
import mdk_introspection.kubernetes


class Supplier(object):
    """
    A Supplier has a 'get' method that can return a value to anyone who needs it.
    """

    def get(self):
        """
        Gets a value
        """
        raise NotImplementedError('`Supplier.get` is an abstract method')

Supplier.mdk_introspection_Supplier_quark_Object__ref = None
class DatawireToken(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def getToken(env):
        """
        Returns the Datawire Access Token by reading the environment variable DATAWIRE_TOKEN.
        """
        token = ((env).var(DatawireToken.TOKEN_VARIABLE_NAME)).get();
        if ((token) == (None)):
            (quark.concurrent.Context.runtime()).fail(u"Neither 'MDK_DISCOVERY_SOURCE' nor 'DATAWIRE_TOKEN' are set. Either set the former to an existing discovery source (e.g. 'synapse:path=/synapse/output_files/'), or use the Datawire cloud services. For the latter please visit https://app.datawire.io/#/signup to create a free account and get a token.");

        return token

    def _getClass(self):
        return u"mdk_introspection.DatawireToken"

    def _getField(self, name):
        if ((name) == (u"TOKEN_VARIABLE_NAME")):
            return DatawireToken.TOKEN_VARIABLE_NAME

        return None

    def _setField(self, name, value):
        if ((name) == (u"TOKEN_VARIABLE_NAME")):
            DatawireToken.TOKEN_VARIABLE_NAME = _cast(value, lambda: unicode)


DatawireToken.TOKEN_VARIABLE_NAME = u"DATAWIRE_TOKEN"
DatawireToken.mdk_introspection_DatawireToken_ref = None
class Platform(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    @staticmethod
    def platformType(env):
        result = ((env).var(Platform.PLATFORM_TYPE_VARIABLE_NAME)).get();
        if ((result) != (None)):
            result = (result).upper()

        return result

    @staticmethod
    def getRoutableHost(env):
        """
        Returns the routable hostname or IP for this service instance.
        This method always returns the value of the environment variable DATAWIRE_ROUTABLE_HOST if it is defined.
        """
        result = _cast(None, lambda: unicode);
        logger = quark._getLogger(u"Platform");
        if (((env).var(Platform.ROUTABLE_HOST_VARIABLE_NAME)).isDefined()):
            (logger).debug(((u"Using value in environment variable '") + (Platform.ROUTABLE_HOST_VARIABLE_NAME)) + (u"'"));
            result = ((env).var(Platform.ROUTABLE_HOST_VARIABLE_NAME)).get()
        else:
            if ((Platform.platformType(env)) == (None)):
                (logger).error(((u"Platform type not specified in environment variable '") + (Platform.PLATFORM_TYPE_VARIABLE_NAME)) + (u"'"));
                (quark.concurrent.Context.runtime()).fail(u"Environment variable 'DATAWIRE_PLATFORM_TYPE' is not set.");

            if ((Platform.platformType(env)).startswith(Platform.PLATFORM_TYPE_EC2)):
                (logger).debug((Platform.PLATFORM_TYPE_VARIABLE_NAME) + (u" = EC2"));
                parts = (Platform.platformType(env)).split(u":");
                (logger).debug((u"Platform Scope = ") + ((parts)[1]));
                if ((len(parts)) == (2)):
                    return (mdk_introspection.aws.Ec2Host(env, (parts)[1])).get()
                else:
                    (logger).error(((u"Invalid format for '") + (Platform.PLATFORM_TYPE_VARIABLE_NAME)) + (u"' starting with 'ec2'. Expected (ec2:<scope>)"));
                    (quark.concurrent.Context.runtime()).fail(u"Invalid format for DATAWIRE_PLATFORM_TYPE == EC2. Expected EC2:<scope>.");

        return result

    @staticmethod
    def getRoutablePort(env, servicePort):
        """
        Returns the routable port number for this service instance or uses the provided port if a value cannot be resolved.
        This method always returns the value of the environment variable DATAWIRE_ROUTABLE_PORT if it is defined.
        """
        if (((env).var(Platform.ROUTABLE_PORT_VARIABLE_NAME)).isDefined()):
            return int(((env).var(Platform.ROUTABLE_PORT_VARIABLE_NAME)).get())

        if ((Platform.platformType(env)) == (Platform.PLATFORM_TYPE_KUBERNETES)):
            return (mdk_introspection.kubernetes.KubernetesPort()).get()

        return servicePort

    def _getClass(self):
        return u"mdk_introspection.Platform"

    def _getField(self, name):
        if ((name) == (u"PLATFORM_TYPE_VARIABLE_NAME")):
            return Platform.PLATFORM_TYPE_VARIABLE_NAME

        if ((name) == (u"PLATFORM_TYPE_EC2")):
            return Platform.PLATFORM_TYPE_EC2

        if ((name) == (u"PLATFORM_TYPE_GOOGLE_COMPUTE")):
            return Platform.PLATFORM_TYPE_GOOGLE_COMPUTE

        if ((name) == (u"PLATFORM_TYPE_GOOGLE_CONTAINER")):
            return Platform.PLATFORM_TYPE_GOOGLE_CONTAINER

        if ((name) == (u"PLATFORM_TYPE_KUBERNETES")):
            return Platform.PLATFORM_TYPE_KUBERNETES

        if ((name) == (u"ROUTABLE_HOST_VARIABLE_NAME")):
            return Platform.ROUTABLE_HOST_VARIABLE_NAME

        if ((name) == (u"ROUTABLE_PORT_VARIABLE_NAME")):
            return Platform.ROUTABLE_PORT_VARIABLE_NAME

        return None

    def _setField(self, name, value):
        if ((name) == (u"PLATFORM_TYPE_VARIABLE_NAME")):
            Platform.PLATFORM_TYPE_VARIABLE_NAME = _cast(value, lambda: unicode)

        if ((name) == (u"PLATFORM_TYPE_EC2")):
            Platform.PLATFORM_TYPE_EC2 = _cast(value, lambda: unicode)

        if ((name) == (u"PLATFORM_TYPE_GOOGLE_COMPUTE")):
            Platform.PLATFORM_TYPE_GOOGLE_COMPUTE = _cast(value, lambda: unicode)

        if ((name) == (u"PLATFORM_TYPE_GOOGLE_CONTAINER")):
            Platform.PLATFORM_TYPE_GOOGLE_CONTAINER = _cast(value, lambda: unicode)

        if ((name) == (u"PLATFORM_TYPE_KUBERNETES")):
            Platform.PLATFORM_TYPE_KUBERNETES = _cast(value, lambda: unicode)

        if ((name) == (u"ROUTABLE_HOST_VARIABLE_NAME")):
            Platform.ROUTABLE_HOST_VARIABLE_NAME = _cast(value, lambda: unicode)

        if ((name) == (u"ROUTABLE_PORT_VARIABLE_NAME")):
            Platform.ROUTABLE_PORT_VARIABLE_NAME = _cast(value, lambda: unicode)


Platform.PLATFORM_TYPE_VARIABLE_NAME = u"DATAWIRE_PLATFORM_TYPE"
Platform.PLATFORM_TYPE_EC2 = u"EC2"
Platform.PLATFORM_TYPE_GOOGLE_COMPUTE = u"GOOGLE_COMPUTE"
Platform.PLATFORM_TYPE_GOOGLE_CONTAINER = u"GOOGLE_CONTAINER"
Platform.PLATFORM_TYPE_KUBERNETES = u"Kubernetes"
Platform.ROUTABLE_HOST_VARIABLE_NAME = u"DATAWIRE_ROUTABLE_HOST"
Platform.ROUTABLE_PORT_VARIABLE_NAME = u"DATAWIRE_ROUTABLE_PORT"
Platform.mdk_introspection_Platform_ref = None


def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_introspection")
