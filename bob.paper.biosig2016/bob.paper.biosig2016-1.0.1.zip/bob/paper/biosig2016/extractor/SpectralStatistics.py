#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
# Tue  9 Jun 23:10:43 CEST 2015
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

"""Cepstral Features for speaker recognition"""

import numpy as np
import math
import sys
import logging

from bob.bio.base.extractor import Extractor

logger = logging.getLogger("bob.paper.biosig2016")


class SpectralStatistics(Extractor):
  """ Extracts the Cepstral features """
  def __init__(
      self,
      win_length_ms=20,
      win_shift_ms=10,
      pre_emphasis_coef=0.95,
      log_flag=True,
      with_mean=True,
      with_std=True,
      hamming=True,
      normalize_flag=False,
      mean_removal_flag=True,
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Extractor.__init__(
        self,
        win_length_ms=win_length_ms,
        win_shift_ms=win_shift_ms,
        pre_emphasis_coef=pre_emphasis_coef,
        log_flag=log_flag,
        with_mean=with_mean,
        with_std=with_std,
        hamming=hamming,
        normalize_flag=normalize_flag,
        mean_removal_flag=mean_removal_flag,
    )
    # copy parameters
    self.win_length_ms = win_length_ms
    self.win_shift_ms = win_shift_ms
    self.pre_emphasis_coef = pre_emphasis_coef
    self.log_flag = log_flag
    self.normalize_flag = normalize_flag
    self.mean_removal_flag = mean_removal_flag
    self.with_mean = with_mean
    self.with_std = with_std
    self.hamming = hamming

  def preemphasis(self, x, pre):
    y = np.zeros(len(x))
    for i in range(len(x)):
      if i == 0:
        y[i] = x[i] * (1 - pre)
      else:
        y[i] = x[i] - pre * x[i - 1]
    return y

  def splitIntoFrames(self, samples, rate, wlS, wsS):
    N = len(samples)
    nbFrames = int(1 + math.floor((N - wlS - 1) / wsS))
    wlS = int(wlS)
    wsS = int(wsS)
    frames = np.zeros((nbFrames, wlS))
    # remove the average of each frame
    for i in range(nbFrames):
      if(self.mean_removal_flag):
        frames[i, :] = samples[i * wsS:i * wsS + wlS] - np.mean(samples[i * wsS:i * wsS + wlS])
      else:
        frames[i, :] = samples[i * wsS:i * wsS + wlS]
    return frames

  def hammingWindow(self, frame):
    w = np.hamming(len(frame))
    res = np.multiply(frame, w)
    return res

  def computePowerSpectrum(self, frame):
    N = int(np.power(2, math.ceil(np.log2(len(frame)))))
    frameFFT = np.fft.fft(frame, N)
    PowerSpectrum = np.absolute(frameFFT)[:N / 2]
    if self.log_flag:
      # floor values to 1+sys.float_info.min to have strictly positive value after log compression
      idx0 = np.argwhere(PowerSpectrum <= 1)
      PowerSpectrum[idx0] = 1 + sys.float_info.min
      c = np.log(PowerSpectrum)
    else:
      c = PowerSpectrum

    return c

  def computeFeatures(self, wavsample, rate, wl, ws, pre):
    wavsample = self.preemphasis(wavsample, pre)
    frames = self.splitIntoFrames(wavsample, rate, wl, ws)
    if (self.hamming):
        frames = np.apply_along_axis(self.hammingWindow, 1, frames)
    feature = np.apply_along_axis(self.computePowerSpectrum, 1, frames)
    return feature

  def __call__(self, input_data):
    """Computes and returns spectral statistics for the given input data
    input_data[0] --> sampling rate
    input_data[1] -->  sample data
    """
    rate = input_data[0]
    wavsample = input_data[1]

    # Set parameters
    wl = self.win_length_ms
    ws = self.win_shift_ms
    pre = self.pre_emphasis_coef

    # if the sample is too short, return ab array filled with zeros
    wlS = math.floor(rate * wl / 1000.0)
    wsS = math.floor(rate * ws / 1000.0)
    N = len(wavsample)
    nbFrames = int(1 + math.floor((N - wlS - 1) / wsS))
    if nbFrames <= 1:
      if (self.with_mean and self.with_std):
        return np.zeros(int(wlS))
      else:
        return np.zeros(int(wlS) / 2)

    # Compute features
    features = self.computeFeatures(wavsample, rate, wlS, wsS, pre)
    if(not self.with_mean and not self.with_std):
      logger.warn("Mean and standard deviation flags are set to zero, we compute the mean.")
      self.with_mean = True

    # compute the mean and normalize it if needed
    if(self.with_mean):
      mean = np.mean(features, axis=0)
      if self.normalize_flag:
        if(np.std(mean) != 0):
          mean = (mean - np.mean(mean)) / np.std(mean)
        else:
          mean = (mean - np.mean(mean))

    # compute the standard deviation and normalize it if needed
    if(self.with_std):
      std = np.std(features, axis=0)
      if self.normalize_flag:
        if(np.std(std) != 0):
          std = (std - np.mean(std)) / np.std(std)
        else:
          std = (std - np.mean(std))

    if(self.with_mean and self.with_std):
      return np.concatenate((mean, std))
    elif(self.with_std):
      return std
    elif(self.with_mean):
      return mean

    return None
