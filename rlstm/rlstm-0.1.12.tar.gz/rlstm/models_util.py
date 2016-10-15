from __future__ import print_function

import autograd.numpy as np
from autograd import value_and_grad, grad

from rlstm.optimize import adam
from rlstm import create_toy_data
from rlstm.models import lr, hmm, gru, gruhmm, grudrop, gruredun
from rlstm.nn_util import (reverse_sigmoid, init_hmm_ffbs_weights,
                           init_hmm_out_weights, init_vanilla_gru_weights)
from rlstm.common_util import safe_log, flatten_to_2d, format_preds

from copy import copy
import cPickle
import argparse

# -- train functions --


def train_by_sgd(
        obs_set,
        loglike_fun,
        num_weights,
        out_set=None,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        # regularization
        obs_lambda=0,
        l1_lambda=0,
        num_l1_weights=0,
        # optimization
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        # validation set
        va_obs_set=None,
        va_out_set=None):
    ''' Generic function for training using stochastic gradient descent.
        All models are wrapped around this function.
    '''

    num_batches = int(np.ceil(obs_set.shape[1] / float(batch_size)))

    if init_weights is None:
        init_weights = np.random.randn(num_weights) * param_scale

    def batch_indices(iter):
        idx = iter % num_batches
        return slice(idx * batch_size, (idx+1) * batch_size)

    # wrapper around loss function
    def regularized_loss(weights, x, y):
        loss = loglike_fun(weights, x, y)
        if not y is None and obs_lambda > 0:
            loss += obs_lambda*loglike_fun(weights, x, None)
        loss = -loss + l1_lambda * np.sum(np.abs(weights[:num_l1_weights]))
        return loss

    # loss function in batches
    def batch_loss(weights, iter):
        idx = batch_indices(iter)
        batch_obs_set = obs_set[:, idx]
        batch_out_set = None if out_set is None else out_set[:, idx]
        return regularized_loss(
            weights, batch_obs_set, batch_out_set)

    # loss fnction against all data
    def collective_loss(weights):
        return regularized_loss(weights, obs_set, out_set)

    def validation_loss(weights):
        return regularized_loss(weights, va_obs_set, va_out_set)

    def callback(i, ll, va_ll):
        if not va_ll is None:
            print('iter {}  |  training loss {}  |  validation loss {}'.format(
                i, round(ll,2), round(va_ll,2)))
        else:
            print('iter {}  |  training loss {}'.format(i, round(ll)))

    def callback_early_stop(i, ll, va_ll, p):
        print('iter {}  |  training loss {}  |  validation loss {}  |  patience {}'.format(
            i, round(ll,2), round(va_ll,2), p))


    grad_fun = grad(batch_loss)
    weights = adam(grad_fun,
                   init_weights,
                   step_size=0.001,
                   min_iters=min_iters,
                   max_iters=max_iters,
                   callback=callback_early_stop if early_stop else callback,
                   ll_fun=collective_loss,
                   stop_criterion=stop_criterion,
                   va_ll_fun=validation_loss if not va_obs_set is None else None,
                   early_stop=early_stop,
                   patience=patience)

    return weights


def train_lr(
        obs_set,
        out_set,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.0001,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    in_dim_count = obs_set.shape[0]
    out_dim_count = out_set.shape[0]

    if len(obs_set.shape) > 2:
        obs_set, out_set = lr.flatten_io(obs_set, out_set)

    num_weights = np.prod((out_dim_count, in_dim_count + 1))
    loglike_fun = lr.log_likelihood

    trained_weights = train_by_sgd(
        obs_set,
        lr.log_likelihood,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    pred_fun = lambda weights, obs_set: lr.logistic_predictions(
        weights, obs_set, in_dim_count, out_dim_count)

    return pred_fun, loglike_fun, trained_weights


def append_lr_to_model(
        obs_set,
        out_set,
        hmm_weights,
        output_fun,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.0001,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):
    ''' Often we train a generative model for an hmm but want to
        tag an lr afterwards. This is wrapper function around train_lr
        to do so.
    '''
    # prob_set = state mappings
    num_hmm_weights = hmm_weights.shape[0]
    lhmm, prob_set = hmm.get_state_prob_set(
        output_fun, hmm_weights, obs_set)

    # train lr
    pred_fun, ll_fun, lr_weights = train_lr(prob_set,
                                            out_set,
                                            init_weights=init_weights,
                                            min_iters=min_iters,
                                            max_iters=max_iters,
                                            batch_size=batch_size,
                                            param_scale=param_scale,
                                            obs_lambda=obs_lambda,
                                            l1_lambda=l1_lambda,
                                            stop_criterion=stop_criterion,
                                            early_stop=early_stop,
                                            patience=patience,
                                            va_obs_set=va_obs_set,
                                            va_out_set=va_out_set)

    trained_weights = np.hstack((hmm_weights, lr_weights))

    # return functions so users can pass in obs_set (instead of prob_set)
    def all_pred_fun(weights, obs_set):
        _, prob_set = hmm.get_state_prob_set(
            output_fun, weights, obs_set)
        return safe_log(pred_fun(prob_set))

    def all_loglike_fun(weights, obs_set, out_set=None):
        ''' if out_set, use lr proba; else use hmm proba
        '''

        # we know but exist (but just may want to use one)
        hmm_weights = weights[:num_hmm_weights]
        lr_weights = weights[num_hmm_weights:]

        if not out_set is None:
            _, prob_set = hmm.get_state_prob_set(
                output_fun, hmm_weights, obs_set)
            return ll_fun(lr_weights, prob_set, out_set)
        else:
            return loglike_fun(hmm_weights, obs_set)

    return all_pred_fun, all_loglike_fun, trained_weights


def train_hmm_ffbs(
        obs_set,
        out_set=None,
        hmm_state_count=5,
        ffbs_iters=500,
        # optional params are if out_set is provided
        append_lr=False,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.0001,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    # obs_set is DxTxN where T is the length of the timeseries and N
    # is the number of samples.
    obs_count, time_count, data_count = obs_set.shape
    pi_mat, trans_mat, obs_mat = init_hmm_ffbs_weights(
        hmm_state_count, obs_count, flatten=False)
    # ^ no need to do reverse_sigmoid or anything (ffbs works with regular weights)

    for ffbs_iter in range(ffbs_iters):
        # For each timeseries, infer the states
        state_set = np.zeros((data_count, time_count)).astype(int)
        for data_index in range(data_count):
            obs_prob_set = hmm.compute_obs_prob_set(
                obs_set[:, :, data_index], obs_mat)
            hmm_states = hmm.ffbs(trans_mat, pi_mat, obs_prob_set)
            state_set[data_index, :] = hmm_states

        # And then update the parameters
        pi_mat = hmm.sample_pi_mat(state_set, hmm_state_count)
        trans_mat = hmm.sample_trans_mat(state_set, hmm_state_count)
        obs_mat = hmm.sample_obs_mat(state_set, obs_set, hmm_state_count)

        ffbs_weights = np.hstack(
            (pi_mat.flatten(), trans_mat.flatten(), obs_mat.flatten()))
        print('iter {} norm {}'.format(
            ffbs_iter + 1, np.linalg.norm(ffbs_weights)))

    # if given out set, add LR
    if not out_set is None and append_lr:
        lffbs_weights = np.hstack((safe_log(pi_mat.flatten()),
                                   safe_log(trans_mat.flatten()),
                                   reverse_sigmoid(obs_mat.flatten())))

        outputs, loglike_fun, num_weights, print_weights = \
            hmm.build(obs_count, hmm_state_count)

        pred_fun, loglike_fun, lr_weights = \
            append_lr_to_model(obs_set,
                               out_set,
                               lffbs_weights,
                               outputs,
                               init_weights=init_weights,
                               min_iters=min_iters,
                               max_iters=max_iters,
                               batch_size=batch_size,
                               param_scale=param_scale,
                               obs_lambda=obs_lambda,
                               l1_lambda=l1_lambda,
                               stop_criterion=stop_criterion,
                               early_stop=early_stop,
                               patience=patience,
                               va_obs_set=va_obs_set,
                               va_out_set=va_out_set)

        trained_weights = np.hstack((ffbs_weights, lr_weights))
        return pred_fun, loglike_fun, trained_weights

    return pi_mat, trans_mat, obs_mat


def train_hmm_sgd(
        obs_set,
        out_set=None,
        hmm_state_count=5,
        append_lr=False,
        init_hmm_weights=None,
        init_lr_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):
    ''' Train an HMM with stochastic gradient descent:
        If we don't provide an out_set, then we just
        optimize the likelihood of the observations
        in obs_set.

        If append_lr, we may pass out_set and train and lr
        for prediction after hmm sgd. If append_lr is false
        but out_set is provided, hmm uses both in its cost
        function.
    '''

    obs_count = obs_set.shape[0]
    out_count = None
    if not out_set is None and not append_lr:
        out_count = out_set.shape[0]

    # Build the model
    outputs, loglike_fun, num_weights, print_weights = \
        hmm.build(obs_count, hmm_state_count, out_count)

    # Initializing the weights randomly, but making sure
    # that they still represent distributions, etc.
    if init_hmm_weights is None:
        init_hmm_weights = init_hmm_ffbs_weights(hmm_state_count, obs_count, flatten=True)

    if init_lr_weights is None:
        init_lr_weights = init_hmm_out_weights(hmm_state_count, out_count, param_scale)

    init_weights = np.hstack((init_hmm_weights, init_lr_weights))

    trained_weights = train_by_sgd(
        obs_set,
        loglike_fun,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    if append_lr:
        pred_fun, loglike_fun, trained_weights = \
            append_lr_to_model(obs_set,
                               out_set,
                               lffbs_weights,
                               outputs,
                               init_weights=None,
                               min_iters=min_iters,
                               max_iters=max_iters,
                               batch_size=batch_size,
                               param_scale=param_scale,
                               obs_lambda=obs_lambda,
                               l1_lambda=l1_lambda,
                               stop_criterion=stop_criterion,
                               early_stop=early_stop,
                               patience=patience,
                               va_obs_set=va_obs_set,
                               va_out_set=va_out_set)

        return pred_fun, loglike_fun, trained_weights

    return outputs, loglike_fun, trained_weights


def train_gru(
        obs_set,
        out_set,
        gru_state_count,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    pred_fun, loglike_fun, num_weights = gru.build(
        input_count, gru_state_count, output_count)

    trained_weights = train_by_sgd(
        obs_set,
        loglike_fun,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def train_gru_drop(
        obs_set,
        out_set,
        gru_state_count,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        max_conn=4,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    pred_fun, loglike_fun, num_weights = grudrop.build(
        input_count, gru_state_count, output_count, max_conn=max_conn)

    trained_weights = train_by_sgd(
        obs_set,
        loglike_fun,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def train_gru_redun(
        obs_set,
        out_set,
        gru_state_count,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        redun_epsilon=0.5,
        obs_lambda=0,
        l1_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    pred_fun, loglike_fun, num_weights = gruredun.build(
        input_count, gru_state_count, output_count, redun_epsilon)

    trained_weights = train_by_sgd(
        obs_set,
        loglike_fun,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def train_gru_hmm(
        obs_set,
        out_set,
        hmm_state_count,
        gru_state_count,
        init_gru_weights=None,
        init_hmm_weights=None,
        init_weights=None,
        min_iters=100,
        max_iters=100,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        max_conn=0,
        redun_epsilon=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    pred_fun, loglike_fun, num_gru_weights, num_hmm_weights = gruhmm.build(
        input_count,
        hmm_state_count,
        gru_state_count,
        output_count,
        max_conn=max_conn,
        redun_epsilon=redun_epsilon)

    if init_gru_weights is None:
        init_gru_weights = init_vanilla_gru_weights(gru_state_count,
                                                    input_count,
                                                    output_count,
                                                    param_scale)

    if init_hmm_weights is None:
        init_hmm_weights = np.hstack((
            init_hmm_ffbs_weights(hmm_state_count,
                                  input_count,
                                  flatten=True),
            init_hmm_out_weights(hmm_state_count,
                                 output_count,
                                 param_scale)))

    if init_weights:
        init_weights = np.hstack((init_gru_weights, init_hmm_weights))

    trained_weights = train_by_sgd(
        obs_set,
        loglike_fun,
        num_gru_weights + num_hmm_weights,
        out_set=out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_gru_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights
