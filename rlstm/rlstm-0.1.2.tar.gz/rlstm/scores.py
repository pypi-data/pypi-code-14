
from __future__ import print_function

import autograd.numpy as np
from sklearn.metrics import auc, roc_curve

from rlstm.common_util import flatten_to_2d


def flatten_and_get_auc(dim_outputs, dim_probas):
    outputs = dim_outputs.flatten()
    probas = flatten_to_2d(dim_probas)
    return get_auc(outputs, probas)


def get_auc(outputs, probas):
    ''' AUC is a common metric for binary classification
        methods by comparing true & false positive rates

        Args
        ----
        outputs : numpy array of true outcomes (OxTxN)
        probas  : numpy array of predicted probabilities (OxTxN)
    '''

    fpr, tpr, _ = roc_curve(outputs, probas[:, 1])
    return auc(fpr, tpr)


def get_log_sparsity(weights, thres=1e-3):
    ''' Sparser weights are more interpretable.
        This returns a fraction of weights that are below
        a threshold.

        Args
        ----
        weights : numpy array of weights (1xW)
        thres   : float
    '''
    nonzero_count = np.sum(np.abs(weights) < thres)
    all_count = float(weights.shape[0])
    return nonzero_count / all_count


def get_pr_obs(ll_fun, weights, obs):
    ''' Given that it is important to model observations,
        not just outputs, then this tells us how well we
        can explain the observations.

        Args
        ----
        ll_fun  : function provided by one of the models in
                          this repo. Returns a lambda function
        weights : numpy array of weights (1xW)
        obs     : numpy array of inputs (IxTxN)
    '''
    return llfun(weights, obs)
