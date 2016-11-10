import autograd.numpy as np
import autograd.numpy.random as npr
from autograd import grad, value_and_grad

from rlstm.common_util import safe_log
from rlstm.nn_util import sigmoid, flatten_io


def logistic_predictions(weights, input_farray, in_dim_count, out_dim_count):
    # input should be ( dims by data ) or vertical columns
    # Adds in the row of ones, so we don't have to when passing things in!
    # outputs probability of a label being true according to logistic model.

    # flatten but we already have flattened version in farray
    input_set = input_farray.array_2d
    my_input_set = np.vstack((input_set, np.ones((1, input_set.shape[1]))))
    weights = np.reshape(weights, (out_dim_count, in_dim_count + 1))
    return sigmoid(np.dot(weights, my_input_set))


def logistic_log_predictions(weights, input_farray, in_dim_count, out_dim_count):
    return np.log(logistic_predictions(weights, input_farray, in_dim_count, out_dim_count))


def log_likelihood(weights, input_farray, output_farray):
    # Training loss is the negative log-likelihood of the training labels.

    # flatten but we already have flattened version in farray
    input_set = input_farray.array_2d
    output_set = output_farray.array_2d

    in_dim_count = input_set.shape[0]
    out_dim_count = output_set.shape[0]
    preds = logistic_predictions(
        weights, input_farray, in_dim_count, out_dim_count)
    label_probabilities = safe_log(
        preds) * output_set + safe_log(1 - preds) * (1 - output_set)

    return np.sum(label_probabilities)
