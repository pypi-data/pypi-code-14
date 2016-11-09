from os.path import expanduser

import yaml


def config_from_file(path):
    with open(expanduser(path), 'r') as f:
        return yaml.load(f)
