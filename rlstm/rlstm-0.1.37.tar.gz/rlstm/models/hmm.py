from __future__ import absolute_import, print_function

import pdb
from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp
from scipy.optimize import minimize

from rlstm.models import lr
from rlstm.weights_parser import WeightsParser
from rlstm.common_util import safe_log, my_dstack
from rlstm.nn_util import sigmoid


# -------------------------- #
#   FFBS Training Functions  #
# -------------------------- #
# Assumes that observations are binary (though maybe multiple dimensions)
# * hmm_state_set is NxT where (n,t) contains the state in seq n at time t
# * state_count is a scalar
# * obs_prob_set is KxT prob of the obs in each state k at each time t
# finale! not optimized for speed!


def normalize(vec):
    vec = vec / np.sum(vec)
    return vec


def sample_pi_mat(hmm_state_set, state_count):
    pi_mat = np.ones((state_count)) / state_count
    for data_index in range(hmm_state_set.shape[0]):
        pi_mat[hmm_state_set[data_index, 0]] += 1
    pi_mat = np.random.dirichlet(alpha=pi_mat)
    return pi_mat


def sample_obs_mat(hmm_state_set, obs_set, state_count):
    state_visit_count_set = np.bincount(
        hmm_state_set.flatten().astype('int'), minlength=state_count)
    obs_count = obs_set.shape[0]
    obs = np.zeros((state_count, obs_count))
    for data_index in range(hmm_state_set.shape[0]):
        for obs_index in range(obs_count):
            for time_index in range(hmm_state_set.shape[1]):
                obs[ hmm_state_set[ data_index , time_index ] , obs_index ] = \
                    obs[ hmm_state_set[ data_index , time_index ] , obs_index ] + \
                    obs_set[obs_index, time_index, data_index]
    for obs_index in range(obs_count):
        for state_index in range(state_count):
            alpha = np.array(((1./2 + obs[state_index, obs_index]),
                              (1./2 + state_visit_count_set[state_index] - obs[state_index, obs_index])))
            obs[state_index, obs_index] = np.random.dirichlet(alpha=alpha)[0]
    return obs


def sample_trans_mat(hmm_states, num_states):
    trans_mat = np.ones((num_states, num_states)) / num_states
    for data_index in range(hmm_states.shape[0]):
        for time_index in range(hmm_states.shape[1]):
            if time_index > 1:
                trans_mat[hmm_states[data_index, time_index-1],
                          hmm_states[data_index, time_index]] += 1
    for state in range(num_states):
        trans_mat[state, :] = np.random.dirichlet(alpha=trans_mat[state, :])
    return trans_mat


def forward_filtering(trans_mat, pi_mat, obs_prob_set):
    time_count = obs_prob_set.shape[1]
    fresult = np.zeros((time_count, trans_mat.shape[0]))
    fresult[0, :] = normalize(copy(pi_mat.flatten()) *
                              obs_prob_set[:, 0])
    for time_index in range(1, time_count):
        fresult[time_index, :] = normalize(np.dot(
            fresult[time_index-1, :], trans_mat) * obs_prob_set[:, time_index])
    return fresult


def ffbs(trans_mat, pi_mat, obs_prob_set):
    fresult = forward_filtering(trans_mat, pi_mat, obs_prob_set)
    seq_length = obs_prob_set.shape[1]
    bsamples = np.zeros(seq_length, dtype=int)
    bsamples[
        seq_length-1] = np.random.multinomial(1, fresult[seq_length-1]).argmax()
    for index in reversed(range(seq_length-1)):
        prob = normalize(fresult[index] * trans_mat[:, bsamples[index+1]])
        bsamples[index] = np.random.multinomial(1, prob).argmax()
    return bsamples


def compute_obs_prob_set(obs_set, obs_mat):
    # assumes that the obs_set is already a 2D slice of obs x T
    state_count, obs_count = obs_mat.shape
    ll = np.zeros((state_count, obs_set.shape[1]))
    for obs_index in range(obs_count):
        ll = ll + safe_log(np.dot(obs_mat[:, [obs_index]], obs_set[[obs_index], :]) +
                           np.dot(1 - obs_mat[:, [obs_index]], 1 - obs_set[[obs_index], :]))
    return np.exp(ll)

# ------------------------- #
#         HMM Utils         #
# ------------------------- #

# updates the belief state of the HMM, does not renormalize constants.
# Update order is transition first, observation next (so on the very
# first iteration, if we receive an observation before transitioning,
# we need to account for that separately)


def update(curr_input, prev_lstate, ltrans_mat, lobs_mat):
    curr_lstate = logsumexp(prev_lstate + ltrans_mat, axis=0, keepdims=True)
    curr_lstate = np.transpose(curr_lstate)

    # the lobs mat is the natural parameter that we covert to a
    # binary value using 1/(1+exp(z)). Note that 1-p(1) =
    # 1/(1+exp(-z)), so for 0's we need to multiply the z by -1.
    # Then to take the log: log(1/(1+exp(z))) = -log(1+exp(z)).
    my_input = copy(curr_input)
    my_input[curr_input < .5] = -1
    tmp = -1 * logsumexp(my_dstack([np.zeros(lobs_mat.shape),
                                    lobs_mat * my_input]), axis=2)
    curr_lstate = curr_lstate + np.sum(tmp, 1, keepdims=True)

    # finale: here is slower code that does the same thing, here in
    # case we need to check for correctness again
    '''
    lbelief = prev_lstate
    trans_mat = np.exp( ltrans_mat )
    maxb = np.max( lbelief )
    lbelief = maxb + np.log( np.dot( trans_mat.T , np.exp( lbelief - maxb ) ) )
    obs_mat = 1 / ( 1 + np.exp( lobs_mat ) )
    pobs = copy( obs_mat )
    pobs[:, curr_input == 0 ] = 1 - pobs[:, curr_input == 0 ]
    lbelief = lbelief + np.sum( np.log( pobs ) , 1 , keepdims = True )
    print( np.sum( np.abs( lbelief - curr_lstate ) ) )
    '''

    # return the updated belief
    return curr_lstate

# Uses a sigmoid/logistic regression model for predicting the outputs
# given the input


def compute_out_lprob(current_output, lstate_norm, out_weights):
    my_input = np.vstack((copy(lstate_norm),
                          np.ones((1, lstate_norm.shape[1]))))
    pred_set = sigmoid(np.dot(out_weights, my_input))
    label_prob_set = pred_set * current_output + \
        (1 - pred_set) * (1 - current_output)
    lout = np.sum(safe_log(label_prob_set))
    return lout


def build(input_count, state_count, output_count=None):
    # the input count is just the number of input dimensions, we
    # assume that any/all 1-hot encoding, etc. has been done already.
    # the output count is the *number* of *binary* outputs (no
    # multinomial or continuous support at the moment)  lpi_mat is a
    # column vector, and so are all the lstates; ltrans( s, s') and
    # lobs( s, k ).
    parser = WeightsParser()
    parser.add_shape('lpi_mat', (state_count, 1))
    parser.add_shape('ltrans_mat', (state_count, state_count))
    parser.add_shape('lobs_mat', (state_count, input_count))
    if output_count is not None:
        parser.add_shape('out_weights', (output_count, state_count + 1))

    # Computes the state probabilities and overall log-likelihood for
    # the HMM.  lstate_set is the log of the belief at every time
    # step.  ll_vec is the log probs of the sequence of observation at
    # every time step: p(o1), p(o1,o2), p(o1,o2,o3), etc. mostly for
    # helping with diagnostics.  Somewhat arcane concatinations to get
    # around various autograd-related things.
    def outputs(weights, input_set, output_set=None):
        data_count = input_set.shape[2]
        time_count = input_set.shape[1]

        # Get parameters
        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        lobs_mat = parser.get(weights, 'lobs_mat')
        if output_set is not None:
            out_weights = parser.get(weights, 'out_weights')

        # Normalize the initial distribution and the transition distribution
        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)

        # finale: for debuggering: ll_per_time should return the same
        # ll as the final ll computed in this loop
        '''
        pi_mat = np.exp( lpi_mat )
        trans_mat = np.exp( ltrans_mat )
        obs_mat = 1 / ( 1 + np.exp( lobs_mat ) )
        my_out = ll_per_time( input_set , trans_mat , obs_mat , pi_mat )
        '''

        # Loop over the sequences
        in_ll = 0
        out_ll = 0
        for data_index in range(data_count):

            # Initialize the belief, including the very first observation
            lstate = copy(lpi_mat)
            my_input = copy(input_set[:, 0, data_index])
            my_input[my_input < .5] = -1
            tmp = -1 * \
                logsumexp(
                    my_dstack([np.zeros(lobs_mat.shape), lobs_mat * my_input]), axis=2)
            lstate = lstate + np.sum(tmp, 1, keepdims=True)

            # Loop over time indices
            for time_index in range(time_count):
                if time_index > 0:
                    lstate = update(input_set[:, time_index, data_index],
                                    lstate, ltrans_mat, lobs_mat)
                lstate_norm = lstate - logsumexp(lstate)

                # Compute the probability of the observation
                my_ll = logsumexp(lstate)
                if time_index == 0:
                    lmat = lstate_norm
                    ll_vec = my_ll
                else:
                    lmat = np.hstack((lmat, lstate_norm))
                    ll_vec = np.vstack((ll_vec, my_ll))

                # Compute the probability of the output
                if output_set is not None:
                    out_ll = out_ll + compute_out_lprob(output_set[:, time_index, data_index],
                                                        lstate_norm, out_weights)

            # Track the overall probability of the sequence, collection of
            # beliefs
            in_ll = in_ll + my_ll
            if data_index == 0:
                lstate_set = lmat
                ll_mat = ll_vec
            else:
                lstate_set = my_dstack((lstate_set, lmat))
                ll_mat = np.hstack((ll_mat, ll_vec))

        # compute for the output
        if output_set is not None:
            out_ll = lr.log_likelihood(out_weights, lstate_set, output_set)

        # return values
        return in_ll, out_ll, lstate_set, ll_mat

    def prediction(weights, input_set):
        out_weights = parser.get(weights, 'out_weights')
        _, _, lstate_set, _ = outputs(weights, input_set)
        preds = lr.logistic_predictions(
            out_weights, lstate_set, state_count, output_count)
        return preds.reshape(output_count,
                             input_set.shape[-2],
                             input_set.shape[-1])

    # Returns the log likelihood. If there are outputs, returns the
    # probability of the output set.  Otherwise, returns the
    # probability of the input set based on the model.
    def log_likelihood(weights, input_set, output_set=None):
        in_ll, out_ll, lstate_set, ll_vec = outputs(
            weights, input_set, output_set)
        if output_set is None:
            return in_ll
        else:
            return out_ll

    # For debugging/visualization: converts log weights into
    # probabilities, prints them out, and also displays the transition
    # and emission matrices
    def print_weights(weights, show_plot=False):
        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        lobs_mat = parser.get(weights, 'lobs_mat')

        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)

        print("Pi")
        print(np.exp(lpi_mat))
        print("Trans")
        print(np.exp(ltrans_mat))
        print("Obs")
        print(1 / (1 + np.exp(lobs_mat)))

        if show_plot:
            import matplotlib.pyplot as plt
            plt.matshow((1 / (1 + np.exp(lobs_mat))), vmin=0, vmax=1)
            plt.colorbar()
            plt.matshow(np.exp(ltrans_mat), vmin=0, vmax=1)
            plt.colorbar()
            plt.show(block=False)

        return np.exp(lpi_mat), np.exp(ltrans_mat), (1 / (1 + np.exp(lobs_mat)))

    if not output_count is None:
        return prediction, log_likelihood, parser.num_weights, print_weights
    else:
        return outputs, log_likelihood, parser.num_weights, print_weights

# ------------------------ #
#     Debugging Tools      #
# ------------------------ #
# Computes the ll over the sequence for each sequence per time step
# (ie. p(o1), p(o1,o2), p(o1,o2,o3), etc. for each sequence)


def ll_per_time(input_set, trans_mat, obs_mat, pi_mat):
    state_count = trans_mat.shape[0]
    obs_count, time_count, data_count = input_set.shape
    ll_set = np.zeros((time_count, data_count))
    for data_index in range(data_count):
        lbelief = copy(safe_log(pi_mat))
        for time_index in range(time_count):
            pvec = np.zeros((state_count, 1))
            pobs = copy(obs_mat)
            pobs[:, input_set[:, time_index, data_index] == 0] = 1 - \
                pobs[:, input_set[:, time_index, data_index] == 0]
            lbelief = lbelief + np.sum(safe_log(pobs), 1, keepdims=True)
            ll_set[time_index, data_index] = logsumexp(lbelief)
            maxb = np.max(lbelief)
            lbelief = maxb + \
                safe_log(np.dot(trans_mat.T, np.exp(lbelief - maxb)))
    return ll_set

# Computes the probability of one-step ahead observation, given
# current belief for each time step, ie. given b_t, computes p(o_t+1)


def ltrans_per_time(lstate_set, input_set, trans_mat, obs_mat):
    state_count, time_count, data_count = lstate_set.shape
    obs_count = input_set.shape[0]
    ll_trans = np.zeros((time_count - 1, data_count))
    for data_index in range(data_count):
        my_ll_trans = np.zeros((obs_count, time_count - 1))
        my_input_set = input_set[:, 1:, data_index]
        next_set = np.dot(trans_mat.T, np.exp(lstate_set[:, :, data_index]))
        next_set = next_set[:, 1:]
        p1 = np.dot(obs_mat.T, next_set)
        one_set = (my_input_set == 1)
        my_ll_trans[one_set] = safe_log(p1[one_set])
        my_ll_trans[1 - one_set] = safe_log(1 - p1[1 - one_set])
        my_ll_trans = np.sum(my_ll_trans, 0)
        ll_trans[:, data_index] = my_ll_trans
    return ll_trans

# Computes the probability of each observation given the belief at the
# time, ie. given b_t computes p(o_t).


def lobs_per_time(lstate_set, input_set, obs_mat):
    state_count, time_count, data_count = lstate_set.shape
    obs_count = input_set.shape[0]
    ll_obs = np.zeros((obs_count, time_count, data_count))
    for data_index in range(data_count):
        my_ll_obs = np.zeros((obs_count, time_count))
        p1 = np.dot(obs_mat.T, np.exp(lstate_set[:, :, data_index]))
        one_set = (input_set[:, :, data_index] == 1)
        my_ll_obs[one_set] = safe_log(p1[one_set])
        my_ll_obs[1 - one_set] = safe_log(1 - p1[1 - one_set])
        ll_obs[:, :, data_index] = my_ll_obs
    return ll_obs

# Computes the beliefs for a new set of data, given the weights and
# the observations (note that outputs aren't used in
# updating/computing the belief because we wish to respect the HMM
# structure of the model)


def get_state_prob_set(pred_fun, weights, obs_set):
    ll_in, ll_out, lstate_set, lvec = pred_fun(weights, obs_set)
    return ll_in, lstate_set
