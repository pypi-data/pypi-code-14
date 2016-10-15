from copy import copy

import rlstm.residual_lstm as model
from rlstm import create_toy_data
from rlstm.distillation import grudistill
from rlstm.cross_validation import split_dataset
from rlstm.early_stopping.optimize import adam

import autograd.numpy as np
from autograd import value_and_grad, grad

input_count = 7
state_count = 10
output_count = 2

def train_grudistill(   obs_set, soft_out_set , state_count , true_out_set=None ,
                        temperature=1 , init_weights=None , train_iters=500 ,
                        batch_size=5 , patience=50 , early_stop_freq=1 ):
    input_count = obs_set.shape[0]
    output_count = soft_out_set.shape[0]
    param_scale = 0.01

    # Build the model
    pred_fun, loglike_fun, num_weights = grudistill.build_grudistill(
        input_count , state_count , output_count )

    ids_set = np.expand_dims( np.arange( obs_set.shape[1] ) , axis = 0)
    # split into a validation set
    (tr_obs_set , va_obs_set ) , ( tr_ids_set , va_ids_set ) = split_dataset( obs_set , ids_set , frac=0.80)
    tr_soft_out_set , va_soft_out_set = soft_out_set[:, tr_ids_set[0]] , soft_out_set[:, va_ids_set[0]]
    if not true_out_set is None:
        tr_true_out_set , va_true_out_set = true_out_set[:, tr_ids_set[0]] , true_out_set[:, va_ids_set[0]]

    num_batches = int( np.ceil ( tr_obs_set.shape[1] / float( batch_size ) ) )
    if init_weights is None:
        init_weights = np.random.randn(num_weights) * param_scale

    def batch_indices(iter):
        idx = iter % num_batches
        return slice(idx * batch_size, (idx+1) * batch_size)

    def tr_batch_loss(weights, iter):
        idx = batch_indices(iter)
        return -1 * loglike_fun( weights , tr_obs_set[:, idx] , tr_soft_out_set[:, idx] ,
                                 true_output_set=None if true_out_set is None else tr_true_out_set[:, idx] ,
                                 temperature=temperature )

    def va_loss(weights):
        return -1 * loglike_fun( weights , va_obs_set , va_soft_out_set ,
                                 true_output_set=None if true_out_set is None else va_true_out_set ,
                                 temperature=temperature )

    def callback( xk , i , gv ):
        if i % early_stop_freq == 0:
            print( '({}) batch loss [tr] {} , loss [va] {} '.format( i , tr_batch_loss( xk , i ) , va_loss( xk ) ) )
        else:
            print( '({}) batch loss [tr] {} '.format( i , tr_batch_loss( xk , i ) ) )

    def tempered_tr_grad( x , i ):
        # gradient adjusted for temperature
        f = grad( tr_batch_loss )
        return f( x , i) * temperature**2

    tr_grad , va_grad = tempered_tr_grad , value_and_grad( va_loss )
    weights = adam( tr_grad, init_weights, step_size=0.001, max_iters=train_iters,
                    callback=callback , validation_grad=va_grad , patience=patience ,
                    early_stop_freq=early_stop_freq )

    return pred_fun, loglike_fun, weights

# step 0 : parameters
time_count  = 50
cumbersome_state_count = 100
distilled_state_count  = 10
temperature = 4

# step 1 : make initial data set
train_data_count = 25
test_data_count  = 10
obs_set, out_set, param_set = create_toy_data.create_toy_data(
    train_data_count + test_data_count , time_count,
    bias_mat   = np.array( [ 15, 15] ),
    weight_mat = np.array( ( [ 10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0 ], \
                            [ 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0 ] ) ) )

train_obs_set = obs_set[ :, :, 0:train_data_count ]
train_out_set = out_set[ :, :, 0:train_data_count ]
test_obs_set  = obs_set[ :, :, train_data_count: ]
test_out_set  = out_set[ :, :, train_data_count: ]

# step 2 : train a cumbersome model
cumbersome_pred_fun , cumbersome_ll_fun , cumbersome_weights = train_grudistill(
    train_obs_set, train_out_set , cumbersome_state_count , temperature=temperature ,
    init_weights=None , train_iters=10000 , batch_size=5 , patience=50 , early_stop_freq=5 )

# step 3 : create a large data set
# easy for us to munge a big dataset
# use real munge algo when we get continuous data
munged_train_data_count = 250
munged_test_data_count  = 100
munged_obs_set, munged_out_set, _ = create_toy_data.create_toy_data(
    munged_train_data_count + munged_test_data_count , time_count,
    bias_mat = np.array( [ 15, 15] ),
    weight_mat = np.array( ( [ 10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0 ], \
                            [ 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0 ] ) ) )

munged_train_obs_set = munged_obs_set[ :, :, 0:munged_train_data_count ]
munged_train_out_set = munged_out_set[ :, :, 0:munged_train_data_count ]
munged_test_obs_set  = munged_obs_set[ :, :, munged_train_data_count: ]
munged_test_out_set  = munged_out_set[ :, :, munged_train_data_count: ]

# step 4 : make predictions using cumbersome
munged_train_pred_set = cumbersome_pred_fun( cumbersome_weights , munged_train_obs_set )[0]

# step 5 : train the distilled model
# add more iters because little fear of overfitting
distilled_pred_fun , distilled_ll_fun , distilled_weights = train_grudistill(
    munged_train_obs_set, np.exp( munged_train_pred_set ) , distilled_state_count ,
    true_out_set=munged_train_out_set , temperature=temperature ,
    init_weights=None , train_iters=20000 , batch_size=5 , patience=50 , early_stop_freq=5 )

# step 6 : check the loglikelihoods for both models on the munged data set
cumbersome_ll_fun( cumbersome_weights , munged_train_obs_set , munged_train_out_set )
cumbersome_ll_fun( cumbersome_weights , munged_test_obs_set , munged_test_out_set )

# set temperature back to 1 after training the distilled model
distilled_ll_fun( distilled_weights , munged_train_obs_set , munged_train_out_set , temperature=1 )
distilled_ll_fun( distilled_weights , munged_test_obs_set , munged_test_out_set , temperature=1 )

# step 7 : check the loglikelihoods for both models on the original data set
cumbersome_ll_fun( cumbersome_weights , train_obs_set , train_out_set )
cumbersome_ll_fun( cumbersome_weights , test_obs_set , test_out_set )

distilled_ll_fun( distilled_weights , train_obs_set , train_out_set , temperature=1 )
distilled_ll_fun( distilled_weights , test_obs_set , test_out_set , temperature=1 )
