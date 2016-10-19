#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pyannote.parser import UEMParser, MDTMParser
import os.path as op


class EtapeSpeakerDiarizationProtocol(SpeakerDiarizationProtocol):

    def __init__(self, **kwargs):
        super(EtapeSpeakerDiarizationProtocol, self).__init__(**kwargs)
        self.uem_parser_ = UEMParser()
        self.mdtm_parser_ = MDTMParser()

    def _subset(self, protocol, subset):

        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')

        # load annotated parts
        # e.g. /data/{tv|radio|all}.{train|dev|test}.uem
        path = op.join(data_dir, '{protocol}.{subset}.uem'.format(subset=subset, protocol=protocol))
        uems = self.uem_parser_.read(path)

        # load annotations
        path = op.join(data_dir, '{protocol}.{subset}.mdtm'.format(subset=subset, protocol=protocol))
        mdtms = self.mdtm_parser_.read(path)

        for uri in sorted(uems.uris):
            annotated = uems(uri)
            annotation = mdtms(uri)
            current_file = {
                'uri': uri,
                'annotated': annotated,
                'annotation': annotation}
            yield current_file


class TV(EtapeSpeakerDiarizationProtocol):
    """Speaker diarization protocol using TV subset of ETAPE"""

    def trn_iter(self):
        return self._subset('tv', 'trn')

    def dev_iter(self):
        return self._subset('tv', 'dev')

    def tst_iter(self):
        return self._subset('tv', 'tst')


class Radio(EtapeSpeakerDiarizationProtocol):
    """Speaker diarization protocol using radio subset of ETAPE"""

    def trn_iter(self):
        return self._subset('radio', 'trn')

    def dev_iter(self):
        return self._subset('radio', 'dev')

    def tst_iter(self):
        return self._subset('radio', 'tst')


class Full(EtapeSpeakerDiarizationProtocol):
    """Speaker diarization protocol using ETAPE"""

    def trn_iter(self):
        return self._subset('all', 'trn')

    def dev_iter(self):
        return self._subset('all', 'dev')

    def tst_iter(self):
        return self._subset('all', 'tst')


class Debug(EtapeSpeakerDiarizationProtocol):
    """Speaker diarization protocol using ETAPE meant for debugging"""

    def trn_iter(self):
        return self._subset('debug', 'trn')

    def dev_iter(self):
        return self._subset('debug', 'dev')

    def tst_iter(self):
        return self._subset('debug', 'tst')



class Etape(Database):
    """ETAPE corpus

Reference
---------
"The ETAPE corpus for the evaluation of speech-based TV content processing in the French language"
Guillaume Gravier, Gilles Adda, Niklas Paulson, Matthieu Carré, Aude Giraudel, Olivier Galibert.
Eighth International Conference on Language Resources and Evaluation, 2012.

Citation
--------
@inproceedings{ETAPE,
  title = {{The ETAPE Corpus for the Evaluation of Speech-based TV Content Processing in the French Language}},
  author = {Gravier, Guillaume and Adda, Gilles and Paulson, Niklas and Carr{\'e}, Matthieu and Giraudel, Aude and Galibert, Olivier},
  booktitle = {{LREC - Eighth international conference on Language Resources and Evaluation}},
  address = {Turkey},
  year = {2012},
}

Website
-------
http://www.afcp-parole.org/etape-en.html
    """

    def __init__(self, **kwargs):
        super(Etape, self).__init__(**kwargs)

        self.register_protocol(
            'SpeakerDiarization', 'TV', TV)

        self.register_protocol(
            'SpeakerDiarization', 'Radio', Radio)

        self.register_protocol(
            'SpeakerDiarization', 'Full', Full)

        self.register_protocol(
            'SpeakerDiarization', 'Debug', Debug)
