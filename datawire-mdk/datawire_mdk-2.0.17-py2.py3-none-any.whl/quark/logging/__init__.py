# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("quark.logging")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect


class Appender(_QObject):
    """
    Destination for logging
    """
    def _init(self):
        self.name = None

    def __init__(self, name):
        self._init()
        (self).name = name

    def _getClass(self):
        return u"quark.logging.Appender"

    def _getField(self, name):
        if ((name) == (u"name")):
            return (self).name

        return None

    def _setField(self, name, value):
        if ((name) == (u"name")):
            (self).name = _cast(value, lambda: unicode)


Appender.quark_logging_Appender_ref = None

def stdout():
    """
    Logging appender that sends log messages to standard output
    """
    return Appender(u":STDOUT")


def stderr():
    """
    Logging appender that sends log messages to standard error
    """
    return Appender(u":STDERR")


def file(path):
    """
    Logging appender that sends log messages to a file
    """
    return Appender(path)


def setEnvironmentOverride(envVar, level):
    """
    Set an environment variable to override logging set up in the code
    """
    Config._overrideEnvVar = envVar
    Config._overrideLevel = level

class Config(_QObject):
    """
    Logging configurator
    """
    def _init(self):
        self.appender = stderr()
        self.level = u"INFO"

    def __init__(self): self._init()

    def setAppender(self, appender):
        """
        Set the destination for logging, default stderr()
        """
        (self).appender = appender
        return self

    def setLevel(self, level):
        """
        set the logging level [trace|debug|info|warn|error], default 'info'
        """
        (self).level = level
        return self

    @staticmethod
    def _getOverrideIfExists():
        if ((Config._overrideEnvVar) == (None)):
            return _cast(None, lambda: unicode)

        envVarValue = os.environ.get(Config._overrideEnvVar);
        if (((((envVarValue) == (None)) or ((envVarValue) == (u""))) or ((envVarValue) == (u"0"))) or (((envVarValue).lower()) == (u"false"))):
            return _cast(None, lambda: unicode)

        return envVarValue

    @staticmethod
    def _autoconfig():
        return (not (Config._configured)) and ((Config._getOverrideIfExists()) != (None))

    def configure(self):
        """
        Configure the logging
        """
        envVarValue = Config._getOverrideIfExists();
        if ((envVarValue) != (None)):
            if (((envVarValue) == (u"1")) or (((envVarValue).lower()) == (u"true"))):
                self.appender = stderr()
            else:
                self.appender = file(envVarValue)

            self.level = Config._overrideLevel

        _configure_logging((self.appender), (self.level));
        Config._configured = True

    def _getClass(self):
        return u"quark.logging.Config"

    def _getField(self, name):
        if ((name) == (u"_overrideEnvVar")):
            return Config._overrideEnvVar

        if ((name) == (u"_overrideLevel")):
            return Config._overrideLevel

        if ((name) == (u"_configured")):
            return Config._configured

        if ((name) == (u"appender")):
            return (self).appender

        if ((name) == (u"level")):
            return (self).level

        return None

    def _setField(self, name, value):
        if ((name) == (u"_overrideEnvVar")):
            Config._overrideEnvVar = _cast(value, lambda: unicode)

        if ((name) == (u"_overrideLevel")):
            Config._overrideLevel = _cast(value, lambda: unicode)

        if ((name) == (u"_configured")):
            Config._configured = _cast(value, lambda: bool)

        if ((name) == (u"appender")):
            (self).appender = _cast(value, lambda: Appender)

        if ((name) == (u"level")):
            (self).level = _cast(value, lambda: unicode)


Config._overrideEnvVar = u"QUARK_TRACE"
Config._overrideLevel = u"DEBUG"
Config._configured = False
Config.quark_logging_Config_ref = None

def makeConfig():
    """
    Create a logging configurator
    """
    return Config()


def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("quark.logging")
