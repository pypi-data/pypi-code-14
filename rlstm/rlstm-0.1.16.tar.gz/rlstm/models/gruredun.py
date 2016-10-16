from __future__ import absolute_import, print_function

import pdb
from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.weights_parser import WeightsParser
from rlstm.nn_util import sigmoid, add_bias_and_multiply
from rlstm.common_util import safe_log


def row_norms(X):
    norms = np.einsum('ij,ij->i', X, X)
    return np.sqrt(norms)


def cosine_cdist(XA, XB):
    mA = XA.shape[0]
    mB = XB.shape[0]
    dm = np.zeros((mA, mB), dtype=np.double)

    normsA = row_norms(XA)
    normsB = row_norms(XB)

    dm = np.dot(XA, XB.T)
    dm /= normsA.reshape(-1, 1)
    dm /= normsB
    dm *= -1
    dm += 1
    return dm


def sparse_cos_dists(A, B):
    cos_dists_output = cosine_cdist(A, B)
    # symmetric, so just keep 1/2 (ignore diagonal)
    return np.triu(cos_dists_output, k=1)


def is_redundant(A, epsilon=0.5):
    redun_idx = []
    idx = np.argwhere(np.logical_and(np.abs(A) < epsilon, A != 0))
    if idx.shape[0] > 0:  # get unique so no duplicate removals
        # quick way to get rid of duplicates
        idx = idx[np.unique(idx[:, 1], return_index=True)[1], :]
        # create a map from uid1 to uid2
        uid_pool = np.unique(idx[:, 0])
        for uid in uid_pool:
            redun_idx.append((uid, idx[:, 1][idx[:, 0] == uid]))
    return redun_idx, idx[:, 1]


def autograd_zero(A, index):
    ''' Because autograd can't support indexing, we have to
        be kind of clever about it
            - this handles empty indexes
    '''
    B = copy(A.T)
    if index.shape[0] > 0:
        index_all = np.arange(B.shape[1])
        index_ordered = np.concatenate(
            (index, index_all[~np.in1d(index_all, index)]))
        B_ordered = B[np.arange(B.shape[0])[:, None], index_ordered]
        B_zeroed = np.concatenate(
            (np.zeros((B.shape[0], len(index))), B_ordered[:, len(index):]), axis=1)
        index_recover = np.argsort(index_ordered)
        B = B_zeroed[np.arange(B.shape[0])[:, None], index_recover]
    return B.T


def autograd_add(A, index):
    B = copy(A)
    if len(index) > 0:
        for i, j in index:
            C = np.expand_dims(B[i, :] + np.sum(B[j, :], axis=0), axis=0)
            B = np.concatenate((B[:i, :], C, B[i+1:, :]))
    return B


def split_weights(weights, num_hiddens):
    num_parts = weights.shape[1] / num_hiddens
    return [weights[:, i*num_hiddens:(i+1)*num_hiddens]
        for i in range(num_parts)]


def update(
        curr_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights,
        reset_x_weights,
        reset_h_weights,
        thidden_x_weights,
        thidden_h_weights,
        redun_epsilon=0.5):

    ''' breaks connections not in the nodes but in the wiring '''
    num_hiddens = prev_hiddens.shape[1]

    # get "redundant" index by cosine distances between weight matrices
    all_x_weights = np.concatenate(
        (update_x_weights, reset_x_weights, thidden_x_weights), axis=1)
    all_x_redun, xy_redun = is_redundant(
        sparse_cos_dists(all_x_weights, all_x_weights), redun_epsilon)

    all_h_weights = np.concatenate(
        (update_h_weights, reset_h_weights, thidden_h_weights), axis=1)
    all_h_redun, hy_redun = is_redundant(
        sparse_cos_dists(all_h_weights, all_h_weights), redun_epsilon)

    # 0 out the proper indexes in the connections
    all_x_weights = autograd_zero(
        autograd_add(all_x_weights, all_x_redun), xy_redun)
    all_h_weights = autograd_zero(
        autograd_add(all_h_weights, all_h_redun), hy_redun)

    # get the individual vectors out
    update_x_weights, reset_x_weights, thidden_x_weights = \
        split_weights(all_x_weights, num_hiddens)
    update_h_weights, reset_h_weights, thidden_h_weights = \
        split_weights(all_h_weights, num_hiddens)

    # proceed as regular gru
    update = sigmoid(
        add_bias_and_multiply(update_x_weights, curr_input) +
        np.dot(prev_hiddens, update_h_weights))

    reset = sigmoid(
        add_bias_and_multiply(reset_x_weights, curr_input) +
        np.dot(prev_hiddens, reset_h_weights))

    thiddens = np.tanh(
        add_bias_and_multiply(thidden_x_weights, curr_input) +
        np.dot(reset * prev_hiddens, thidden_h_weights))

    hiddens = (1 - update) * prev_hiddens + update * thiddens

    return hiddens


def hiddens_to_output_probs(hiddens, output_h_weights):
    # binary case, each a prob
    output = sigmoid(np.dot(hiddens, output_h_weights))
    # output - logsumexp( output ) # normalize log-probs (multinomial case)
    return safe_log(output), safe_log(1 - output)


def build(input_count, state_count, output_count, redun_epsilon=0.5):
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
                                          thidden_x_weights, thidden_h_weights,
                                          redun_epsilon=redun_epsilon)

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

    def prediction(weights, input_set):
        out, _ = outputs(weights, input_set)
        return out

    def log_likelihood(weights, input_set, output_set):
        lprobs1, lprobs0 = outputs(weights, input_set)
        lprobs = output_set * lprobs1 + (1 - output_set) * lprobs0
        ll = np.sum(lprobs)
        return ll

    return outputs, log_likelihood, parser.num_weights
