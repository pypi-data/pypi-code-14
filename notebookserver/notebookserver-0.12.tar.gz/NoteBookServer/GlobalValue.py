# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
import os
import json
from collections import OrderedDict

templateType_map = OrderedDict([
    ("none", 0),
    ("hive", 1),
    ("pig", 2),
    ("emr_hive", 3),
    ("emr_pig", 4)])

currentDir =  "/tmp/notebook-scripts"
usr_home = os.path.expanduser('~')

class ZetModule(object):
    def __init__(self,module_home):

        cfg = SafeConfigParser()
        cfg.read(os.path.expanduser("~/.screwjack.cfg"))
        if cfg.has_section('user') and cfg.has_option('user', 'username'):
            self.username = cfg.get('user', 'username')
        if cfg.has_section('user') and cfg.has_option('user', 'spec_server'):
            self.spec_server = cfg.get('user', 'spec_server')

        self.module_home = os.path.abspath(module_home or '.')
        self.keep_files = False
        self.fast_build = True
        self.dockermachine_env_name = "dev"
        sj_filename = os.path.join(module_home, "spec.json")
        if not os.path.isfile(sj_filename):
            self.spec_json = None
        else:
            with open(sj_filename, "r") as sj_in:
                self.spec_json = json.load(sj_in, object_pairs_hook=OrderedDict)

    @property
    def clusters_db(self):
        import yaml

        yaml_path = os.path.join(os.path.expanduser("~/.datacanvas.yml"))
        if not os.path.isfile(yaml_path):
            print "WARNING: Can not find '~/.datacanvas.yml'"
            return {}
        obj = yaml.load(open(yaml_path).read())
        return {site['Host']: {c['Name']:c for c in site['Clusters']} for site in obj}  #  字典推导式

    @property
    def clusters(self):
        if self.spec_server:
            spec_server_host = self.spec_server.split(":")[0]
            return self.clusters_db.get(spec_server_host, None)
