# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
Configuration file reader for gravely.
Uses direct python evaluation in a new module to obtain and store values.
"""

import collections
import imp


DEFAULT_CONFIG_STRING = '''
#!/usr/bin/python3
"""This is an example configuration file for 'gravely' gravity simulator."""

# To use a custom gravely installation, use:
#import sys; sys.path.append('/path/to/custom/gravely_directory')

from gravely.body import Body
from gravely.units import g, kg, cm, m, km, sec, hour, day


MOON_PERIOD = 27.3 * day
t_max = MOON_PERIOD
dt = 100 * sec
substepping_max_depth = 100
substepping_target_acceleration = 1 * cm / sec**2 / dt
diagnostics_period = 1 * hour

EARTH_MASS = 5.9721e24 * kg
MOON_MASS = 7.3459e22 * kg
MOON_ORBIT_RADIUS = 384400 * km
MOON_ORBIT_VELOCITY = 1.022 * km / sec

bodies = (
    Body(m=EARTH_MASS),  # Earth
    Body(m=MOON_MASS, x=MOON_ORBIT_RADIUS, vy=-MOON_ORBIT_VELOCITY)  # Moon
)

data_filename = 'gravely.out.hdf5'

plot_limits = ((-4e10, 4e10),) * 3
plot_colors = ('black', '#ff7700')
plot_markers = 'Do'
plot_trail_length = 1 * day

animation_writer = 'ffmpeg'
animation_writer_parameters = {'fps': 60, 'bitrate': 2500, 'codec': 'h264'}
animation_filename = 'gravely.out.mp4'


# To run gravely by executing this file, make it executable and use:
if __name__ == '__main__': from gravely.simulation import run; run(__file__)
'''


def autodetect(something):
    """Create a config 'Do-What-I-Mean' style, autoguessing what to do."""
    if something is None:
        return get_default()
    elif isinstance(something, str):
        if '\n' in something or '=' in something:
            # Probably configuration data, execute it
            return from_string(something)
        else:
            # Probably a configuration file path, read and execute it
            return from_path(something)
    elif isinstance(something, dict):
        config = get_default()
        config.__dict__.update(something)
        return config
    else:
        return something


def get_default():
    """Create a config by executing DEFAULT_CONFIG_STRING."""
    return from_string(DEFAULT_CONFIG_STRING, based_on={})


def from_path(filename=None, based_on=None):
    """Create a config by executing a file. See from_string."""
    if filename is None:
        return get_default()
    with open(filename) as config_file:
        return from_string(config_file.read(),
                           based_on=based_on, filename=filename)


def from_string(config_string, based_on=None, filename='<string>'):
    """Create a config from a string and optional dict. See get_default."""
    defaults = based_on if based_on is not None else get_default().__dict__
    code = compile(config_string, filename, 'exec')
    config = imp.new_module('config')
    config.__dict__.update(defaults)
    exec(code, config.__dict__)
    return config


def subset(config, *field_names):
    """Returns config (as a namedtuple instance) limited to specific fields."""
    subset_namedtuple = collections.namedtuple('ConfigSubset', field_names)
    values = (getattr(config, field_name) for field_name in field_names)
    return subset_namedtuple(*values)
