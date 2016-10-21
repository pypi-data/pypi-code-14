import numpy as np
from copy import copy
from rlstm.compression.munge import munge
from rlstm import create_toy_data
from rlstm.models import gru

input_count = 7
state_count = 10
output_count = 2

weights = cPickle.load(open('../weights/wdict3.pkl', 'rb'))
gru_weights = weights['gru']

pred_fun, loglike_fun, num_weights = gru.build(
    input_count, state_count, output_count)

# easy for us to munge a big dataset
# use real munge algo when we get continuous data
munged_obs_set, _, _ = create_toy_data.create_toy_data(
    1000, time_count,
    bias_mat=np.array([15, 15]),
    weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                         [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0])))

munged_out_set = pred_fun(gru_weights, munged_obs_set)

munged_pred_fun, munged_loglike_fun, munged_weights = model.train_gru(
    munged_obs_set, munged_out_set, 2, init_weights=None,
    train_iters=2000, batch_size=10, patience=50)

# this should be really close to 0
munged_loglike_fun(munged_weights, munged_obs_set, munged_out_set)

# this should be better than just gru's
test_obs_set = np.load('../weights/test_obs_set.npy')
test_out_set = np.load('../weights/test_out_set.npy')
munged_loglike_fun(munged_weights, test_obs_set, test_out_set)
