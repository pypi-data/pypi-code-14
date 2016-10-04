# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
The high-level simulation code.
"""

import h5py
import numpy as np

from . import body
from . import configuration
from . import solver
from .utils import progress


def run(config):
    """Perform a simulation: repeatedly call solver to evolve bodies' state."""
    config = configuration.autodetect(config)
    solver_config = solver.SolverConfig(config)
    config = configuration.subset(
        config,
        'bodies',
        'data_filename',
        'diagnostics_period',
        'dt',
        't_max',
    )

    bodies = body.BodyArray(config.bodies)
    moved = np.empty_like(bodies)

    with h5py.File(config.data_filename, 'w') as f:
        f['dt'], f['diagnostics_period'] = config.dt, config.diagnostics_period
        bodies_dataset = f.create_dataset('bodies',
                                          shape=(0, len(bodies)),
                                          maxshape=(None, len(bodies)),
                                          dtype=body.dtype,
                                          compression='gzip', shuffle=True)
        depths_dataset = f.create_dataset('substepping_depths',
                                          shape=(0,),
                                          maxshape=(None,),
                                          dtype='f')

        step_depths = []
        prev_diagnostics_time = 0
        diagnostics_steps = 0

        time_steps = round(config.t_max / config.dt)
        progress_bar = progress.Progress(max_value=time_steps, text='0.0h')

        for time_step_i in range(time_steps):
            time = time_step_i * config.dt
            depth = solver.move_bodies_with_substepping(solver_config, bodies,
                                                        out=moved)
            step_depths.append(depth)
            bodies, moved = moved, bodies
            progress_bar.update(time_step_i)

            if time - prev_diagnostics_time >= config.diagnostics_period:
                diagnostics_steps += 1
                avg_depth = sum(step_depths) / len(step_depths)
                step_depths = []
                prev_diagnostics_time = time

                bodies_dataset.resize(diagnostics_steps, axis=0)
                bodies_dataset[-1, :] = bodies

                depths_dataset.resize(diagnostics_steps, axis=0)
                depths_dataset[-1] = avg_depth

                time_hours = time / 3600
                progress_bar.update(time_step_i, text=('%.1fh' % time_hours))

        progress_bar.finish(text='Simulation completed')
