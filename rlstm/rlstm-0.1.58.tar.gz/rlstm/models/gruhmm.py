from __future__ import absolute_import, print_function

from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.models import gru, hmm
from rlstm.weights_parser import WeightsParser
from rlstm.nn_util import sigmoid, add_bias_and_multiply
from rlstm.common_util import safe_log


# --------------------
#   GRUHMM FUNCTIONS
# --------------------


def hiddens_to_output_probs(
        hiddens,
        output_h_weights,
        lstate_norm,
        output_hmm_weights):

    state = np.vstack((copy(lstate_norm), np.ones((1, lstate_norm.shape[1]))))
    output = sigmoid(np.dot(hiddens, output_h_weights) +
                     np.transpose(np.dot(output_hmm_weights, state)))
    # output = logsumexp( output ) # normalize log-probs (multinomial case)
    return safe_log(output), safe_log(1 - output)


# --------------------
#  GRUHMM CONSTRUCTOR
# --------------------


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
    def outputs(weights, input_farray):
        # grab all gru weights
        update_x_weights = parser.get(weights, 'update_x_weights')
        update_h_weights = parser.get(weights, 'update_h_weights')
        reset_x_weights = parser.get(weights, 'reset_x_weights')
        reset_h_weights = parser.get(weights, 'reset_h_weights')
        thidden_x_weights = parser.get(weights, 'thidden_x_weights')
        thidden_h_weights = parser.get(weights, 'thidden_h_weights')
        output_h_weights = parser.get(weights, 'output_h_weights')

        # grab hmm weights
        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        eta_mat = parser.get(weights, 'eta_mat')
        output_hmm_weights = parser.get(weights, 'output_hmm_weights')

        # normalize probas
        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)

        data_count = input_farray.shape[2]
        feat_count = input_farray.shape[0]

        # the output set of dimension ( output_count, time_count, data_count )
        # output_set = np.zeros( ( output_count, time_count, data_count ) )
        all_ll = 0
        for data_iter in range(data_count):
            # Initialize hidden states in the HMM
            hiddens = copy(parser.get(weights, 'init_hiddens'))
            time_count = input_farray.shape[1][data_iter]

            # grab sequence for this data_iter
            curr_input_DT = input_farray.slice((xrange(feat_count), data_iter))

            # get log proba array from emissions
            curr_input_log_proba_TK = calc_log_proba_arr_for_x(
                curr_input_DT, eta_DK=eta_mat)

            # Initialize fwd belief vector at t = 0
            cur_belief_log_proba_K = lpi_mat + curr_input_log_proba_TK[0]
            cur_x_log_proba = logsumexp(cur_belief_log_proba_K)
            cur_belief_log_proba_K = cur_belief_log_proba_K - cur_x_log_proba

            # Loop over time steps
            for time_iter in range(time_count):
                # update gru
                hiddens = gru.update(
                    max_conn,
                    redun_epsilon,
                    np.expand_dims(curr_input_DT[:, time_count], axis=0),
                    prev_hiddens,
                    update_x_weights,
                    update_h_weights,
                    reset_x_weights,
                    reset_h_weights,
                    thidden_x_weights,
                    thidden_h_weights)

                # update hmm
                cur_belief_log_proba_K, cur_x_log_proba = update_belief_log_probas(
                    cur_belief_log_proba_K,
                    curr_input_log_proba_TK[t],
                    ltrans_mat)

                # output_set[:,time_iter,data_iter] = \
                #    hiddens_to_output_probs( hiddens, output_h_weights )
                # more convoluted way with hstack and vstack because
                # autograd does not support assigning with indices
                out_vec1, out_vec0 = hiddens_to_output_probs(
                    hiddens,
                    output_h_weights,
                    cur_belief_log_proba_K,
                    output_hmm_weights)

                out_vec1 = np.transpose(out_vec1)
                out_vec0 = np.transpose(out_vec0)
                if time_iter == 0:
                    out_mat1 = out_vec1
                    out_mat0 = out_vec0
                    lmat = cur_belief_log_proba_K
                else:
                    out_mat1 = np.hstack((out_mat1, out_vec1))
                    out_mat0 = np.hstack((out_mat0, out_vec0))
                    lmat = np.hstack((lmat, cur_belief_log_proba_K))

            my_ll = logsumexp(cur_belief_log_proba_K)
            all_ll = all_ll + my_ll
            if data_iter == 0:
                output_set1 = out_mat1
                output_set0 = out_mat0
                lstate_set = lmat
            else:
                output_set1 = np.hstack((output_set1, out_mat1))
                output_set0 = np.hstack((output_set0, out_mat0))
                lstate_set = np.hstack((lstate_set, lmat))

        output1_farray = farray(output_set1, input_farray.fenceposts)
        output0_farray = farray(output_set0, input_farray.fenceposts)
        lstate_farray = farray(lstate_farray, input_farray.fenceposts)

        return output1_farray, output0_farray, all_ll, lstate_farray

    def prediction(weights, input_farray):
        out, _, _, _ = outputs(weights, input_farray)
        return out

    def log_likelihood(weights, input_farray, output_farray=None):
        lprobs1_farray, lprobs0_farray, all_ll, _ = outputs(weights, input_farray)
        if output_farray is None:
            return all_ll
        else:
            cross_entropy = lambda o, lp1, lp0: o * lp1 + (1 - o) * lp0
            lprobs = cross_entropy(output_farray.array_2d, lprobs1_farray, lprobs0_farray)
            ll = np.sum(lprobs)
            return ll

    return prediction, log_likelihood, num_gru_weights, num_hmm_weights
