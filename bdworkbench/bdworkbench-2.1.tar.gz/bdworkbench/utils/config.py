#
# Copyright (c) 2016 BlueData Software, Inc.
#
from __future__ import print_function

import os
import ConfigParser

KEY_BASE = 'base'
KEY_SDKBASE = 'sdkbase'
KEY_DELIVERABLES = 'deliverables_dir'

KEY_LOGDIR = 'log_dir'
KEY_IMAGEDIR = 'image_dir'
KEY_STAGEDIR = 'staging_dir'
KEY_APPCONFIGDIR = 'appconfig_dir'

KEY_DEF_ORGNAME = 'def_orgname'

SECTION_WB = 'workbench'

CONF_FILENAME = 'bench.conf'
DIRNAME = os.path.dirname(os.path.realpath(__file__))
SDK_BASE_DIR = os.path.abspath(os.path.join(DIRNAME, '..'))

class WBConfig(object):
    """

    """

    def __init__(self):
        """
        """
        cwd = os.getcwd()
        self.sdkcfg = os.path.join(SDK_BASE_DIR, CONF_FILENAME)
        self.localcfg = os.path.join(cwd, CONF_FILENAME)
        self.config = ConfigParser.SafeConfigParser({'ABSCWD': cwd})
        self.config.read([self.localcfg, self.sdkcfg])

        if os.getenv('USE_BDS_INTERNAL_ORGNAME', 'false') == 'true':
            orgname = 'bluedata'
        else:
            orgname = None

        self.defaults = {KEY_BASE: cwd, KEY_SDKBASE: SDK_BASE_DIR,
                         KEY_DEF_ORGNAME: orgname}

    def _save(self):
        """
        Save the modified config params to the local config file.
        """
        with open(self.localcfg, 'wb') as f:
            config.write(f)

    def get(self, section, key, default=None):
        """

        """
        try:
            return self.config.get(section, key, vars=self.defaults)
        except ConfigParser.NoSectionError, ConfigParser.NoOptionError:
            return default

    def addOrUpdate(self, section, key, value):
        """

        """
        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, key, str(value))
        self._save()

__all__ = ['WBConfig', 'KEY_BASE', 'KEY_SDKBASE', 'KEY_LOGDIR', 'KEY_IMAGEDIR',
           'KEY_COMPSDIR', 'KEY_APPCONFIGDIR', 'SECTION_WB']
