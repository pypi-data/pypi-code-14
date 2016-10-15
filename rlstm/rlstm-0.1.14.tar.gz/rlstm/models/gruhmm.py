from __future__ import absolute_import, print_function

from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.models import gru, grudrop, gruredun, hmm
from rlstm.weights_parser import WeightsParser
from rlstm.nn_util import sigmoid, add_bias_and_multiply
from rlstm.common_util import safe_log


def normalize(x):
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x / norm


def kdropout(weights, k):
    ''' chooses k indexes of x. set others to 0. '''
    num_inputs = weights.shape[0]
    num_states = weights.shape[1]
    new_weights = copy(weights)
    # sort the weights
    sort_id_weights = np.argsort(np.abs(new_weights), axis=1)
    sort_weights = new_weights[np.arange(num_inputs)[:, None], sort_id_weights]
    sort_weights = np.hstack(
        (np.zeros((num_inputs, num_states-k)), sort_weights[:, -k:]))
    # recover indexes into new_weights
    recover_sort_id = np.argsort(sort_id_weights, axis=1)
    new_weights = sort_weights[np.arange(num_inputs)[:, None], recover_sort_id]
    return new_weights


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


def hiddens_to_output_probs(
        hiddens,
        output_h_weights,
        lstate_norm=0,
        output_hmm_weights=0):

    state = np.vstack((copy(lstate_norm), np.ones((1, lstate_norm.shape[1]))))
    output = sigmoid(np.dot(hiddens, output_h_weights) +
                     np.transpose(np.dot(output_hmm_weights, state)))
    # output = logsumexp( output ) # normalize log-probs (multinomial case)
    return safe_log(output), safe_log(1 - output)


def update_gru(
        max_conn,
        redun_epsilon,
        curr_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights,
        reset_x_weights,
        reset_h_weights,
        thidden_x_weights,
        thidden_h_weights):

    if redun_epsilon > 0:
        num_hiddens = prev_hiddens.shape[1]

        # get "redundant" index by cosine distances between weight matrices
        all_x_weights = np.concatenate(
            (update_x_weights, reset_x_weights, thidden_x_weights), axis=1)
        all_x_redun, xy_redun = is_redundant(
            sparse_cos_dists(all_x_weights, all_x_weights), epsilon)

        all_h_weights = np.concatenate(
            (update_h_weights, reset_h_weights, thidden_h_weights), axis=1)
        all_h_redun, hy_redun = is_redundant(
            sparse_cos_dists(all_h_weights, all_h_weights), epsilon)

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

    if max_conn > 0:
        update_x_weights = kdropout(update_x_weights, max_conn)
        update_h_weights = kdropout(update_h_weights, max_conn)
        reset_x_weights = kdropout(reset_x_weights, max_conn)
        reset_h_weights = kdropout(reset_h_weights, max_conn)
        thidden_x_weights = kdropout(thidden_x_weights, max_conn)
        thidden_h_weights = kdropout(thidden_h_weights, max_conn)

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

# Update GRU and HMM parameters independently


def update(
        max_conn,
        redun_epsilon,
        curr_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights,
        reset_x_weights,
        reset_h_weights,
        thidden_x_weights,
        thidden_h_weights,
        prev_lstate,
        ltrans_mat,
        lobs_mat):

    hiddens = update_gru(max_conn, redun_epsilon,
                         curr_input, prev_hiddens, update_x_weights,
                         update_h_weights, reset_x_weights, reset_h_weights,
                         thidden_x_weights, thidden_h_weights)
    curr_lstate = hmm.update(curr_input, prev_lstate, ltrans_mat, lobs_mat)
    return hiddens, curr_lstate


def build(
        input_count,
        hmm_state_count,
        gru_state_count,
        output_count,
        max_conn=0,
        redun_epsilon=0):

    # the input count is just the number of input dimensions, we
    # assume that any/all 1-hot encoding, etc. has been done already.
    # the output count is the *number* of *binary* outputs (no
    # multinomial or continuous support at the moment)
    parser = WeightsParser()

    # GRU parameters
    parser.add_shape('init_hiddens', (1, gru_state_count))
    parser.add_shape('update_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('update_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('reset_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('reset_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('thidden_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('thidden_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('output_h_weights', (gru_state_count, output_count))

    num_gru_weights = parser.num_weights

    # HMM parameters
    parser.add_shape('lpi_mat', (hmm_state_count, 1))
    parser.add_shape('ltrans_mat', (hmm_state_count, hmm_state_count))
    parser.add_shape('lobs_mat', (hmm_state_count, input_count))
    parser.add_shape('output_hmm_weights', (output_count, hmm_state_count + 1))

    num_hmm_weights = parser.num_weights - num_gru_weights

    # Make predictions through a linear combination of GRU and HMM parameters
    def outputs(weights, input_set):
        update_x_weights = parser.get(weights, 'update_x_weights')
        update_h_weights = parser.get(weights, 'update_h_weights')
        reset_x_weights = parser.get(weights, 'reset_x_weights')
        reset_h_weights = parser.get(weights, 'reset_h_weights')
        thidden_x_weights = parser.get(weights, 'thidden_x_weights')
        thidden_h_weights = parser.get(weights, 'thidden_h_weights')
        output_h_weights = parser.get(weights, 'output_h_weights')

        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        lobs_mat = parser.get(weights, 'lobs_mat')

        output_hmm_weights = parser.get(weights, 'output_hmm_weights')

        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)

        data_count = input_set.shape[2]
        time_count = input_set.shape[1]

        # the output set of dimension ( output_count, time_count, data_count )
        # output_set = np.zeros( ( output_count, time_count, data_count ) )
        all_ll = 0
        for data_iter in range(data_count):

            # Initialize hidden states in the HMM
            hiddens = copy(parser.get(weights, 'init_hiddens'))

            # Initialize belief in HMM with the first set of observations so
            # things are sync'd appropriately
            lstate = copy(lpi_mat)
            my_input = copy(input_set[:, 0, data_iter])
            my_input[my_input < .5] = -1
            tmp = -1 * \
                logsumexp(
                    hmm.my_dstack([np.zeros(lobs_mat.shape), lobs_mat * my_input]), axis=2)
            lstate = lstate + np.sum(tmp, 1, keepdims=True)

            # Loop over time steps
            for time_iter in range(time_count):
                hiddens, lstate = update(
                    max_conn,
                    redun_epsilon,
                    np.expand_dims(input_set[:, time_iter, data_iter], axis=0),
                    hiddens,
                    update_x_weights,
                    update_h_weights,
                    reset_x_weights,
                    reset_h_weights,
                    thidden_x_weights,
                    thidden_h_weights,
                    lstate,
                    ltrans_mat,
                    lobs_mat)

                lstate_norm = lstate - logsumexp(lstate)
                # output_set[:,time_iter,data_iter] = \
                #    hiddens_to_output_probs( hiddens, output_h_weights )
                # more convoluted way with hstack and vstack because
                # autograd does not support assigning with indices
                out_vec1, out_vec0 = hiddens_to_output_probs(
                    hiddens,
                    output_h_weights,
                    lstate_norm,
                    output_hmm_weights)

                out_vec1 = np.transpose(out_vec1)
                out_vec0 = np.transpose(out_vec0)
                if time_iter == 0:
                    out_mat1 = out_vec1
                    out_mat0 = out_vec0
                    lmat = lstate_norm
                else:
                    out_mat1 = np.hstack((out_mat1, out_vec1))
                    out_mat0 = np.hstack((out_mat0, out_vec0))
                    lmat = np.hstack((lmat, lstate_norm))

            my_ll = logsumexp(lstate)
            all_ll = all_ll + my_ll
            if data_iter == 0:
                output_set1 = out_mat1
                output_set0 = out_mat0
                lstate_set = lmat
            else:
                output_set1 = np.dstack((output_set1, out_mat1))
                output_set0 = np.dstack((output_set0, out_mat0))
                lstate_set = np.dstack((lstate_set, lmat))

        return output_set1, output_set0, all_ll, lstate_set

    def log_likelihood(weights, input_set, output_set=None):
        lprobs1, lprobs0, all_ll, lstate_set = outputs(weights, input_set)
        if output_set is None:
            return all_ll
        else:
            lprobs = output_set * lprobs1 + (1 - output_set) * lprobs0
            ll = np.sum(lprobs)
            return ll

    return outputs, log_likelihood, num_gru_weights, num_hmm_weights
