#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @author: Pavel Korshunov <pavel.korshunov@idiap.ch>
# @author: Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
# @date: Wed 19 Aug 13:43:21 2015
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

import bob.io.base
import os
import random
import logging

from .FileSelector import FileSelector
from bob.pad.base.tools.extractor import read_features
from bob.bio.base import utils

logger = logging.getLogger("bob.paper.biosig2016")


def train_projector(algorithm, extractor, force=False):
    """Trains the feature projector using extracted features of the ``'train'`` group, if the algorithm requires projector training.

    This function should only be called, when the ``algorithm`` actually requires projector training.
    The projector of the given ``algorithm`` is trained using extracted features.
    It writes the projector to the file specified by the :py:class:`bob.pad.base.tools.FileSelector`.
    By default, if the target file already exist, it is not re-created.

    **Parameters:**

    algorithm : py:class:`bob.pad.base.algorithm.Algorithm` or derived
      The algorithm, in which the projector should be trained.

    extractor : py:class:`bob.bio.base.extractor.Extractor` or derived
      The extractor, used for reading the training data.

    force : bool
      If given, the projector file is regenerated, even if it already exists.
    """
    if not algorithm.requires_projector_training:
        logger.warn("The train_projector function should not have been called, "
                    "since the algorithm does not need projector training.")
        return

    # the file selector object
    fs = FileSelector.instance()

    if utils.check_file(fs.projector_file, force, 1000):
        logger.info("- Projection: projector '%s' already exists.", fs.projector_file)
    else:
        bob.io.base.create_directories_safe(os.path.dirname(fs.projector_file))
        # train projector
        logger.info("- Projection: loading training data")
        train_files = fs.training_list('extracted', 'train_projector')
        train_features = read_features(train_files, extractor)
        logger.info("- Projection: training projector '%s' using %d training files: ", fs.projector_file,
                    len(train_files))

        # perform training
        dev_files = fs.feature_list_splitted(groups="dev")
        dev_features = read_features_dev(dev_files, extractor)
        algorithm.train_projector(train_features, dev_features, fs.projector_file)


def read_features_dev(file_names, extractor):
  """read_features(file_names, extractor, split_by_client = False) -> extracted

  Reads the extracted features from ``file_names`` using the given ``extractor``.
  If ``split_by_client`` is set to ``True``, it is assumed that the ``file_names`` are already sorted by client.

  **Parameters:**

  file_names : [str] or [[str]]
    A list of names of files to be read.
    If ``split_by_client = True``, file names are supposed to be split into groups.

  extractor : py:class:`bob.pad.base.extractor.Extractor` or derived
    The extractor, used for reading the extracted features.

  **Returns:**

  extracted : [object] or [[object]]
    The list of extracted features, in the same order as in the ``file_names``.
  """
  attack_files = file_names[1]
  real_files = file_names[0]
  random.seed(4)
  random.shuffle(real_files)
  random.shuffle(attack_files)
  real_files = real_files[0:len(real_files) / 4]
  attack_files = attack_files[0:len(attack_files) / 4]
  return [[extractor.read_feature(str(f)) for f in real_files], [extractor.read_feature(str(f)) for f in attack_files]]
