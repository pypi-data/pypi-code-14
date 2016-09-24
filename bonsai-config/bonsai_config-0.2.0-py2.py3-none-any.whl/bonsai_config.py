"""
This file contains ip address and port related constants.
"""

import os
from six.moves.configparser import ConfigParser


CONFIG_FILE = os.path.expanduser('~/.bonsai')

DEFAULT_BRAIN_API_PORT = '80'
DEFAULT_BRAIN_API_HOST = "api.bons.ai"
DEFAULT_BRAIN_WEB_PORT = '80'
DEFAULT_BRAIN_WEB_HOST = "beta.bons.ai"

# Keys used in the config file.
_DEFAULT_SECTION = 'DEFAULT'
_PORT = 'Port'
_HOST = 'Host'
_WEB_PORT = 'WebPort'
_WEB_HOST = 'WebHost'
_USERNAME = 'Username'
_ACCESS_KEY = 'AccessKey'


class BonsaiConfig():
    def __init__(self):
        self.section = _DEFAULT_SECTION
        self.config = ConfigParser(defaults={
            _PORT: DEFAULT_BRAIN_API_PORT,
            _HOST: DEFAULT_BRAIN_API_HOST,
            _WEB_PORT: DEFAULT_BRAIN_WEB_PORT,
            _WEB_HOST: DEFAULT_BRAIN_WEB_HOST,
            _USERNAME: None,
            _ACCESS_KEY: None
        })
        self.config.read(CONFIG_FILE)

    def _write(self):
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)

    def update_access_key_and_username(self, access_key, username):
        self.config.set(self.section, _ACCESS_KEY, access_key)
        self.config.set(self.section, _USERNAME, username)
        self._write()

    def uri(self):
        value = self.config['DEFAULT'].get('Uri', None)
        if value:
            return value
        return 'http://{}:{}'.format(self.host(), self.port())

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

    def brain_api_netloc(self):
        """Get the brain api host and port formatted as a netloc."""
        return "{}:{}".format(self.host(), self.port())

    def brain_web_netloc(self):
        """Get the brain web host and port formatted as a netloc."""
        return "{}:{}".format(self.web_host(), self.web_port())

    def update(self, **kwargs):
        """Updates the configuration with the Key/value pairs in kwargs."""
        if not kwargs:
            return
        for key, value in kwargs.items():
            self.config.set(self.section, key, str(value))
        self._write()
