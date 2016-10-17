import autograd.numpy as np
import autograd.numpy.random as npr
from autograd import grad, value_and_grad

from rlstm.common_util import safe_log, normalize, my_dstack
from rlstm.nn_util import sigmoid


def flatten_io(input_set, output_set=None):
    in_dim_count = input_set.shape[0]
    input_set = np.reshape(input_set, (in_dim_count, -1))
    if output_set is None:
        return input_set
    else:
        out_dim_count = output_set.shape[0]
        output_set = np.reshape(output_set, (out_dim_count, -1))
        return input_set, output_set


def logistic_predictions(weights, input_set, in_dim_count, out_dim_count):
    # input should be ( dims by data ) or vertical columns
    # Adds in the row of ones, so we don't have to when passing things in!
    # outputs probability of a label being true according to logistic model.
    if len(input_set.shape) > 2:
        input_set = flatten_io(input_set)
    my_input_set = np.vstack((input_set, np.ones((1, input_set.shape[1]))))
    weights = np.reshape(weights, (out_dim_count, in_dim_count + 1))
    return sigmoid(np.dot(weights, my_input_set))


def log_likelihood(weights, input_set, output_set, debug=False):
    # Training loss is the negative log-likelihood of the training labels.
    if len(input_set.shape) > 2:
        input_set, output_set = flatten_io(input_set, output_set)
    in_dim_count = input_set.shape[0]
    out_dim_count = output_set.shape[0]
    preds = logistic_predictions(
        weights, input_set, in_dim_count, out_dim_count)
    label_probabilities = safe_log(
        preds) * output_set + safe_log(1 - preds) * (1 - output_set)
    if debug:
        return np.sum(label_probabilities), label_probabilities
    return np.sum(label_probabilities)
