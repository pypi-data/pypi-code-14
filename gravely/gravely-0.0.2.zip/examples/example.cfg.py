#!/usr/bin/python3
"""This is an example configuration file for 'gravely' gravity simulator."""

# To use a custom gravely installation, use:
#import sys; sys.path.append('/path/to/custom/gravely_directory')                                        
from gravely.body import Body
from gravely.units import g, kg, cm, m, km, sec, hour, day


MOON_PERIOD = 27.3 * day
t_max = MOON_PERIOD / 2
dt = 100 * sec
substepping_max_depth = 100000
substepping_target_acceleration = 1 * cm / sec**2 / dt
diagnostics_period = 1 * hour

EARTH_MASS = 5.9721e24 * kg
MOON_MASS = 7.3459e22 * kg
MOON_ORBIT_RADIUS = 384400 * km
MOON_ORBIT_VELOCITY = 1.022 * km / sec

EARTH = Body(m=EARTH_MASS)
MOON = Body(m=MOON_MASS, x=MOON_ORBIT_RADIUS, vy=-MOON_ORBIT_VELOCITY)
ANTIMOON1 = Body(m=MOON_MASS/2, x=-MOON_ORBIT_RADIUS, vy=MOON_ORBIT_VELOCITY,
                 z=+1e9, vx=-2.3e5*0.1)
ANTIMOON2 = Body(m=MOON_MASS/2, x=-MOON_ORBIT_RADIUS, vy=MOON_ORBIT_VELOCITY,
                 z=-1e9, vx=+2.3e5*0.1)
PROBES = (
    Body(m=100, x=6.4e8, vx=7.7581e5, vy=-7.9e5, probe=True),   # coil
    Body(m=100, x=6.4e8, vx=7.7625e5, vy=-7.9e5, probe=True),   # curve

    Body(m=100, x=6.4e8, vx=8.5730e5, vy=-7.0e5, probe=True),   # coil
    Body(m=100, x=6.4e8, vx=8.5800e5, vy=-7.0e5, probe=True),   # curve
)
bodies = (EARTH, MOON, ANTIMOON1, ANTIMOON2) + PROBES

data_filename = 'gravely.out.hdf5'

plot_limits = ((-4e10, 4e10),) * 3
plot_colors = ('black', 'green', 'cyan', 'red', '#ff7700', 'magenta', 'black', 'blue')
plot_markers = 'Do**....'
plot_trail_length = 1 * day

animation_writer = 'ffmpeg'
animation_writer_parameters = {'fps': 60, 'bitrate': 2500, 'codec': 'h264'}
animation_filename = 'gravely.out.mp4'


# To run gravely by executing this file, make it executable and use:
if __name__ == '__main__': from gravely.simulation import run; run(__file__)
