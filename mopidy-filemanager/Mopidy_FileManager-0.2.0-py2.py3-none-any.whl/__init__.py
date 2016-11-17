from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.2.0'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-FileManager'
    ext_name = 'filemanager'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['root_dir'] = config.String(optional=True)
        schema['show_dotfiles'] = config.Boolean(optional=True)
        return schema

    def setup(self, registry):

        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'static'),
        })

        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.factory,
        })

    def factory(self, config, core):
        from .file_manager import FileManagerHandler

        root_dir = config[self.ext_name].get('root_dir', '/')
        show_dotfiles = config[self.ext_name].get('show_dotfiles', True)
        return [
            ("/fs", FileManagerHandler, {'root': root_dir, 'show_dotfiles': show_dotfiles}),
        ]
