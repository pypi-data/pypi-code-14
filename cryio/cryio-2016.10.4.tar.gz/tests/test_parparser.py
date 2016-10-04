#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from cryio import parparser


class TestParParser(TestCase):
    def test(self):
        par = parparser.ParParser(os.path.join('data', 'cbf_cracker.par'))
        assert par.phiy == -0.03141
        assert par.phix == 0.08125
        assert par.phiz == 0.
        assert par.alpha == 50.
        assert par.beam_be == 0.07013
        assert par.beta == 0.
        assert par.cell_a == 6.24503
        assert par.cell_b == 6.24176
        assert par.cell_c == 6.23990
        assert par.cell_alpha == 89.98398
        assert par.cell_beta == 89.95934
        assert par.cell_gamma == 89.86260
        assert par.dist == 144.51605
        assert par.xc == 22.93184
        assert par.yc == 741.05727
        assert par.ub == [-0.0261901873361, 0.0897744425213, -0.0612837016967,
                          0.0670725999668, -0.036346698271, -0.0817602217447,
                          -0.0853802791413, -0.0557406015467, -0.0453264717691]
        assert par.wavelength == 0.69750
        assert par.omega0 == 0.08949
        assert par.kappa0 == 0.
        assert par.theta0 == -0.34437
        assert par.phi0 == 0.00000
        assert par.pixel == 0.172
        assert par.inhor == 1475
        assert par.inver == 1679
