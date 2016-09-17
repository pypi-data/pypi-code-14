# -*- coding: utf-8 -*-

import click
import pixel
import h5py
import numpy as np
import os

@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
  """Console script for pixel"""
  if os.path.isfile(path):
    _, file_extension = os.path.splitext(path)
    if file_extension in ['.h5','.hdf5']:
      display_h5(path)
  else: #is a directory
    raise Exception("Pixel doesn't support folders yet") 

def display_h5(path):
  with h5py.File(path) as f:
    arr = f['main']
    if len(arr.shape) == 3:
      if arr.dtype == np.uint8:
        pixel.display_grayscale(arr)
      if arr.dtype == np.uint32:
        pixel.display_segmentation(arr)
    elif (len(arr.shape) == 4 
          and arr.shape[0] == 3
          and arr.dtype == np.float32):
        pixel.display_affinities(arr)
    else:
      raise ValueError("Do not know how to display array with shape {} of type {}"
                       .format(arr.shape, arr.dtype))

if __name__ == "__main__":
    main()
