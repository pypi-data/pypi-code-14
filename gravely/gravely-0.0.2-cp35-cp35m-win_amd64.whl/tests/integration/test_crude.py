# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

import atexit
import os
import tempfile

import h5py

from gravely.simulation import run


TEST_STRING_TEMPLATE = """
t_max = 3600 * 24 * 27.3
dt = 3600
substepping_max_depth = 100
diagnostics_period = 3600
data_filename = r'%s'
"""


def test_crude():
    data_file = tempfile.NamedTemporaryFile(delete=False)
    atexit.register(os.unlink, data_file.name)
    data_file.close()

    config_file = tempfile.NamedTemporaryFile(delete=False)
    atexit.register(os.unlink, config_file.name)
    config_string = TEST_STRING_TEMPLATE % data_file.name
    config_file.write(config_string.encode())
    config_file.close()

    run(config_file.name)
    
    with h5py.File(data_file.name) as hf:
        assert hf['dt'][()] == 3600
        assert hf['diagnostics_period'][()] == 3600
        bodies, substepping_depths = hf['bodies'], hf['substepping_depths']
        assert len(bodies) == len(substepping_depths)
        assert 24 * 27 < len(bodies) < 24 * 28
        assert len(bodies[0]) == 2

        # Z coordinate (2) of all bodies (second :) were always (first :) 0
        assert (bodies['r'][:, :, 2] == 0).all()

        # All coordinates (last :) of Earth (0) were less than 1e9
        # for all time(first :)
        assert (bodies['r'][:, 0, :] < 1e9).all()

        # Moon (1) was close to the starting point at the last moment (-1)
        moon_final_r = bodies['r'][-1, 1, :]
        assert 3.8e10 < moon_final_r[0] < 3.9e10
        assert -5e9 < moon_final_r[1] < 5e9
