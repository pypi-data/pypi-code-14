"""
Load config files once per interpreter invocation.
"""

import os
from six.moves.configparser import (
    SafeConfigParser, MissingSectionHeaderError,
    NoOptionError, NoSectionError)

from globus_sdk.exc import GlobusError


def _get_lib_config_path():
    """
    Get the location of the default config file in globus_sdk
    This could be made part of GlobusConfigParser, but it really doesn't handle
    any class-specific state. Just a helper for getting the location of a file.
    """
    fname = "globus.cfg"
    try:
        import pkg_resources
        path = pkg_resources.resource_filename("globus_sdk", fname)
    except ImportError:
        pkg_path = os.path.dirname(__file__)
        path = os.path.join(pkg_path, fname)
    return path


class GlobusConfigParser(object):
    """
    Wraps a SafeConfigParser to do modified get()s and config file loading.
    """
    _GENERAL_CONF_SECTION = 'general'

    def __init__(self):
        self._parser = SafeConfigParser()
        self._load_config()

    def _load_config(self):
        # TODO: /etc is not windows friendly, not sure about expanduser
        try:
            self._parser.read([_get_lib_config_path(), "/etc/globus.cfg",
                               os.path.expanduser("~/.globus.cfg")])
        except MissingSectionHeaderError:
            raise GlobusError(
                "Failed to parse your ~/.globus.cfg Your config file may be "
                "in an old format. Please visit https://tokens.globus.org/ to "
                "get the latest format of this file.")

    def get(self, option,
            section=None, environment=None,
            failover_to_general=False, check_env=False,
            type_cast=str):
        """
        Attempt to lookup an option in the config file. Optionally failover to
        the general section if the option is not found.

        Also optionally, check for a relevant environment variable, which is
        named always as GLOBUS_SDK_{option.upper()}. Note that 'section'
        doesn't slot into the naming at all. Otherwise, we'd have to contend
        with GLOBUS_SDK_GENERAL_... for almost everything, and
        GLOBUS_SDK_ENVIRONMENT\ PROD_... which is awful.

        Returns None for an unfound key, rather than raising a NoOptionError.
        """
        # envrionment is just a fancy name for sections that start with
        # 'environment '
        if environment:
            section = 'environment ' + environment
        # if you don't specify a section or an environment, assume it's the
        # general conf section
        if section is None:
            section = self._GENERAL_CONF_SECTION

        # if this is a config option which checks the shell env, look there
        # *first* for a value -- env values have higher precedence than config
        # files so that you can locally override the behavior of a command in a
        # given shell or subshell
        env_option_name = 'GLOBUS_SDK_{0}'.format(option.upper())
        value = None
        if check_env and env_option_name in os.environ:
            value = os.environ[env_option_name]
        else:
            try:
                value = self._parser.get(section, option)
            except (NoOptionError, NoSectionError):
                if failover_to_general:
                    value = self.get(option,
                                     section=self._GENERAL_CONF_SECTION)

        if value is not None:
            value = type_cast(value)
        return value


def _get_parser():
    """
    Singleton pattern implemented via a global varaible and function.
    There is only ever one _parser, and it is always returned by this function.
    """
    global _parser
    if _parser is None:
        _parser = GlobusConfigParser()
    return _parser
# at import-time, it's None
_parser = None


def get_service_url(environment, service):
    p = _get_parser()
    option = service + "_service"
    # TODO: validate with urlparse?
    return p.get(option, environment=environment)


def get_ssl_verify(environment):
    p = _get_parser()
    value = p.get("ssl_verify", environment=environment,
                  failover_to_general=False, check_env=True,
                  type_cast=_bool_cast)
    if value is None:
        return True
    return value


def _bool_cast(value):
    value = value.lower()
    if value in ("1", "yes", "true", "on"):
        return True
    elif value in ("0", "no", "false", "off"):
        return False
    raise ValueError("Invalid config bool")


def _get_token(tok_type, environment):
    p = _get_parser()

    tkn = p.get(tok_type, environment=environment,
                failover_to_general=True, check_env=True)

    return tkn


def get_auth_token(environment):
    """
    Fetch any auth token from the config, if one is present
    """
    return _get_token('auth_token', environment)


def get_transfer_token(environment):
    """
    Fetch any transfer token from the config, if one is present
    """
    return _get_token('transfer_token', environment)


def get_default_environ():
    """
    Get the default environment to look for in the config, as a string.
    Typically just "default", but it can be overridden with
    `GLOBUS_SDK_ENVIRONMENT` in the shell environment. In that case, any client
    which does not explicitly specify its environment will use this value.
    """
    return os.environ.get('GLOBUS_SDK_ENVIRONMENT', 'default')
