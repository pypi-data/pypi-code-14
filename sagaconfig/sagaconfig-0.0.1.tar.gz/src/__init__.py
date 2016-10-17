"""Automatically load a configuration according to the RUN_ENV parameter."""
import os
import logging
from importlib.util import spec_from_file_location, module_from_spec

log = logging.getLogger(__name__)


def merge_configs(a, b):
    """Recursively merge config dictionaries."""
    new_config = dict()
    for key in a.keys() ^ b.keys():
        new_config[key] = a.get(key) or b[key]

    for key in a.keys() & b.keys():
        if isinstance(a[key], dict) and isinstance(b[key], dict):
            new_config[key] = merge_configs(a[key], b[key])
        else:
            log.warn(
                'Overriding keys with different types %s and %s',
                type(a[key]), type(b[key]))
            new_config[key] = b[key]
    return new_config


def load_config(name):
    """Load config with given name.

    Looks in the config folder of the current working directory for
    a file named %{name}.py.
    """
    try:
        path = os.path.join(os.getcwd(), 'config', name.lower() + '.py')
        spec = spec_from_file_location(name, path)
        this_config = module_from_spec(spec)
        spec.loader.exec_module(this_config)
        return this_config.config
    except FileNotFoundError:
        log.warn('Not found %s config', name)
        return dict()


config = merge_configs(
    load_config('default'),
    load_config(os.environ.get('RUN_ENV') or 'development'))
