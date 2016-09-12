from __future__ import unicode_literals

import os

from mopidy import config, ext

__version__ = '0.2.4'


class Extension(ext.Extension):
    dist_name = 'Mopidy-Tachikoma'
    ext_name = 'tachikoma'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['slack_token'] = config.Secret()
        return schema

    def setup(self, registry):
        from .bot import TachikomaFrontend
        registry.add('frontend', TachikomaFrontend)
