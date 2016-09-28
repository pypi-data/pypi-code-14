"""
This file contains ip address and port related constants.
"""

import os
from six.moves.configparser import ConfigParser


CONFIG_FILE = os.path.expanduser('~/.bonsai')

DEFAULT_BRAIN_API_PORT = '443'
DEFAULT_BRAIN_API_HOST = "api.bons.ai"
DEFAULT_BRAIN_WEB_PORT = '443'
DEFAULT_BRAIN_WEB_HOST = "beta.bons.ai"
DEFAULT_USE_SSL = 'True'

# Keys used in the config file.
_DEFAULT_SECTION = 'DEFAULT'
_PORT = 'Port'
_HOST = 'Host'
_WEB_PORT = 'WebPort'
_WEB_HOST = 'WebHost'
_USERNAME = 'Username'
_ACCESS_KEY = 'AccessKey'
_USE_SSL = 'UseSsl'


class BonsaiConfig():
    def __init__(self):
        self.section = _DEFAULT_SECTION
        self.config = ConfigParser(defaults={
            _PORT: DEFAULT_BRAIN_API_PORT,
            _HOST: DEFAULT_BRAIN_API_HOST,
            _WEB_PORT: DEFAULT_BRAIN_WEB_PORT,
            _WEB_HOST: DEFAULT_BRAIN_WEB_HOST,
            _USERNAME: None,
            _ACCESS_KEY: None,
            _USE_SSL: DEFAULT_USE_SSL
        })
        self.config.read(CONFIG_FILE)

    def _write(self):
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)

    def update_access_key_and_username(self, access_key, username):
        self.config.set(self.section, _ACCESS_KEY, access_key)
        self.config.set(self.section, _USERNAME, username)
        self._write()

    def host(self):
        return self.config.get(self.section, _HOST)

    def port(self):
        return self.config.get(self.section, _PORT)

    def web_host(self):
        return self.config.get(self.section, _WEB_HOST)

    def web_port(self):
        return self.config.get(self.section, _WEB_PORT)

    def username(self):
        return self.config.get(self.section, _USERNAME)

    def access_key(self):
        return self.config.get(self.section, _ACCESS_KEY)

    def use_ssl(self):
        return self.config.getboolean(self.section, _USE_SSL)

    def _can_omit_port(self, port):
        """Function for determining if we can omit the port when formatting
        urls. We can omit the port when we're using the default port, which
        is 443 for ssl connections and 80 for non ssl connections.
        """
        if self.use_ssl():
            return port == "443"
        else:
            return port == "80"

    def _format_url(self, scheme, host, port):
        if self._can_omit_port(port):
            return "{}://{}".format(scheme, host)
        else:
            return "{}://{}:{}".format(scheme, host, port)

    def brain_api_url(self):
        """Uses the scheme, host and port config values to format a url for
        the BRAIN api.
        """
        scheme = "https" if self.use_ssl() else "http"
        return self._format_url(scheme, self.host(), self.port())

    def brain_websocket_url(self):
        """Uses the scheme, host and port config values to format a url for
        the BRAIN api.
        """
        scheme = "wss" if self.use_ssl() else "ws"
        return self._format_url(scheme, self.host(), self.port())

    def brain_web_url(self):
        """Uses the scheme, web host and web port config values to format a
        url for the BRAIN website.
        """
        scheme = "https" if self.use_ssl() else "http"
        return self._format_url(scheme, self.web_host(), self.web_port())

    def update(self, **kwargs):
        """Updates the configuration with the Key/value pairs in kwargs."""
        if not kwargs:
            return
        for key, value in kwargs.items():
            self.config.set(self.section, key, str(value))
        self._write()
