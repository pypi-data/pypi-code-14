import dask.array as da
import dask.bytes as db

import numpy as np

import netCDF4

file='/home/laliberte/CDB/2.0/sea_ice_landfast/'

dataset=netCDF4.Dataset(file)
x = da.from_array(dataset.variables['usi'],chunks=1000)
print(x.shape)
