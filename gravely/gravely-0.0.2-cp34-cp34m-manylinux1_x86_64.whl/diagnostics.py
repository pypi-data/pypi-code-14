# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
Diagnostics output functionality for gravely.
"""

import h5py

from . import configuration
from .utils import progress


def animate(config):
    """Animated gravely output data from a HDF5 file."""
    config = configuration.autodetect(config)
    with h5py.File(config.data_filename) as f:
        # Read simulation results from the data file
        rs, substepping_depths = f['bodies']['r'], f['substepping_depths']
        # The simulation results file is the best source for its parameters:
        dt, diagnostics_period = f['dt'][()], f['diagnostics_period'][()]
        animate_data(config, rs, substepping_depths, dt, diagnostics_period)


def animate_data(config, rs, substepping_depths, dt, diagnostics_period):
    """Produces a video file with animated body trajectories."""

    config = configuration.subset(
        config,
        'animation_filename',
        'animation_writer',
        'animation_writer_parameters',
        'data_filename',
        'plot_colors',
        'plot_limits',
        'plot_markers',
        'plot_trail_length',
    )

    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import mpl_toolkits.mplot3d.axes3d as p3
    except ImportError:
        raise RuntimeError('matplotlib package is required for animations')

    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)  # FullHD, 1920x1080, 16:9
    axes = p3.Axes3D(fig)
    axes.set_xlim(config.plot_limits[0])
    axes.set_ylim(config.plot_limits[1])
    axes.set_zlim(config.plot_limits[2])

    lines, points = [], []
    for i in range(rs.shape[1]):
        color, marker = config.plot_colors[i], config.plot_markers[i]
        line = axes.plot(rs[0, :, 0], rs[0, :, 1], rs[0, :, 2],
                         color=color)[0]
        point = axes.plot(rs[0, :, 0], rs[0, :, 1], rs[0, :, 2],
                          color=color, marker=marker,
                          markerfacecolor='None')[0]
        lines.append(line)
        points.append(point)

    progress_bar = progress.Progress(max_value=rs.shape[0], text='frame 0')

    def update_animation(frame_i):
        """Updates the plots for the new frame. Frame numbers start from 0."""

        now = frame_i + 1
        trail_start = now - (config.plot_trail_length / diagnostics_period)
        trail_start = int(max(trail_start, 0))
        substepping_depth = substepping_depths[frame_i]
        time_days = now * diagnostics_period / (24 * 3600)
        axes.set_xlabel('t = %.1f days' % time_days)
        axes.set_ylabel('dt = %.4f s (%.1f s / %.1f)' % (
            dt / substepping_depth,
            dt,
            substepping_depth
        ))

        axes.yaxis.label.set_color(_substepping_color(substepping_depth))

        for j, line in enumerate(lines):
            # Display jth body coordinates from trail_start to now inclusive
            _set_3d_plot_data(line, rs[trail_start:now+1, j])

        for j, point in enumerate(points):
            # Display jth body coordinates at current moment
            _set_3d_plot_data(point, rs[now, j])

        progress_bar.update(frame_i, text=('frame %d' % now))

    anim = animation.FuncAnimation(fig, update_animation, interval=15,
                                   frames=(rs.shape[0] - 1))

    if isinstance(config.animation_writer, str):
        writer_class = animation.writers[config.animation_writer]
        writer = writer_class(**config.animation_writer_parameters)
    else:
        writer = config.animation_writer

    anim.save(config.animation_filename, writer=writer)

    progress_bar.finish(text='Animation completed')


def _set_3d_plot_data(plot, data):
    """Hide that plot.set_data doesn't work with 3D values."""
    plot.set_data(data[..., 0:2].T)         # set x and y
    plot.set_3d_properties(data[..., 2])    # set z values separately


def _substepping_color(substepping_depth):
    """Choose a color for the substepping depth text."""
    if substepping_depth >= 1000:
        return 'red'
    elif substepping_depth >= 100:
        return '#FF7700'  # orange
    elif substepping_depth >= 10:
        return 'green'
    else:
        return 'blue'
