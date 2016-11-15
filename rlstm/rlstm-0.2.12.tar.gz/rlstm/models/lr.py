import pdb
import autograd.numpy as np
import autograd.numpy.random as npr
from autograd import grad, value_and_grad

from rlstm.common_util import safe_log
from rlstm.nn_util import sigmoid, flatten_io, cross_entropy


def logistic_predictions(weights, input_set, fence_set, in_dim_count, out_dim_count):
    # input should be ( dims by data ) or vertical columns
    # Adds in the row of ones, so we don't have to when passing things in!
    # outputs probability of a label being true according to logistic model.

    # flatten but we already have flattened version in farray
    my_input_set = np.vstack((input_set, np.ones((1, input_set.shape[1]))))
    weights = np.reshape(weights, (out_dim_count, in_dim_count + 1))
    return sigmoid(np.dot(weights, my_input_set))


def logistic_log_predictions(weights, input_set, fence_set, in_dim_count, out_dim_count):
    return safe_log(logistic_predictions(weights, input_set, fence_set, in_dim_count, out_dim_count))


def log_likelihood(weights, input_set, fence_set, output_set):
    # Training loss is the negative log-likelihood of the training labels.
    in_dim_count = input_set.shape[0]
    out_dim_count = output_set.shape[0]
    pred_set = logistic_predictions(weights, input_set, fence_set, in_dim_count, out_dim_count)

    logpred_set1 = safe_log(pred_set)
    logpred_set0 = safe_log(1 - pred_set)

    ll = cross_entropy(output_set, logpred_set1, logpred_set0)
    return np.sum(ll)
