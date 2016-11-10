from __future__ import absolute_import, print_function

import pdb
import os
import sys
from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.models import lr
from rlstm.weights_parser import WeightsParser
from rlstm.common_util import safe_log, my_dstack
from rlstm.nn_util import sigmoid

sys.path.append('../emission_models')
sys.path.append('../')

# this is for FenceArray3D
from rlstm.timeseries_util import farray

# HMM provides continuous support for HMM through
# continuous emission functions.
import rlstm.emission_models.bernoulli_multivariate as bernoulli_mv
import rlstm.emission_models.diagonal_gaussian_multivariate as gaussian_mv


# ------------------------- #
#         HMM Utils         #
# ------------------------- #


def calc_loss_for_many_sequences(
        x_DMF=None,
        y_CMF=None,
        calc_log_proba_arr_for_x=None,
        eta_DK=None,
        start_log_proba_K=None,
        trans_log_proba_KK=None,
        output_weights_CK=None,
        **kwargs):
    ''' Compute loss (negative log probability) for many sequences given an HMM

    Args
    ----
    x_DMF : FencePost3D array, D x M, of real values
        Each row contains observed x data at one timestep of a sequence.
    y_CMF : FencePost3D array, C x M, of real values
        Each row contains observed y responses at one timestep of a sequence.
    calc_log_proba_arr_for_x : function
        Computes log proba of each observation under each possible state
        Returns T x K array
    eta_DK : NumPy array, D x K, of real values
        Contains parameters to calculate emission probabilities
    start_log_proba_K : 1D array, size K
        Starting-state log probabilities for the HMM.
        np.exp(start_log_proba_K) must sum to one
    trans_log_proba_KK : 2D array, size K x K
        Transition log probabilities for the HMM.
        np.exp(trans_log_proba_KK) must sum to one along each row
    output_weights_CK : 2D array, size C x K
        Logistic Regression weights to calculate output probabilities

    Returns
    -------
    loss_x : real scalar
    loss_y : real scalar
    '''
    n_seqs = len(x.DMF.shape[1]) - 1
    n_dims = x_DMF.shape[0]

    loss_x = 0.0
    loss_y = 0.0

    for n in xrange(n_seqs):
        # Get slice of x data corresp. to current sequence
        x_n_DT = x_DMF.slice((xrange(n_dims), n))
        if y_CM is None:
            y_n_CT = None
        else:
            y_n_CT = y_CMF.slice((xrange(n_dims), n))

        loss_x_n, loss_y_n, belief_log_proba_TK = calc_loss_for_one_sequence(
            x_n_DT=x_n_DT,
            y_n_CT=y_n_CT,
            calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
            eta_DK=eta_DK,
            start_log_proba_K=start_log_proba_K,
            trans_log_proba_KK=trans_log_proba_KK,
            output_weights_CK=output_weights_CK)

        loss_x = loss_x + loss_x_n
        loss_y = loss_y + loss_y_n

        # Use hstack instead of indexing for autograd-friendliness
        if n == 0:
            belief_log_proba_NTK = log_proba_TK
        else:
            belief_log_proba_NTK = np.hstack((belief_log_proba_NTK, log_proba_TK))

    # wrap things in TKF
    belief_log_proba_TKF = farray(belief_log_proba_NTK, x_DMF.fenceposts)
    return loss_x, loss_y, belief_log_proba_TKF


def calc_loss_for_one_sequence(
        x_n_DT=None,
        y_n_CT=None,
        calc_log_proba_arr_for_x=None,
        eta_DK=None,
        start_log_proba_K=None,
        trans_log_proba_KK=None,
        output_weights_CK=None,
        **kwargs):
    ''' Compute loss (negative log probability) for one sequence given an HMM

    Args
    ----
    x_n_DT : 2D array, D x T, of real values
        Each row contains observed x data at timestep t of the sequence.
    y_n_CT : 2D array, C x T, of real values
        Each row contains observed y responses at timestep t of the seq.
    calc_log_proba_arr_for_x : function
        Computes log proba of each observation under each possible state
        Returns T x K array
    eta_DK : NumPy array, D x K, of real values
        Contains parameters to calculate emission probabilities
    start_log_proba_K : 1D array, size K
        Starting-state log probabilities for the HMM.
        np.exp(start_log_proba_K) must sum to one
    trans_log_proba_KK : 2D array, size K x K
        Transition log probabilities for the HMM.
        np.exp(trans_log_proba_KK) must sum to one along each row

    Returns
    -------
    loss_x : real scalar
    loss_y : real scalar
    '''
    n_timesteps = x_n_DT.shape[1]
    n_states = start_log_proba_K.shape[0]

    # Compute log proba array
    x_n_log_proba_TK = calc_log_proba_arr_for_x(
        x_n_DT,
        eta_DK=eta_DK)

    # store all state probabilities
    belief_log_proba_TK = np.zeros((n_timesteps, n_states))

    # Initialize fwd belief vector at t = 0
    cur_belief_log_proba_K = start_log_proba_K + x_n_log_proba_TK[0]
    cur_x_log_proba = logsumexp(cur_belief_log_proba_K)
    cur_belief_log_proba_K = cur_belief_log_proba_K - cur_x_log_proba

    loss_x = cur_x_log_proba
    loss_y = 0.0

    # Recursively update forward beliefs via dynamic programming
    for t in range(1, n_timesteps):
        cur_belief_log_proba_K, cur_x_log_proba = update_belief_log_probas(
            cur_belief_log_proba_K,
            x_n_log_proba_TK[t],
            trans_log_proba_KK)

        belief_log_proba_TK[t, :] = cur_belief_log_proba_K

        # Compute log proba for x[t]
        loss_x += cur_x_log_proba

        # Compute log proba for y[t]
        if y_n_CT is not None:
            loss_y += compute_out_lprob(
                y_n_CT[:, t], cur_belief_log_proba_K, output_weights_CK)

    return loss_x, loss_y, belief_log_proba_TK


def update_belief_log_probas(
        prev_belief_log_proba_K,
        curr_data_log_proba_K,
        trans_log_proba_KK,
        return_norm_const=1):
    '''

    Examples
    --------
    # Uniform belief and uniform transitions, should just equal data probs
    >>> prev_belief_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> curr_data_log_proba_K = np.log(np.asarray([0.6, 0.4]))
    >>> trans_log_proba_KK = np.log(np.asarray([[0.5, 0.5], [0.5, 0.5]]))
    >>> curr_belief_log_proba_K = update_belief_log_probas(
    ...     prev_belief_log_proba_K, curr_data_log_proba_K, trans_log_proba_KK,
    ...     return_norm_const=0)
    >>> print np.exp(curr_belief_log_proba_K)
    [ 0.6  0.4]

    >>> prev_belief_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> curr_data_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> trans_log_proba_KK = np.log(np.asarray([[0.9, 0.1], [0.9, 0.1]]))
    >>> curr_belief_log_proba_K = update_belief_log_probas(
    ...     prev_belief_log_proba_K, curr_data_log_proba_K, trans_log_proba_KK,
    ...     return_norm_const=0)
    >>> print np.exp(curr_belief_log_proba_K)
    [ 0.9  0.1]
    '''
    cur_belief_log_proba_K = logsumexp(
        trans_log_proba_KK + prev_belief_log_proba_K[:, np.newaxis],
        axis=0)
    cur_belief_log_proba_K = cur_belief_log_proba_K \
        + curr_data_log_proba_K
    # Normalize in log space
    log_norm_const = logsumexp(cur_belief_log_proba_K)
    cur_belief_log_proba_K = cur_belief_log_proba_K - log_norm_const
    if return_norm_const:
        return cur_belief_log_proba_K, log_norm_const
    else:
        return cur_belief_log_proba_K


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


# Computes the beliefs for a new set of data, given the weights and
# the observations (note that outputs aren't used in
# updating/computing the belief because we wish to respect the HMM
# structure of the model)

def get_state_prob_set(pred_fun, weights, obs_farray):
    ll_in, ll_out, lstate_set, lvec = pred_fun(weights, obs_farray)
    return ll_in, lstate_set


# ------------------------- #
#     HMM Constructor       #
# ------------------------- #


def build(input_count, state_count, output_count=None, emission_type='bernoulli'):
    # the input count is just the number of input dimensions, we
    # assume that any/all 1-hot encoding, etc. has been done already.
    # the output count is the *number* of *binary* outputs (no
    # multinomial or continuous support at the moment)  lpi_mat is a
    # column vector, and so are all the lstates; ltrans( s, s') and
    # lobs( s, k ).
    # emission_type defines the distribution behind the emission
    # matrix used in HMM. discrete and continuous matrices are supported.
    assert emission_type in ['bernoulli', 'gaussian'], 'EMISSION_TYPE not recognized.'

    if emission_type == 'bernoulli':
        import bernoulli_multivariate as emission_module
    else:  # must be gaussian
        import diagonal_gaussian_multivariate as emission_module

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
    def outputs(weights, input_farray, output_farray=None):
        ''' Only farrays are supported. See FenceArray3D.
            One may wrap normal 3D arrays in farray().
        '''
        feat_count = input_farray.shape[0]
        data_count = input_farray.shape[2]

        # Get parameters
        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        eta_mat = parser.get(weights, 'eta_mat')  # see emission_models folder
        if output_farray is not None:
            out_weights = parser.get(weights, 'out_weights')

        # Normalize the initial distribution and the transition distribution
        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)

        # calculate loss for all sequences
        in_ll, _, lstate_farray = calc_loss_for_many_sequences(
            x_DMF=input_farray,
            # y_CMF=output_farray,
            calc_log_proba_arr_for_x=emission_module.calc_log_proba_data_arr_NK,
            eta_DK=eta_mat,
            start_log_proba_K=lpi_mat,
            trans_log_proba_KK=ltrans_mat)
            # output_weights_CK=out_weights)

        if output_farray is not None:
            out_ll = lr.log_likelihood(out_weights, lstate_farray, output_farray)

        # return values
        return in_ll, out_ll, lstate_farray

    def prediction(weights, input_farray):
        ''' log probabilities '''
        out_weights = parser.get(weights, 'out_weights')
        _, _, lstate_farray = outputs(weights, input_farray)
        logpreds = lr.logistic_log_predictions(
            out_weights,
            lstate_farray,
            state_count,
            output_count)

        return logpreds

    # Returns the log likelihood. If there are outputs, returns the
    # probability of the output set.  Otherwise, returns the
    # probability of the input set based on the model.
    def log_likelihood(weights, input_farray, output_farray=None):
        in_ll, out_ll, lstate_set = outputs(
            weights, input_farray, output_farray)
        if output_set is None:
            return in_ll
        else:
            return out_ll

    if not output_count is None:
        return prediction, log_likelihood, parser.num_weights
    else:
        return outputs, log_likelihood, parser.num_weights

