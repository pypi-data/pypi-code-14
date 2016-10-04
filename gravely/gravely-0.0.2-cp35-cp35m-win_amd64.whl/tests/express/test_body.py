# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

import numpy as np

from gravely.body import Body, BodyArray


def test_body_instantiation():
    b = Body(m=100, x=2, vx=4)
    # Body gets converted to a dict in pythonland
    assert b['m'] == 100
    assert b['r'] == [2, 0, 0]
    assert b['v'] == [4, 0, 0]


def test_body_array():
    b1 = Body(m=100, x=2, vx=4)
    b2 = Body(m=50, y=-1, vy=-2)
    b = BodyArray((b1, b2))
    assert isinstance(b, np.ndarray)
    assert b[0]['m'] == 100
    assert np.array_equal(b[0]['r'], [2, 0, 0])
    assert np.array_equal(b[0]['v'], [4, 0, 0])
    assert b[1]['m'] == 50
    assert np.array_equal(b[1]['r'], [0, -1, 0])
    assert np.array_equal(b[1]['v'], [0, -2, 0])
    assert np.array_equal(b['m'], [100, 50])
    assert np.array_equal(b['r'], [[2, 0, 0], [0, -1, 0]])
    assert np.array_equal(b[0]['v'] + b[1]['v'], [4, -2, 0])
