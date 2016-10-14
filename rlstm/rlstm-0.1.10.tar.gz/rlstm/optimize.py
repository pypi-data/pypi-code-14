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


def adam(
        grad,
        init_params,
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
    cur_iter = 0
    reset_patience = patience
    old_ll, cur_ll, cur_va_ll, best_va_ll = 1, 0, None, None

    while ((cur_iter < max_iters) and (np.abs(cur_ll - old_ll) > stop_criterion)) \
            or (cur_iter < min_iters):

        g = flattened_grad(x, cur_iter)  # pass iter for batch training
        m = (1 - b1) * g + b1 * m  # First  moment estimate.
        v = (1 - b2) * (g**2) + b2 * v  # Second moment estimate.
        mhat = m / (1 - b1**(cur_iter + 1))    # Bias correction.
        vhat = v / (1 - b2**(cur_iter + 1))
        x = x - step_size*mhat/(np.sqrt(vhat) + eps)

        # measure convergence
        if ll_fun:
            old_ll = cur_ll
            cur_ll = ll_fun(x)

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
            if early_stop:
                callback(cur_iter, cur_ll, cur_va_ll, patience)
            else:
                callback(cur_iter, cur_ll, cur_va_ll)

        cur_iter += 1
    return unflatten(best_x if early_stop else x)
