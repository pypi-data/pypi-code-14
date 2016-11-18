#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import _cryio


class CCP4Image:
    def __init__(self, par):
        self._par = par
        self._ccp4_ = _cryio.init_ccp4(self._par.parbuf())

    def ccp4(self, array, angle, osc):
        _cryio.cbf2ccp4(self._ccp4_, array, angle, osc)

    def cbf2ccp4(self, cbfheader):
        self.ccp4(cbfheader.cbf_str, cbfheader.header['Start_angle'], cbfheader.header['Angle_increment'])

    def save_map(self, filepath):
        header, body = _cryio.get_ccp4_map(self._ccp4_)
        with open(filepath, 'wb') as f:
            f.write(header)
            f.write(body)
