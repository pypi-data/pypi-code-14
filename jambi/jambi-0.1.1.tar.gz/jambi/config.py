import configparser
import logging
import os

from jambi.exceptions import ImproperlyConfigured


logger = logging.getLogger(__name__)


class JambiConfig(object):
    """jambi configuration object"""
    def __init__(self):
        self.config, self.location = self.load_config()

    def load_config(self):
        """loads the jambi configuration from file"""
        config = configparser.ConfigParser()
        location = os.path.abspath('jambi.conf')
        config.read(location)
        if self.is_valid_config(config):
            logger.info('Configuration loaded.')
        else:
            raise ImproperlyConfigured('Configuration is not valid.')
        return config, os.getcwd()

    def is_valid_config(self, config):
        """determines if the supplied config is a valid jambi configuration

        Arguments:
        config -- the configparser config after calling read() on it

        Returns:
        (bool) whether the configuration is a valid jambi configuration"""
        return \
            config.has_section('database') and \
            config.has_option('migrate', 'location')

    def get(self, section, option):
        """a safe way to get things out of the loaded jambi configuration

        Arguments:
        section -- the section to get the option out of
        option -- the option to get from the supplied section

        Returns:
        the desired value from the loaded jambi configuration

        Raises:
        ImproperlyConfigured -- if the configuration value cannot be found
        """
        try:
            return self.config[section][option]
        except KeyError as e:
            raise ImproperlyConfigured(
                'Unable to find \'{}\' in config file.'.format(e))
