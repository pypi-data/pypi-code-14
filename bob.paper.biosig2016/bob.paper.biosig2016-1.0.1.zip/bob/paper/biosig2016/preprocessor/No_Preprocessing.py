#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
# Tue  9 Jun 16:56:01 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""{4Hz modulation energy and energy}-based voice activity detection for speaker recognition"""

import numpy
import logging

from bob.bio.spear.preprocessor.Base import Base
from bob.bio.base.preprocessor import Preprocessor

logger = logging.getLogger("bob.paper.biosig2016")


class No_Preprocessing(Base):
  """VAD based on the modulation of the energy around 4 Hz and the energy """
  def __init__(
      self,
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Preprocessor.__init__(
        self,
    )

  def __call__(self, input_signal, annotations=None):
    """labels speech (1) and non-speech (0) parts of the given input wave file using 4Hz modulation energy and energy
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal
    """
    rate = input_signal[0]
    data = input_signal[1]
    labels = numpy.ones(len(data))
#   returns data as it is, i.e., no preprocessing.
    return rate, data, labels
