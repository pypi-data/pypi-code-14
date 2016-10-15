from __future__ import absolute_import, print_function

from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.weights_parser import WeightsParser
from rlstm.nn_util import sigmoid, add_bias_and_multiply
from rlstm.common_util import safe_log

def update(
        curr_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights,
        reset_x_weights,
        reset_h_weights,
        thidden_x_weights,
        thidden_h_weights):

    update = sigmoid(add_bias_and_multiply(update_x_weights, curr_input) +
                     np.dot(prev_hiddens, update_h_weights))
    reset = sigmoid(add_bias_and_multiply(reset_x_weights, curr_input) +
                    np.dot(prev_hiddens, reset_h_weights))
    thiddens = np.tanh(add_bias_and_multiply(thidden_x_weights, curr_input) +
                       np.dot(reset * prev_hiddens, thidden_h_weights))
    hiddens = (1 - update) * prev_hiddens + update * thiddens
    return hiddens


def hiddens_to_output_probs(hiddens, output_h_weights):
    # binary case, each a prob
    output = sigmoid(np.dot(hiddens, output_h_weights))
    # output - logsumexp( output ) # normalize log-probs (multinomial case)
    # <-- softmax
    return safe_log(output), safe_log(1 - output)


def build(input_count, state_count, output_count):
    # the input count is just the number of input dimensions, we
    # assume that any/all 1-hot encoding, etc. has been done already.
    # the output count is the *number* of *binary* outputs (no
    # multinomial or continuous support at the moment)

    parser = WeightsParser()
    parser.add_shape('init_hiddens', (1, state_count))
    parser.add_shape('update_x_weights', (input_count + 1, state_count))
    parser.add_shape('update_h_weights', (state_count, state_count))
    parser.add_shape('reset_x_weights', (input_count + 1, state_count))
    parser.add_shape('reset_h_weights', (state_count, state_count))
    parser.add_shape('thidden_x_weights', (input_count + 1, state_count))
    parser.add_shape('thidden_h_weights', (state_count, state_count))
    parser.add_shape('output_h_weights', (state_count, output_count))

    def outputs(weights, input_set):
        update_x_weights = parser.get(weights, 'update_x_weights')
        update_h_weights = parser.get(weights, 'update_h_weights')
        reset_x_weights = parser.get(weights, 'reset_x_weights')
        reset_h_weights = parser.get(weights, 'reset_h_weights')
        thidden_x_weights = parser.get(weights, 'thidden_x_weights')
        thidden_h_weights = parser.get(weights, 'thidden_h_weights')
        output_h_weights = parser.get(weights, 'output_h_weights')

        data_count = input_set.shape[2]
        time_count = input_set.shape[1]

        # the output set of dimension ( output_count, time_count, data_count )
        # output_set = np.zeros( ( output_count, time_count, data_count ) )
        for data_iter in range(data_count):
            hiddens = copy(parser.get(weights, 'init_hiddens'))
            for time_iter in range(time_count):
                hiddens = update(np.expand_dims(input_set[:, time_iter, data_iter], axis=0),
                                 hiddens, update_x_weights, update_h_weights,
                                 reset_x_weights, reset_h_weights,
                                 thidden_x_weights, thidden_h_weights)

                # output_set[:,time_iter,data_iter] = \
                #    hiddens_to_output_probs( hiddens, output_h_weights )
                # more convoluted way with hstack and vstack because
                # autograd does not support assigning with indices
                out_vec1, out_vec0 = hiddens_to_output_probs(
                    hiddens, output_h_weights)
                out_vec1 = np.transpose(out_vec1)
                out_vec0 = np.transpose(out_vec0)
                if time_iter == 0:
                    out_mat1 = out_vec1
                    out_mat0 = out_vec0
                else:
                    out_mat1 = np.hstack((out_mat1, out_vec1))
                    out_mat0 = np.hstack((out_mat0, out_vec0))

            if data_iter == 0:
                output_set1 = out_mat1
                output_set0 = out_mat0
            else:
                output_set1 = np.dstack((output_set1, out_mat1))
                output_set0 = np.dstack((output_set0, out_mat0))
        return output_set1, output_set0

    def log_likelihood(weights, input_set, output_set):
        lprobs1, lprobs0 = outputs(weights, input_set)
        lprobs = output_set * lprobs1 + (1 - output_set) * lprobs0
        ll = np.sum(lprobs)
        return ll

    return outputs, log_likelihood, parser.num_weights
