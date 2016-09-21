#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Thu May 24 10:41:42 CEST 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bob.bio.base
import unittest
import os
import numpy
import bob.bio.caffe_face
from nose.plugins.skip import SkipTest
import bob.io.base.test_utils
from bob.bio.base.test import utils

import pkg_resources

regenerate_refs = False


def test_caffe_feature():
    # read input
    input_data = bob.io.base.load(
        os.path.join(pkg_resources.resource_filename("bob.ip.caffe_extractor", 'data'), '8821.hdf5'))

    reference = bob.io.base.load(
        os.path.join(pkg_resources.resource_filename("bob.ip.caffe_extractor", 'data'), 'reference.hdf5'))

    caffe_extractor = bob.bio.base.load_resource('vgg_features', 'extractor',
                                                       preferred_package='bob.bio.caffe_face')
    assert isinstance(caffe_extractor, bob.bio.caffe_face.extractor.VGGFeatures)
    assert not caffe_extractor.requires_training

    feature = caffe_extractor(input_data)
    assert numpy.any(numpy.isclose(feature, reference, rtol=1e-08, atol=1e-08))
