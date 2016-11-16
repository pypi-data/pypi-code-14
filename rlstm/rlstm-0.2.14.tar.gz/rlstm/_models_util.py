from __future__ import print_function
from collections import defaultdict

import autograd.numpy as np
from autograd import value_and_grad, grad

from rlstm.optimize import adam
from rlstm import create_toy_data

from rlstm.models import lr, hmm, mlp, gru, gruhmm
from rlstm.nn_util import (reverse_sigmoid, init_hmm_ffbs_weights,
                     init_hmm_out_weights, init_vanilla_gru_weights)
from rlstm.common_util import (safe_log, flatten_to_2d, wrapper_func)
from rlstm.autograd_util import autograd_extract, is_autograd_array
from rlstm.scores import get_accuracy, get_mean_squared_error
from rlstm.interpret.rnn_tree import train_decision_tree

from copy import copy
import cPickle
import dill
import argparse
from datetime import datetime
import pdb  # remove me

# -- train functions --


def _train_by_sgd(
        obs_set,
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
    num_batches = int(np.ceil(obs_set.shape[-1] / float(batch_size)))

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
        def regularized_loss(weights, x, y):
            loss = loglike_fun(weights, x, y)
            if not y is None and obs_lambda > 0:
                ''' Add a parameter to balance between out log-likelihood and obs log-likelihood. '''
                loss += obs_lambda*loglike_fun(weights, x, None)
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
            batch_obs_set = obs_set[..., idx]
            batch_out_set = None if out_set is None else out_set[..., idx]
            return regularized_loss(
                weights, batch_obs_set, batch_out_set)

    # loss fnction against all data
    if collective_loss is None:
        def collective_loss(weights):
            return regularized_loss(weights, obs_set, out_set)

    if validation_loss is None:
        def validation_loss(weights):
            return regularized_loss(weights, va_obs_set, va_out_set)

    if callback is None:
        def callback(e_i, b_i, ll, va_ll, p, w):
            acc = error_func(
                out_set, np.exp(logpred_fun(w, obs_set))) if not out_set is None else None

            if not va_ll is None:
                va_acc = error_func(
                    va_out_set, np.exp(logpred_fun(w, va_obs_set))) if not va_out_set is None else None
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
