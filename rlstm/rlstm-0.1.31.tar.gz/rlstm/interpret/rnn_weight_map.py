""" Given sparse trained weights from a recursive neural
    network, it might be possible to interpret the network's
    decision function by seeing which inputs cause each
    gate to fire.

    In the classic GRU, there are 3 gates:

    z = sigmoid(x_t*U^z + s_(t-1)W^z)
    r = sigmoid(x_t*U^r + s_(t-1)W^r)
    h = tanh(x_t*U^h + (s_(t-1) dot r)W^h)
    s_t = (1-z) dot h + z dot s_(t-1)
    y_t = sigmoid(s_t*U^o)

    If we are able to train a simple, interpretable model
    like linear regression to see which inputs most align
    with a particular gate turning on, then we can draw
    conclusions about the effects of each gate on the hidden
    variables and the output.

    TODO : make work for any RNN.
"""


from __future__ import absolute_import, print_function

import numpy as np
from copy import copy
import seaborn as sns
import matplotlib.pyplot as plt
from rlstm.common_util import safe_log, wrapper_func
from rlstm.nn_util import flatten_io, sigmoid, add_bias_and_multiply
from rlstm.weights_parser import WeightsParser
from sklearn.linear_model import LinearRegression

def update(curr_input,
           prev_hiddens,
           update_x_weights,
           update_h_weights,
           reset_x_weights,
           reset_h_weights,
           thidden_x_weights,
           thidden_h_weights):
    ''' Return the gate results after squashing (no rounding) '''

    update = sigmoid(add_bias_and_multiply(update_x_weights, curr_input) +
                     np.dot(prev_hiddens, update_h_weights))
    reset = sigmoid(add_bias_and_multiply(reset_x_weights, curr_input) +
                    np.dot(prev_hiddens, reset_h_weights))
    thiddens = np.tanh(add_bias_and_multiply(thidden_x_weights, curr_input) +
                       np.dot(reset * prev_hiddens, thidden_h_weights))
    hiddens = (1 - update) * prev_hiddens + update * thiddens
    return (update, reset, thiddens, hiddens)


def build(input_count, state_count, output_count):
    # weights of the GRU and of the LinReg have to be stored
    # in the parser.

    parser = WeightsParser()
    # gru weights
    parser.add_shape('init_hiddens', (1, state_count))
    parser.add_shape('update_x_weights', (input_count + 1, state_count))
    parser.add_shape('update_h_weights', (state_count, state_count))
    parser.add_shape('reset_x_weights', (input_count + 1, state_count))
    parser.add_shape('reset_h_weights', (state_count, state_count))
    parser.add_shape('thidden_x_weights', (input_count + 1, state_count))
    parser.add_shape('thidden_h_weights', (state_count, state_count))
    parser.add_shape('output_h_weights', (state_count, output_count))

    def generate(weights, input_set):
        ''' Given trained weights, generate a dataset of (input, gate)
            for each input and each gate
        '''

        # grab weights from the parser
        update_x_weights = parser.get(weights, 'update_x_weights')
        update_h_weights = parser.get(weights, 'update_h_weights')
        reset_x_weights = parser.get(weights, 'reset_x_weights')
        reset_h_weights = parser.get(weights, 'reset_h_weights')
        thidden_x_weights = parser.get(weights, 'thidden_x_weights')
        thidden_h_weights = parser.get(weights, 'thidden_h_weights')
        output_h_weights = parser.get(weights, 'output_h_weights')

        data_count = input_set.shape[2]
        time_count = input_set.shape[1]

        ugate_set = np.zeros((state_count, time_count, data_count))
        rgate_set = np.zeros((state_count, time_count, data_count))
        tgate_set = np.zeros((state_count, time_count, data_count))

        for data_iter in range(data_count):
            hiddens = copy(parser.get(weights, 'init_hiddens'))
            for time_iter in range(time_count):
                cur_input_set = np.expand_dims(input_set[:, time_iter, data_iter], axis=0)
                u_gate, r_gate, t_gate, hiddens = update(cur_input_set,
                                                         hiddens,
                                                         update_x_weights,
                                                         update_h_weights,
                                                         reset_x_weights,
                                                         reset_h_weights,
                                                         thidden_x_weights,
                                                         thidden_h_weights)
                ugate_set[:, time_iter, data_iter] = u_gate.flatten()
                rgate_set[:, time_iter, data_iter] = r_gate.flatten()
                tgate_set[:, time_iter, data_iter] = t_gate.flatten()

        output_set = np.vstack((ugate_set, rgate_set, tgate_set))
        return output_set

    return generate

def train_map(obs_set,
              rnn_state_count,
              output_count,
              rnn_weights):

    input_count = obs_set.shape[0]
    gen_fun = build(input_count, rnn_state_count, output_count)
    gate_set = gen_fun(rnn_weights, obs_set)

    if len(obs_set.shape) > 2:
        obs_set = flatten_io(obs_set)

    if len(gate_set.shape) > 2:
        gate_set = flatten_io(gate_set)

    regress = LinearRegression()
    regress.fit(obs_set.T, gate_set.T)
    return regress


def analyze_map(regress, save_path=None, notebook_display=False):
    params = regress.coef_

    plt.figure()
    sns.heatmap(parameters)
    plt.xlabel('Features')
    plt.ylabel('Gates ([0-50] U; [50-100] R; [100-150] T)')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    if notebook_display:
        plt.show()
