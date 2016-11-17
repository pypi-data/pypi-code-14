#!/usr/bin/env python
# encoding: utf-8
#
# maskbit.py
#
# Created by José Sánchez-Gallego on 16 Nov 2016.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from collections import OrderedDict


class MaskType(OrderedDict):

    def __init__(self, name, datatype, maskbits):

        self.name = name
        self.datatype = datatype
        OrderedDict.__init__(self, [(xx[0], (xx[1], xx[2])) for xx in maskbits])

manga_target1 = MaskType(
    'manga_target1', 64,
    ((0, 'NONE', ''),
     (1, 'PRIMARY_PLUS_COM', 'March 2014 commissioning'),
     (2, 'SECONDARY_COM', 'March 2014 commissioning'),
     (3, 'COLOR_ENHANCED_COM', 'March 2014 commissioning'),
     (4, 'PRIMARY_v1_1_0', 'First tag, August 2014 plates'),
     (5, 'SECONDARY_v1_1_0', 'First tag, August 2014 plates'),
     (6, 'COLOR_ENHANCED_v1_1_0', 'First tag, August 2014 plates'),
     (7, 'PRIMARY_COM2', 'July 2014 commissioning'),
     (8, 'SECONDARY_COM2', 'July 2014 commissioning'),
     (9, 'COLOR_ENHANCED_COM2', 'July 2014 commissioning'),
     (10, 'PRIMARY_v1_2_0', ''),
     (11, 'SECONDARY_v1_2_0', ''),
     (12, 'COLOR_ENHANCED_v1_2_0', ''),
     (13, 'FILLER', 'Filler targets'),
     (14, 'RETIRED', 'Bit retired from use')))


class MaskBit(object):

    def __init__(self, maskbit, flag, datatype=None):

        self.maskbit = maskbit
        self.flag = flag
        self.datatype = datatype

    def get_dict(self):
        """Returns a dictionary with the active bits in ``maskbit``.

        The value for each key in the dictionary is a tuple containing label
        and description for the bit.

        """

        pass

    def bits(self):
        """Returns a tuple of active bits in ``maskbit``."""

        return tuple([ii for ii in range(self.datatype) if self.maskbit & 1 << ii])

    def labels(self):
        pass

    @classmethod
    def list_bits(self, flag):
        pass
