# -*- coding: utf-8 -*-
"""
Stream statistics classes.

Created by phillip on 11/16/2016
"""
from __future__ import absolute_import

from cable_modem_stats.utils import strip_float


class Stream(object):
    def __init__(self, name, cid=None, freq=None, power=None, modulation=None):
        """
        Represents a modem channel

        :param name: the name of this channel
        :param cid: the DCID or UCID
        :param freq: the frequency, in MHz, that this channel operates on
        :param power: the power of the signal measured in dBmV
        :param modulation: the modulation of this stream
        """
        self.name = name
        self.cid = cid
        self.freq = strip_float(freq)
        self.power = strip_float(power)
        self.modulation = modulation

    def __str__(self):
        return "'{name}' {cid} {freq} MHz {power} dBmV {modulation}".format(**self.__dict__)


class Downstream(Stream):
    def __init__(self, name, cid=None, freq=None, power=None, modulation=None, snr=None, octets=None,
                 correcteds=None, uncorrectables=None):
        """
        A downstream channel

        :param snr: the signal-to-noise ratio in dB
        :param octets: octets count
        :param correcteds: correcteds count
        :param uncorrectables: uncorrectables count
        """
        super(self.__class__, self).__init__(name, cid=cid, freq=freq, power=power, modulation=modulation)
        self.snr = strip_float(snr)
        self.octets = octets
        self.correcteds = correcteds
        self.uncorrectables = uncorrectables

    def __str__(self):
        return "Downstream {super} {snr} dB {octets} {correcteds} {uncorrectables}".format(
            super=super(self.__class__, self).__str__(), **self.__dict__
        )


class Upstream(Stream):
    def __init__(self, name, cid, freq, power, modulation, channel_type, symbol_rate):
        """
        An upstream channel

        :param channel_type: the type of the channel like TDMA and DOCSIS version
        :param symbol_rate: the rate of symbols sent in kiloSymbols per second (kSym/s)
        """
        super(self.__class__, self).__init__(name, cid=cid, freq=freq, power=power, modulation=modulation)
        self.channel_type = channel_type
        self.symbol_rate = strip_float(symbol_rate)

    def __str__(self):
        return "Upstream {super} {channel_type} {symbol_rate} kSym/s".format(
            super=super(self.__class__, self).__str__(), **self.__dict__
        )
