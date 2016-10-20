# -*- coding: utf-8 -*-

import os
import sys
import json
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Simple config class to get and save config variables.
    """
    def __init__(self, config_file="/etc/dirvishbot/config.json"):
        """
        :param str config_file: The path to the config file.
        """
        self._config_file = config_file
        self._config = None
        self.init_config()

    def init_config(self):
        """
        Load the config variables from self._config_file.

        :return:
        """
        if os.path.isfile(self._config_file):
            try:
                with open(self._config_file, 'r') as f:
                    self._config = json.loads('\n'.join(f.readlines()))
                    if not 'api_token' in self._config:
                        raise Exception('Missing api_token in config "%s"' % self._config_file)
            except Exception as e:
                logger.error("Failed to load %s" % self._config_file, exc_info=True)
                sys.exit(1)
        else:
            self._config = {}

    def get(self, key):
        """
        Get the value for the requested key.

        :param str key:
        :return: object|None
        """
        if key in self._config:
            return self._config[key]
        return None

    def set(self, key, value):
        """
        Write a key/value pair to the config(-file)

        :param str key:
        :param object value:
        :return:
        """
        try:
            self._config[key] = value
            with open(self._config_file, 'w') as f:
                f.write(json.dumps(self._config, indent=4, sort_keys=True))
        except Exception as e:
            logger.error('Failed to set "%s"="%s" to config file "%s"' % (key, value, self._config_file), exc_info=True)


