# -*- coding: utf-8 -*-

import click
import pixel
import h5py
import numpy as np
import os
import hashlib
from backend import start_server
from time import sleep
import threading
import deepzoom

@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
  """Console script for pixel"""
  if os.path.isfile(path):
    _, file_extension = os.path.splitext(path)
    if file_extension in ['.h5','.hdf5']:
      exists, tmp_path = maybe_create_folder(path)
      if not exists:
        async_creation(path, tmp_path)
      start_server(tmp_path)
  else: #is a directory
    raise Exception("Pixel doesn't support folders yet") 

def read_h5(path):
  with h5py.File(path) as f:
    arr = f['main']
    return arr
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

def maybe_create_folder(path):
  """
  It creates a folder /tmp/{{hash}}
  where the hash is generated from the path
  and the modification time of the file that
  corresponds to the path
  """
  statbuf = os.stat(path)
  hash_object = hashlib.md5(path + str(statbuf.st_mtime) )
  hash_string = hash_object.hexdigest()
  directory = '/tmp/pixel-' + hash_string

  if os.path.exists(directory):
    return True, directory
  else:
    os.makedirs(directory)
    return False, directory

def _process_grayscale(arr_path, tmp_path):
  # Create Deep Zoom Image creator with weird parameters
  creator = deepzoom.ImageCreator(tile_format="jpg",
                                image_quality=0.8)
  
  with h5py.File(arr_path) as f:
    arr = f['main']
    for z in xrange(arr.shape[0]):
        creator.create(arr[z,:,:], "{}/{}.dzi".format(tmp_path,z))


def async_creation(arr_path , tmp_path):
  t1 = FuncThread(_process_grayscale, arr_path, tmp_path)
  t1.start()
 
class FuncThread(threading.Thread):
  def __init__(self, target, *args):
    self._target = target
    self._args = args
    threading.Thread.__init__(self)
 
  def run(self):
    self._target(*self._args)
    self.join()
    #TODO if it hasn't finish building all mip levels
    #delete folder such that next time we resume building
    #or use some other flag


if __name__ == "__main__":
    main()