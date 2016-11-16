"""
Similar file to early_stopping/optimize.py but
depends on converging vs early_stopping
"""

from __future__ import absolute_import

import autograd.numpy as np
from autograd.util import flatten_func
from builtins import range
from random import sample
from math import ceil
from copy import copy
from rlstm.scores import get_accuracy
import pdb

def adam(
        grad,
        init_params,
        num_batches=1,
        callback=None,
        min_iters=0,
        max_iters=1e5,
        step_size=0.001,
        b1=0.9,
        b2=0.999,
        eps=10**-8,
        ll_fun=None,
        va_ll_fun=None,
        stop_criterion=1e-3,
        early_stop=False,
        patience=10):
    """ Adam as described in http://arxiv.org/pdf/1412.6980.pdf.
    It's basically RMSprop with momentum and some correction terms."""

    flattened_grad, unflatten, x = flatten_func(grad, init_params)

    # initial settings for variables
    m, v = np.zeros(len(x)), np.zeros(len(x))
    reset_patience = patience

    # initialize loglikelihoods (these are used to determine convergence)
    # we define a single ll per batch so we know which to compare to.
    # Comparing ll between batches doesn't make sense.
    old_ll, cur_ll = np.ones(num_batches), np.zeros(num_batches)
    cur_va_ll, best_va_ll = None, None

    # training goes until all batches have converged / max_iter
    have_converged = np.zeros(num_batches)

    cur_iter = 0  # != epoch
    cur_batch = 0

    while (cur_iter < max_iters) or (cur_iter < min_iters):
        # we can test convergence for every batch and keep track
        # of which batches have converged
        if (np.abs(cur_ll[cur_batch] - old_ll[cur_batch]) <= stop_criterion):
            have_converged[cur_batch] = 1
        else:  # this should rarely fire
            have_converged[cur_batch] = 0

        # if all batches have converged before max_iter: break
        if sum(have_converged) == num_batches:
            break

        # pdb.set_trace()
        g = flattened_grad(x, cur_iter)  # pass iter for batch training
        m = (1 - b1) * g + b1 * m  # First  moment estimate.
        v = (1 - b2) * (g**2) + b2 * v  # Second moment estimate.
        mhat = m / (1 - b1**(cur_iter + 1))    # Bias correction.
        vhat = v / (1 - b2**(cur_iter + 1))
        x = x - step_size*mhat/(np.sqrt(vhat) + eps)

        if ll_fun:
            old_ll[cur_batch] = cur_ll[cur_batch]
            cur_ll[cur_batch] = ll_fun(x)

        if va_ll_fun:
            cur_va_ll = va_ll_fun(x)

            # stop based on va ll
            if early_stop:
                if cur_iter == 0:
                    best_va_ll = cur_va_ll
                    best_x = x
                else:
                    if cur_va_ll <= best_va_ll:
                        best_va_ll = cur_va_ll
                        best_x = x
                        patience = reset_patience
                    else:
                        patience -= 1

                if patience <= 0:
                    break

        if callback:
            callback(cur_iter // num_batches,
                     cur_batch,
                     cur_ll[cur_batch],
                     cur_va_ll,
                     patience if early_stop else None,
                     x)

        cur_iter += 1
        cur_batch = cur_iter % num_batches

    return unflatten(best_x if early_stop else x)
