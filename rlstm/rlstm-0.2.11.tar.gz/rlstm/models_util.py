from __future__ import print_function
from collections import defaultdict

import autograd.numpy as np
from autograd import value_and_grad, grad

from rlstm.optimize import adam
from rlstm import create_toy_data

from rlstm.models import lr, hmm, mlp, gru, gruhmm
from rlstm.interpret.rnn_tree import train_decision_tree

from rlstm.nn_util import (reverse_sigmoid, init_hmm_ffbs_weights,
                     init_hmm_out_weights, init_vanilla_gru_weights)
from rlstm.common_util import (safe_log, flatten_to_2d, wrapper_func, map_3d_to_2d)
from rlstm.scores import get_accuracy, get_mean_squared_error
from rlstm.autograd_util import autograd_extract, is_autograd_array

from copy import copy
import cPickle
import dill
import argparse
from datetime import datetime

import pdb  # remove me

# -- train functions --


def train_by_sgd(
        obs_set,
        fence_set,
        loglike_fun,
        logpred_fun,
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
        l2_lambda=0,
        num_l1_weights=0,
        num_l2_weights=0,
        # optimization
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        regression=False,
        # validation set
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None,
        # overwrite functions
        batch_indices=None,
        regularized_loss=None,
        batch_loss=None,
        collective_loss=None,
        validation_loss=None,
        callback=None):
    ''' Generic function for training using stochastic gradient descent.
        All models are wrapped around this function.
    '''

    # assume the *num_data* is always last index
    num_data = len(fence_set) - 1
    num_batches = int(np.ceil(num_data / float(batch_size)))

    if init_weights is None:
        init_weights = np.random.randn(num_weights) * param_scale

    # choose the proper error function
    error_func = get_mean_squared_error if regression else get_accuracy

    if batch_indices is None:
        def batch_indices(iter):
            idx = iter % num_batches
            return slice(idx * batch_size, (idx+1) * batch_size)

    # wrapper around loss function
    if regularized_loss is None:
        def regularized_loss(weights, obs_set, fence_set, out_set):
            loss = loglike_fun(weights, obs_set, fence_set, out_set)
            if not out_set is None and obs_lambda > 0:
                ''' Add a parameter to balance between out log-likelihood and obs log-likelihood. '''
                loss += obs_lambda*loglike_fun(weights, obs_set, fence_set, None)
            loss = -loss

            ''' Add a l1 regularizer to zero-out large weights '''
            if l1_lambda > 0:
                loss += l1_lambda * np.sum(np.abs(weights[:num_l1_weights]))

            ''' Add a l2 regularizer to penalize large weights '''
            if l2_lambda > 0:
                loss += l2_lambda * np.sum(np.power(weights[:num_l2_weights], 2))
            return loss

    # loss function in batches
    if batch_loss is None:
        def batch_loss(weights, iter):
            idx = batch_indices(iter)

            # find the relevant fence posts
            batch_i = np.arange(num_data)[idx]
            batch_fence_set = np.unique(np.concatenate((fence_set[batch_i], fence_set[batch_i+1])))

            # use the fence sets to get batch obs/out set
            batch_out_set = None
            for i in range(batch_i.size):
                if i == 0:
                    batch_obs_set = obs_set[:, batch_fence_set[i]:batch_fence_set[i+1]]
                    if not out_set is None:
                        batch_out_set = out_set[:, batch_fence_set[i]:batch_fence_set[i+1]]
                else:
                    cur_batch_obs_set = obs_set[:, batch_fence_set[i]:batch_fence_set[i+1]]
                    batch_obs_set = np.hstack((batch_obs_set, cur_batch_obs_set))
                    if not out_set is None:
                        cur_batch_out_set = out_set[:, batch_fence_set[i]:batch_fence_set[i+1]]
                        batch_out_set = np.hstack((batch_out_set, cur_batch_out_set))

            return regularized_loss(weights, batch_obs_set, batch_fence_set, batch_out_set)

    # loss fnction against all data
    if collective_loss is None:
        def collective_loss(weights):
            return regularized_loss(weights, obs_set, fence_set, out_set)

    if validation_loss is None:
        def validation_loss(weights):
            return regularized_loss(weights, va_obs_set, va_fence_set, va_out_set)

    if callback is None:
        def callback(e_i, b_i, ll, va_ll, p, w):
            acc = error_func(out_set, np.exp(logpred_fun(w, obs_set, fence_set))) \
                if not out_set is None else None

            if not va_ll is None:
                va_acc = error_func(va_out_set, np.exp(logpred_fun(w, va_obs_set, va_fence_set))) \
                    if not va_out_set is None else None

                print('epoch {}  |  batch {}  |  training loss {}  |  training acc {}  |  validation loss {}  |  validation acc {}  |  patience {}'.format(
                    e_i, b_i, round(ll, 4), round(acc, 4) if acc else '--', round(va_ll, 4),
                    round(va_acc, 4) if va_acc else '--', p if p else '--'))
            else:
                print('epoch {}  |  batch {}  |  training loss {}  | training acc {}'.format(
                    e_i, b_i, round(ll, 4), round(acc, 4) if acc else '--'))

    grad_fun = grad(batch_loss)
    weights = adam(grad_fun,
                   init_weights,
                   step_size=0.001,
                   num_batches=num_batches,
                   min_iters=min_iters,
                   max_iters=max_iters,
                   callback=callback,
                   ll_fun=collective_loss,
                   stop_criterion=stop_criterion,
                   va_ll_fun=validation_loss if not va_obs_set is None else None,
                   early_stop=early_stop,
                   patience=patience)

    return weights


def train_lr(
        obs_set,
        fence_set,
        out_set,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.0001,
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None):

    in_dim_count = obs_set.shape[0]
    out_dim_count = out_set.shape[0]

    num_weights = np.prod((out_dim_count, in_dim_count + 1))
    loglike_fun = lr.log_likelihood
    logpred_fun = lambda weights, obs_set, fence_set: lr.logistic_log_predictions(
        weights, obs_set, fence_set, in_dim_count, out_dim_count)
    pred_fun = wrapper_func(logpred_fun, np.exp)

    trained_weights = train_by_sgd(
        obs_set,
        fence_set,
        lr.log_likelihood,
        logpred_fun,
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
        num_l2_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_fence_set=va_fence_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def append_lr_to_model(
        obs_set,
        fence_set,
        out_set,
        hmm_weights,
        output_fun,
        loglike_fun,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.0001,
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None):
    ''' Often we train a generative model for an hmm but want to
        tag an lr afterwards. This is wrapper function around train_lr
        to do so.
    '''

    num_hmm_weights = hmm_weights.shape[0]
    _, lprob_set = hmm.get_state_prob_set(
        output_fun, hmm_weights, obs_set, fence_set)

    va_lprob_set = None
    if not va_obs_set is None:
        _, va_lprob_set = hmm.get_state_prob_set(
            output_fun, hmm_weights, va_obs_set, va_fence_set)

    # train lr
    logpred_fun, ll_fun, lr_weights = train_lr(lprob_set,
                                               fence_set,
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
                                               va_obs_set=va_lprob_set,
                                               va_fence_set=va_fence_set,
                                               va_out_set=va_out_set)

    trained_weights = np.hstack((hmm_weights, lr_weights))

    # return functions so users can pass in obs_farray (instead of prob_farray)
    def all_logpred_fun(weights, obs_set, fence_set):
        _, lprob_set = hmm.get_state_prob_set(
            output_fun, weights, obs_set, fence_set)
        hmm_weights = weights[:num_hmm_weights]
        lr_weights = weights[num_hmm_weights:]
        return logpred_fun(lr_weights, lprob_set, fence_set)

    def all_loglike_fun(weights, obs_set, fence_set, out_set=None):
        ''' if out_farray, use lr proba; else use hmm proba
        '''

        # we know but exist (but just may want to use one)
        hmm_weights = weights[:num_hmm_weights]
        lr_weights = weights[num_hmm_weights:]

        if not out_set is None:
            _, lprob_set = hmm.get_state_prob_set(
                output_fun, hmm_weights, obs_set, fence_set)
            return ll_fun(lr_weights, lprob_set, fence_set, out_set)
        else:
            return loglike_fun(hmm_weights, obs_set, fence_set)

    return all_logpred_fun, all_loglike_fun, trained_weights


def train_hmm_sgd(
        obs_set,
        fence_set,
        out_set,
        hmm_state_count=5,
        emission_type='bernoulli',
        obs_only=False,
        init_hmm_weights=None,
        init_lr_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None):
    ''' Train an HMM with stochastic gradient descent:
        If obs_only, then we just optimize the likelihood
        of the observations in obs_farray. Otherwise, the out_farray
        is provided, and the hmm uses both in its cost function.
    '''

    obs_count = obs_set.shape[0]
    out_count = None
    if not obs_only:
        out_count = out_set.shape[0]

    # Build the model
    outputs, loglike_fun, num_weights = hmm.build(
        obs_count, hmm_state_count, out_count, emission_type=emission_type)

    # Initializing the weights randomly, but making sure
    # that they still represent distributions, etc.
    if init_hmm_weights is None:
        init_hmm_weights = init_hmm_emission_weights(
            hmm_state_count, obs_count, flatten=False,
                                        emission_type=emission_type)

    if init_lr_weights is None:
        init_lr_weights = init_hmm_out_weights(
            hmm_state_count, out_set.shape[0], param_scale)

    if not obs_only:
        init_weights = np.hstack((init_hmm_weights, init_lr_weights))
    else:
        init_weights = init_hmm_weights

    trained_weights = train_by_sgd(
        obs_set,
        fence_set,
        loglike_fun,
        outputs,
        num_weights,
        out_set=None if obs_only else out_set,
        init_weights=init_weights,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        obs_lambda=obs_lambda,
        l1_lambda=l1_lambda,
        num_l1_weights=num_weights,
        num_l2_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_fence_set=va_fence_set,
        va_out_set=va_out_set)

    if obs_only:
        logpred_fun, loglike_fun, trained_weights = \
            append_lr_to_model(obs_set,
                               fence_set,
                               out_set,
                               trained_weights,
                               outputs,
                               loglike_fun,
                               init_weights=init_lr_weights,
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
                               va_fence_set=va_fence_set,
                               va_out_set=va_out_set)

        pred_fun = wrapper_func(logpred_fun, np.exp)
        return pred_fun, loglike_fun, trained_weights

    return outputs, loglike_fun, trained_weights


def train_mlp(
        obs_set,
        out_set,
        states_list,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_out_set=None):

    from _models_util import _train_by_sgd
    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    logpred_fun, loglike_fun, num_weights = mlp.build(
        input_count, states_list, output_count)
    pred_fun = wrapper_func(logpred_fun, np.exp)

    trained_weights = _train_by_sgd(
        obs_set,
        loglike_fun,
        logpred_fun,
        num_weights,
        out_set=out_set,
        init_weights=init_weights,
        regression=True,
        min_iters=min_iters,
        max_iters=max_iters,
        batch_size=batch_size,
        param_scale=param_scale,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def train_gru(
        obs_set,
        fence_set,
        out_set,
        gru_state_count,
        init_weights=None,
        min_iters=100,
        max_iters=500,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        max_conn=0,
        redun_epsilon=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    logpred_fun, loglike_fun, num_weights = gru.build(
        input_count, gru_state_count, output_count,
        max_conn=max_conn, redun_epsilon=redun_epsilon)

    pred_fun = wrapper_func(logpred_fun, np.exp)

    trained_weights = train_by_sgd(
        obs_set,
        fence_set,
        loglike_fun,
        logpred_fun,
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
        num_l2_weights=num_weights,
        stop_criterion=stop_criterion,
        early_stop=early_stop,
        patience=patience,
        va_obs_set=va_obs_set,
        va_fence_set=va_fence_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


def train_gru_hmm(
        obs_set,
        fence_set,
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
        l2_lambda=0,
        max_conn=0,
        redun_epsilon=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None):

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    logpred_fun, loglike_fun, num_gru_weights, num_hmm_weights = gruhmm.build(
        input_count,
        hmm_state_count,
        gru_state_count,
        output_count,
        max_conn=max_conn,
        redun_epsilon=redun_epsilon)

    pred_fun = wrapper_func(logpred_fun, np.exp)

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

    if init_weights is None:
        init_weights = np.hstack((init_gru_weights, init_hmm_weights))

    trained_weights = train_by_sgd(
        obs_set,
        fence_set,
        loglike_fun,
        logpred_fun,
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
        va_fence_set=va_fence_set,
        va_out_set=va_out_set)

    return pred_fun, loglike_fun, trained_weights


# ---------------------------------------------------------------------------
# Exploratory code Tree Regularization


def _dict_get(d, key, default=None):
    return d[key] if key in d else default


class BlackBoxTreeRegularizer(object):
    ''' Add a wrapper function to regularize a black-box model using
        a WEIGHT-NODE tree mapping.

        In order for the tree to be differentiable, an MLP is trained to
        approximate the tree's WEIGHT-NODE function. The MLP is should be
        differentiated inside the model's cost function.

        This model will take return the following items:
            - tree (final iteration of the tree)
            - MLP (MLP weights)

        The black box model is assumed to have the following design:
            - prediction function: accepts (weights, inputs) and returns proba
            - log_likelihood function: accepts (weights, inputs, outputs)
                                       and returns likelihood

    '''

    def __init__(self):
        self.mlp_pred_fun = None
        self.mlp_loglike_fun = None
        self.mlp_weights = None

    def train_tree(self,
                   obs_set,
                   fence_set,
                   out_set,
                   bb_logpred_fun,
                   bb_loglike_fun,
                   bb_num_weights,
                   params={}):
        ''' Args
            ----
            obs_farray : numpy array
            out_farray : numpy array
            bb_logpred_fun : lambda function
                             rlstm.models object
            bb_loglike_fun : lambda function
                             rlstm.models object
        '''
        input_count = obs_set.shape[0]
        output_count = out_set.shape[0]
        bb_pred_fun = wrapper_func(bb_logpred_fun, np.exp)

        weights_store = np.zeros((bb_num_weights, _dict_get(params, 'max_iters', 10000)))
        counts_store = np.zeros((1, _dict_get(params, 'max_iters', 10000)))
        batch_size = _dict_get(params, 'batch_size', 128)

        num_data = len(fence_set) + 1
        num_batches = int(np.ceil(num_data / float(batch_size)))

        def bb_loss(weights, obs_set, fence_set, out_set):
            return bb_loglike_fun(weights, obs_set, fence_set, out_set)

        # train a tree + store stuff in the callback
        def callback(e_i, b_i, ll, va_ll, p, w):
            iter_i = e_i * num_batches + b_i
            tree = train_decision_tree(bb_pred_fun, w, obs_set, fence_set)
            weights_store[:, iter_i] = w
            counts_store[:, iter_i] = tree.tree_.node_count

            acc = get_accuracy(out_set, np.exp(bb_logpred_fun(w, obs_set, fence_set))) \
                if not out_set is None else None

            if not va_ll is None:
                va_acc = get_accuracy(va_out_set, np.exp(bb_logpred_fun(w, va_obs_set, va_fence_set))) \
                    if not va_out_set is None else None

                print('epoch {}  |  batch {}  |  training loss {}  |  training acc {}  |  validation loss {}  |  validation acc {}  |  patience {}'.format(
                    e_i, b_i, round(ll, 4), round(acc, 4) if acc else '--', round(va_ll, 4),
                    round(va_acc, 4) if va_acc else '--', p if p else '--'))
            else:
                print('epoch {}  |  batch {}  |  training loss {}  | training acc {}'.format(
                    e_i, b_i, round(ll, 4), round(acc, 4) if acc else '--'))

        trained_weights = train_by_sgd(
            obs_set,
            fence_set,
            bb_loss,
            bb_logpred_fun,
            bb_num_weights,
            out_set=out_set,
            min_iters=_dict_get(params, 'min_iters', 100),
            max_iters=_dict_get(params, 'max_iters', 10000),
            batch_size=_dict_get(params, 'batch_size', 64),
            param_scale=_dict_get(params, 'param_scale', 0.01),
            l1_lambda=_dict_get(params, 'l1_lambda', 0),
            l2_lambda=_dict_get(params, 'l2_lambda', 0),
            num_l1_weights=bb_num_weights,
            num_l2_weights=bb_num_weights,
            stop_criterion=_dict_get(params, 'stop_criterion', 1e-3),
            callback=callback
        )

        return weights_store, counts_store

    def train_mlp(self, weights, counts, num_hiddens, params={}):
        pred_fun, loglike_fun, trained_weights = train_mlp(
            weights,
            counts,
            num_hiddens,
            min_iters=_dict_get(params, 'min_iters', 100),
            max_iters=_dict_get(params, 'max_iters', 10000),
            batch_size=_dict_get(params, 'batch_size', 64),
            param_scale=_dict_get(params, 'param_scale', 0.01),
            stop_criterion=_dict_get(params, 'stop_criterion', 1e-3)
        )

        self.mlp_pred_fun = pred_fun
        self.mlp_loglike_fun = loglike_fun
        self.mlp_weights = trained_weights


def train_gru_hmm_tree(
        obs_set,
        fence_set,
        out_set,
        hmm_state_count,
        gru_state_count,
        init_gru_weights=None,
        init_hmm_weights=None,
        init_weights=None,
        min_iters=100,
        max_iters=100,
        mlp_min_iters=100,
        mlp_max_iters=1000,
        batch_size=128,
        param_scale=0.01,
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        tree_lambda=0,
        max_conn=0,
        redun_epsilon=0,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        va_obs_set=None,
        va_fence_set=None,
        va_out_set=None,
        # pretrained tree regressor
        tree_mlp_pred_fun=None,
        tree_mlp_loglike_fun=None,
        tree_mlp_weights=None,
        tree_mlp_output_loc=None):
    ''' Same as train_gru_hmm except a decision tree approximator is added
        to predict a number of nodes that acts as a regularization technique.
    '''

    input_count = obs_set.shape[0]
    output_count = out_set.shape[0]

    # Build the model
    logpred_fun, loglike_fun, num_gru_weights, num_hmm_weights = gruhmm.build(
        input_count,
        hmm_state_count,
        gru_state_count,
        output_count,
        max_conn=max_conn,
        redun_epsilon=redun_epsilon)

    pred_fun = wrapper_func(logpred_fun, np.exp)

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

    if init_weights is None:
        init_weights = np.hstack((init_gru_weights, init_hmm_weights))

    # -------------------------------------------------------
    # initialize a regularizer accent
    if tree_mlp_pred_fun is None and tree_mlp_weights is None:
        treg = BlackBoxTreeRegularizer()
        _gru_logpred_fun, _gru_loglike_fun, _gru_num_weights = gru.build(
            input_count, gru_state_count, output_count)
        print('[{}] training regularization tree'.format(datetime.now()))
        tree_weights, tree_counts = treg.train_tree(
                                        obs_set,
                                        fence_set,
                                        out_set,
                                        _gru_logpred_fun,
                                        _gru_loglike_fun,
                                        _gru_num_weights,
                                        params={'min_iters':min_iters,
                                                'max_iters':max_iters,
                                                'batch_size':batch_size,
                                                'param_scale':param_scale,
                                                'stop_criterion':stop_criterion,
                                                'l1_lambda':l1_lambda,
                                                'l2_lambda':l2_lambda})

        # get rid of any excess examples
        tree_num_real = np.where(tree_counts == 0)[1]
        if tree_num_real.size > 0:
            tree_num_real = tree_num_real[0]
            tree_weights = tree_weights[:, :tree_num_real]
            tree_counts = tree_counts[:, :tree_num_real]

        print('[{}] training regularization perceptron'.format(datetime.now()))
        treg.train_mlp(tree_weights,
                       tree_counts,
                       [100],
                       params={'min_iters':mlp_min_iters,
                               'max_iters':mlp_max_iters,
                               'batch_size':batch_size,
                               'param_scale':param_scale,
                               'stop_criterion':stop_criterion})
        tree_mlp_pred_fun = treg.mlp_pred_fun
        tree_mlp_loglike_fun = treg.mlp_loglike_fun
        tree_mlp_weights = treg.mlp_weights

        if not tree_mlp_output_loc is None:
            with open(tree_mlp_output_loc, 'w') as fp:
                tree_snapshot = {'pred_fun':tree_mlp_pred_fun,
                                 'loglike_fun':tree_mlp_loglike_fun,
                                 'weights':tree_mlp_weights}
                dill.dump(tree_snapshot, fp)

    # -------------------------------------------------------

    # Overwrite the regularized loss function in train_by_sgd to include
    # the tree regularization.
    def regularized_loss(weights, obs_set, fence_set, out_set):
        loss = loglike_fun(weights, obs_set, fence_set, out_set)
        if not out_set is None and obs_lambda > 0:
            loss += obs_lambda*loglike_fun(weights, obs_set, fence_set, None)
        loss = -loss
        if l1_lambda > 0:
            loss += l1_lambda * np.sum(np.abs(weights[:num_gru_weights]))
        if l2_lambda > 0:
            loss += l2_lambda * np.sum(np.power(weights[:num_gru_weights], 2))
        if tree_lambda > 0:
            # rarely MLP could predict < 0 (which makes no sense)
            # b/c we log then re-exp, < 0 --> nan
            tree_mlp_pred = tree_mlp_pred_fun(tree_mlp_weights, weights[:num_gru_weights])
            if np.isnan(tree_mlp_pred):
                tree_mlp_pred = 0
            loss += tree_lambda * np.sum(tree_mlp_pred)
        return loss


    print('[{}] training gru-hmm'.format(datetime.now()))
    trained_weights = train_by_sgd(
        obs_set,
        fence_set,
        loglike_fun,
        logpred_fun,
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
        va_fence_set=va_fence_set,
        va_out_set=va_out_set,
        regularized_loss=regularized_loss)

    return (pred_fun, tree_mlp_pred_fun), \
           (loglike_fun, tree_mlp_loglike_fun), \
           (trained_weights, tree_mlp_weights)
