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

from __future__ import print_function
from collections import defaultdict

import autograd.numpy as np
from autograd import grad

from rlstm.optimize import adam
from rlstm.scores import get_accuracy
from rlstm.common_util import wrapper_func
from rlstm.models_util import train_by_sgd, train_mlp
from rlstm.interpret.rnn_tree import train_decision_tree
from rlstm.autograd_util import autograd_extract, is_autograd_array


def _dict_get(d, key, default=None):
    return d[key] if key in d else default


class BlackBoxTreeRegularizer(object):
    ''' Tree Regularization for any black box RLSTM model.
        Returns a MLP necessary for "tree based learning".
    '''

    def __init__(self):
        self.mlp_pred_fun = None
        self.mlp_loglike_fun = None
        self.mlp_weights = None

    def train_tree(self,
                   obs_set,
                   out_set,
                   bb_logpred_fun,
                   bb_loglike_fun,
                   bb_num_weights,
                   params={}):
        ''' Args
            ----
            obs_set : numpy array
            out_set : numpy array
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

        def bb_loss(weights, x, y):
            return bb_loglike_fun(weights, x, y)

        # train a tree + store stuff in the callback
        def callback(i, ll, va_ll, p, w):
            tree = train_decision_tree(bb_pred_fun, w, obs_set)
            weights_store[:, i] = w
            counts_store[:, i] = tree.tree_.node_count

            acc = get_accuracy(out_set, np.exp(bb_logpred_fun(w, obs_set))) \
                if not out_set is None else None

            if not va_ll is None:
                va_acc = get_accuracy(va_out_set, np.exp(bb_logpred_fun(w, va_obs_set))) \
                    if not va_out_set is None else None

                print('iter {}  |  training loss {}  |  training acc {}  |  validation loss {}  |  validation acc {}  |  patience {}'.format(
                    i, round(ll, 4), round(acc, 4) if acc else '--', round(va_ll, 4),
                    round(va_acc, 4) if va_acc else '--', p if p else '--'))
            else:
                print('iter {}  |  training loss {}  | training acc {}'.format(
                    i, round(ll, 4), round(acc, 4) if acc else '--'))

        trained_weights = train_by_sgd(
            obs_set,
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
