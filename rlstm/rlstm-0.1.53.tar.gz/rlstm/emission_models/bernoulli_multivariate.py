'''
Bernoulli Multivariate observation model

Parameters
----------
K : num states
D : num dimensions for each observation
eta_KD : NATURAL parameters
    eta_KD[k, d] = log odds ratio of observing dim d with cluster k
'''

import autograd.numpy as np
import sys
import os

from autograd.scipy.misc import logsumexp

def init_natural_param_dict_from_data(
        data_ND, K=1, n_states=None, seed=0):
    '''
    '''
    prng = np.random.RandomState(int(seed))
    if n_states is not None:
        K = int(n_states)
    else:
        K = int(K)
    D = data_ND.shape[1]
    eta_KD = prng.randn(K, D)
    return dict(
        eta_KD=eta_KD)

def eta2mu(eta_KD):
    ''' Convert mean to natural parameters

    Returns
    -------
    mu_KD : 2D array, K x D

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> eta = np.asarray([-4, -1, 0, 1, 4])
    >>> print eta2mu(eta)
    [ 0.018  0.269  0.5    0.731  0.982]
    '''
    return 1.0 / (1.0 + np.exp(-eta_KD))

def mu2eta(mu_KD):
    ''' Convert mean to natural parameters

    Returns
    -------
    eta_KD : 2D array, K x D

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> mu = np.asarray([0.018, 0.269, 0.5, 0.731, 0.982])
    >>> print mu2eta(mu)
    [-3.999 -1.     0.     1.     3.999]
    '''
    mu_KD = np.maximum(np.minimum(mu_KD, 0.99999), 0.00001)
    return np.log( mu_KD / (1 - mu_KD) )


def calc_log_proba_data_arr_NK(data_ND, eta_KD=None, mu_KD=None, **kwargs):
    ''' Compute log probability of each dataset observation under each cluster

    Args
    ----
    data_ND : 2D array, n_examples x n_dims, with binary values
        data_ND[n, d] = 1 if dimension d is ON for observation n
    eta_KD : 2D array, n_states x n_dims, with real values
        log odds ratio for observing ON value under cluster k and dim d
        not needed if mu_KD provided
    mu_KD : 2D array, n_states x n_dims, with values 0 < mu < 1
        probability of observing ON value under cluster k and dim d

    Returns
    -------
    log_proba_NK : 2D array, n_examples x n_states, with real values
        entry n,k gives log probability of data row n under state k

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> data_ND = np.asarray([[0], [1]])
    >>> mu_KD = np.asarray([[0.8], [0.1]])
    >>> log_proba_NK_v1 = calc_log_proba_data_arr_NK(
    ...     data_ND, mu_KD=mu_KD)
    >>> log_proba_NK_v2 = calc_log_proba_data_arr_NK(
    ...     data_ND, eta_KD=mu2eta(mu_KD))

    # Verify that the log probas are < 0
    >>> assert np.all(log_proba_NK_v1 < 0)

    # Verify that the log probas sum to 1 across 0 and 1
    >>> assert np.allclose(1.0, np.sum(np.exp(log_proba_NK_v1), axis=0))

    # Verify two methods are the same
    >>> assert np.allclose(log_proba_NK_v1, log_proba_NK_v2)

    >>> prng = np.random.RandomState(0)
    >>> big_data_ND = prng.rand(100, 3) > 0.3
    >>> mu_KD = prng.rand(2, 3)
    >>> log_proba_NK_v1 = calc_log_proba_data_arr_NK(
    ...     big_data_ND, mu_KD=mu_KD)
    >>> log_proba_NK_v2 = calc_log_proba_data_arr_NK(
    ...     big_data_ND, eta_KD=mu2eta(mu_KD))

    # Verify two methods are the same
    >>> assert np.allclose(log_proba_NK_v1, log_proba_NK_v2)
    '''
    if mu_KD is not None:
        # Using mean parameter
        log_mu_KD = np.log(mu_KD)
        log_1minus_mu_KD = np.log(1 - mu_KD)
        log_proba_NK = np.dot(data_ND, log_mu_KD.T)
        log_proba_NK += np.dot(1 - data_ND, log_1minus_mu_KD.T)
    else:
        # Using natural parameter
        log_cumulant_K = np.sum(np.log(1 - eta2mu(eta_KD)), axis=1)
        log_proba_NK = np.dot(data_ND, eta_KD.T)
        log_proba_NK += log_cumulant_K[np.newaxis, :]
    return log_proba_NK
