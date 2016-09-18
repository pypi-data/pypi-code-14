#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tqdm import tqdm
import numpy as np
import deepzoom


# Create Deep Zoom Image creator with weird parameters
creator = deepzoom.ImageCreator(tile_format="png",
                                image_quality=1.0, 
                                resize_filter="nearest",
                                tile_size=1024,
                                tile_overlap=1)


import h5py
import scipy.misc
import StringIO

with h5py.File('/usr/people/it2/seungmount/research/datasets/blended_piriform_157x2128x2128/all/image.h5') as f:
  channel =  f['/main'][:]


with h5py.File('/usr/people/it2/seungmount/research/datasets/blended_piriform_157x2128x2128/all/human_labels.h5') as f:
  segmentation =  f['/main'][:]

  # print max(np.unique(segmentation))

img = segmentation + channel * 2**(8*3)
for z in tqdm(xrange(img.shape[0])):
  creator.create(img[z,:,:], "./piriform/{}.dzi".format(z))
