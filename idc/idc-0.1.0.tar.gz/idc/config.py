import ConfigParser
import utils
import os

DEFAULTS = {
    'media_path':  '../media',
    'artifacts_path': '../artifacts',
    'log_path': '../logs',
    'sessions_path': '../sessions',
    'video_format': 'XVID',
    'server_port': '5000',
    'server_ip': '127.0.0.1',
    'output_file_path': '../artifacts',
    }

class Config(object):

    __metaclass__ = utils.Singleton

    def __init__(self):
        self.config = None
        self.config_path = None

        self.set_config_path()
        self._set_config()

    def set_config_path(self):
        home_dir = os.path.expanduser('~')
        self.config_path = os.path.join(
            home_dir,
            '.idc/idc.conf'
        )

    def _set_config(self):

        config_parser = ConfigParser.ConfigParser(defaults=DEFAULTS)
        config_parser.read(self.config_path)
        self.config = config_parser

    def reload(self):
        self._set_config()

    def __getitem__(self, item):
        try:
            if self.config.has_section('idc'):
                return self.config.get('idc', item)
            else:
                return DEFAULTS[item]
        except ConfigParser.Error as e:
            print e
            raise KeyError(item)
