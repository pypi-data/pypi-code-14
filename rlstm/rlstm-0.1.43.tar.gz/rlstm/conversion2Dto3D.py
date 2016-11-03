import os
import sys

import numpy as np

# Convert from the 2D data format (subjects x time points, observations) described here
# https://gist.github.com/michaelchughes/76336975162477dfb4b38ffd881da3d5
# to 3D data format (observations, time points, subjects)

def convert_single_patient_data(dir_name = 'physionet2014/1009'):
  import h5py
  times = {'train': 150000, 'test': 66000}
  suff = {'train' : '', 'test': '_val'}
  for data_type in ['train', 'test']:
    f = h5py.File(dir_name+'/data'+suff[data_type]+'.h5','r')
    x = np.transpose(f['obs'])
    x = x.reshape(6,times[data_type],1)
    np.save(dir_name+'_3D/X_'+data_type+'.npy',x)
    y = np.reshape(f['output'], (1,times[data_type],1))
    np.save(dir_name+'_3D/y_'+data_type+'.npy',y)
    f.close()

directory = sys.argv[1]
if not os.path.exists(directory+'_3D'):
  os.mkdir(directory+'_3D')

for data_type in ['train', 'test']:
    X = np.load(directory+'/X_'+data_type+'.npy')
    Y = np.load(directory+'/Y_'+data_type+'.npy')

    fence = np.load(directory+'/fenceposts_'+data_type+'.npy')
    max_time = max(fence[1:] - fence[:-1])
    num_subjects = len(fence)-1

    obs_set = np.zeros((X.shape[1], max_time, num_subjects))
    out_set = np.zeros((Y.shape[1], max_time, num_subjects))

    for i in range(num_subjects):
        time = fence[i+1] - fence[i]
        obs_set[:,:time,i] = X[fence[i]:fence[i+1]].transpose()
        out_set[:,:time,i] = Y[fence[i]:fence[i+1]].transpose()

    np.save(directory+'_3D/X_'+data_type, obs_set)
    np.save(directory+'_3D/y_'+data_type, out_set)
