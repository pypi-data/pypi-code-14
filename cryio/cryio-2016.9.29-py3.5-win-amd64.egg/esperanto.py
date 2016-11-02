#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
from datetime import datetime
import numpy as np
from . import templates, tools, _cryio, ImageError


class EsperantoException(ImageError):
    pass


class EsperantoImage:
    ESPERANTO_SIZE = 254  # -len('\r\n')

    def __init__(self, filepath=None):
        self.filepath = filepath
        self._capsule = _cryio.init_esp()
        self.array = None
        if self.filepath:
            self.parse()

    def parse(self):
        self.parse_header()
        self.parse_binary()

    def parse_header(self):
        pass

    def parse_binary(self):
        pass

    def save(self, filepath, array=None, pack=True, **kwargs):
        if array is None and self.array is None:
            raise EsperantoException('Nothing to save, an array is not provided')
        if array is None:
            array = self.array
        # crysalis reads only squared esperanto arrays with the x,x size divided by 4
        if array.shape[0] != array.shape[1] or array.shape[0] % 4 and array.shape[1] % 4:
            x = y = int(math.ceil(max(array.shape) / 4.0) * 4)
            array = tools.padArray(array, x, y)
        shape = array.shape[0]
        espstr = array.reshape((shape ** 2,)).astype(np.int32).tostring()
        datatype = '4BYTE_LONG'
        if pack:
            datatype = 'AGI_BITFIELD'
            espstr = _cryio.encode_esp(self._capsule, espstr)
        esp_header = {
            'shape': shape,
            'datetime': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            'datatype': datatype,
        }
        esp_header.update(kwargs)
        header = templates.env.get_template('esp').render(esp_header).splitlines()
        binblob = [bytes(l.ljust(self.ESPERANTO_SIZE).encode('ascii')) for l in header]
        with open(filepath, 'wb') as fedf:
            fedf.write(b'\r\n'.join(binblob))
            fedf.write(b'\r\n')
            fedf.write(espstr)
