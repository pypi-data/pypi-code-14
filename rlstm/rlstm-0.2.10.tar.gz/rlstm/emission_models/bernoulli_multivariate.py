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
import pdb

from autograd.scipy.misc import logsumexp

def init_natural_param_dict_from_data(
        data_DN, K=1, n_states=None, seed=0):
    '''
    '''
    prng = np.random.RandomState(int(seed))
    if n_states is not None:
        K = int(n_states)
    else:
        K = int(K)
    D = data_DN.shape[0]
    eta_DK = prng.randn(K, D).T
    return dict(
        eta_DK=eta_DK)


def init_natural_param_array_from_data(
        data_DN, K=1, n_states=None, seed=0):
    prng = np.random.RandomState(int(seed))
    if n_states is not None:
        K = int(n_states)
    else:
        K = int(K)
    D = data_DN.shape[0]
    eta_DK = prng.randn(K, D).T
    return eta_DK


def eta2mu(eta_DK):
    ''' Convert mean to natural parameters

    Returns
    -------
    mu_DK : 2D array, D x K

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> eta = np.asarray([-4, -1, 0, 1, 4])
    >>> print eta2mu(eta)
    [ 0.018  0.269  0.5    0.731  0.982]
    '''
    return 1.0 / (1.0 + np.exp(-eta_DK))

def mu2eta(mu_DK):
    ''' Convert mean to natural parameters

    Returns
    -------
    eta_DK : 2D array, D x K

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> mu = np.asarray([0.018, 0.269, 0.5, 0.731, 0.982])
    >>> print mu2eta(mu)
    [-3.999 -1.     0.     1.     3.999]
    '''
    mu_DK = np.maximum(np.minimum(mu_DK, 0.99999), 0.00001)
    return np.log( mu_DK / (1 - mu_DK) )


def calc_log_proba_data_arr_NK(data_DN, eta_DK=None, mu_DK=None, **kwargs):
    ''' Compute log probability of each dataset observation under each cluster

    Args
    ----
    data_DN : 2D array, n_dims x n_examples, with binary values
        data_ND[n, d] = 1 if dimension d is ON for observation n
    eta_DK : 2D array, n_dims x n_states , with real values
        log odds ratio for observing ON value under cluster k and dim d
        not needed if mu_KD provided
    mu_DK : 2D array, n_dims x n_states, with values 0 < mu < 1
        probability of observing ON value under cluster k and dim d

    Returns
    -------
    log_proba_NK : 2D array, n_examples x n_states, with real values
        entry n,k gives log probability of data row n under state k

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> data_DN = np.asarray([[0, 1]])
    >>> mu_DK = np.asarray([[0.8, 0.1]])
    >>> log_proba_NK_v1 = calc_log_proba_data_arr_NK(
    ...     data_DN, mu_DK=mu_DK)
    >>> log_proba_NK_v2 = calc_log_proba_data_arr_NK(
    ...     data_DN, eta_DK=mu2eta(mu_DK))

    # Verify that the log probas are < 0
    >>> assert np.all(log_proba_NK_v1 < 0)

    # Verify that the log probas sum to 1 across 0 and 1
    >>> assert np.allclose(1.0, np.sum(np.exp(log_proba_NK_v1), axis=0))

    # Verify two methods are the same
    >>> assert np.allclose(log_proba_NK_v1, log_proba_NK_v2)

    >>> prng = np.random.RandomState(0)
    >>> big_data_DN = prng.rand(3, 100) > 0.3
    >>> mu_DK = prng.rand(3, 2)
    >>> log_proba_NK_v1 = calc_log_proba_data_arr_NK(
    ...     big_data_DN, mu_DK=mu_DK)
    >>> log_proba_NK_v2 = calc_log_proba_data_arr_NK(
    ...     big_data_DN, eta_DK=mu2eta(mu_DK))

    # Verify two methods are the same
    >>> assert np.allclose(log_proba_NK_v1, log_proba_NK_v2)
    '''
    if mu_DK is not None:
        # Using mean parameter
        log_mu_DK = np.log(mu_DK)
        log_1minus_mu_DK = np.log(1 - mu_DK)
        log_proba_NK = np.dot(data_DN.T, log_mu_DK)
        log_proba_NK += np.dot(1 - data_DN.T, log_1minus_mu_DK)
    else:
        # Using natural parameter
        log_cumulant_K = np.sum(np.log(1 - eta2mu(eta_DK)), axis=0)
        log_proba_NK = np.dot(data_DN.T, eta_DK)
        log_proba_NK += log_cumulant_K[np.newaxis, :]
    return log_proba_NK
