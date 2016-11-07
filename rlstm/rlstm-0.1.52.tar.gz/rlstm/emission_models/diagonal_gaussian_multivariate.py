'''
Gaussian Multivariate observation model, with unknown mean and diag covariance.

Parameters
----------
K : num states
D : num dimensions for each observation

mu_KD : mean position for cluster k at dimension d
stddev_KD : standard deviation for cluster k at dimension d
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
    mu_KD = prng.randn(K, D)
    stddev_KD = 0.1 + 0.1 * prng.rand(K, D)
    return mu2eta(
        mu_KD=mu_KD,
        stddev_KD=stddev_KD)

def eta2mu(eta_mu_KD=None, eta_stddev_KD=None, eps=0.00001, **kwargs):
    ''' Convert unconstrained to mean parameters

    Returns
    -------
    mu_KD : 2D array, K x D
    stddev_KD : 2D array, K x D
    '''
    mu_KD = eta_mu_KD
    stddev_KD = eps + np.log(1.0 + np.exp(eta_stddev_KD))
    return dict(mu_KD=mu_KD, stddev_KD=stddev_KD)


def mu2eta(mu_KD=None, stddev_KD=None, eps=0.00001, **kwargs):
    ''' Convert mean to unconstrained parameters

    Returns
    -------
    eta_mu_KD : 2D array, K x D
    eta_stddev_KD : 2D array, K x D

    Examples
    --------
    >>> np.set_printoptions(suppress=1, precision=3)
    >>> mu_KD = np.zeros((1, 4))
    >>> stddev_KD = np.asarray([[0.1, 0.5, 1.0, 9.0]])
    >>> eta_dict = mu2eta(mu_KD=mu_KD, stddev_KD=stddev_KD)
    >>> print eta_dict['eta_mu_KD']
    [[ 0.  0.  0.  0.]]
    >>> print eta_dict['eta_stddev_KD']
    [[-2.252 -0.433  0.541  9.   ]]

    # Verify invertibility. If we transform then invert, we get original input.
    >>> mu_dict = eta2mu(**eta_dict)
    >>> np.allclose(mu_dict['mu_KD'], mu_KD)
    True
    >>> np.allclose(mu_dict['stddev_KD'], stddev_KD)
    True
    '''
    eta_mu_KD = mu_KD
    stddev_KD = np.maximum(stddev_KD, eps)
    eta_stddev_KD = np.log(np.exp(stddev_KD - eps) - 1.0)
    return dict(eta_mu_KD=eta_mu_KD, eta_stddev_KD=eta_stddev_KD)

def calc_log_proba_data_arr_NK(
        data_ND,
        mu_KD=None,
        stddev_KD=None,
        eta_mu_KD=None,
        eta_stddev_KD=None,
        **kwargs):
    ''' Compute log probability of each dataset observation under each cluster

    Args
    ----
    data_ND : 2D array, n_examples x n_dims, with real values
        data_ND[n, d] = observed value for observation n's d-th dimension
    mu_KD : 2D array, n_states x n_dims, with real values 

    Returns
    -------
    log_proba_NK : 2D array, n_examples x n_states, with real values
        entry n,k gives log probability of data row n under state k

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> prng = np.random.RandomState(0)

    # Verify the log proba calc is correct (integrates to unity)
    >>> data_ND = np.linspace(-5, 5, 100)[:,np.newaxis]
    >>> mu_KD = np.asarray([[0.0], [1.0]])
    >>> stddev_KD = np.asarray([[1.0], [0.5]])
    >>> log_proba_NK = calc_log_proba_data_arr_NK(
    ...     data_ND, mu_KD=mu_KD, stddev_KD=stddev_KD)
    >>> assert log_proba_NK.ndim == 2
    >>> sum_proba_1 = np.trapz(np.exp(log_proba_NK[:,0]), data_ND[:,0])
    >>> np.allclose(1.0, sum_proba_1)
    True
    >>> sum_proba_2 = np.trapz(np.exp(log_proba_NK[:,1]), data_ND[:,0])
    >>> np.allclose(1.0, sum_proba_2)
    True
    '''
    N = data_ND.shape[0]
    if eta_mu_KD is not None:
        mu_dict = eta2mu(eta_mu_KD=eta_mu_KD, eta_stddev_KD=eta_stddev_KD)
        mu_KD = mu_dict['mu_KD']
        stddev_KD = mu_dict['stddev_KD']

    K, D = mu_KD.shape
    log_proba_list = list()
    for k in xrange(K):
        var_k_D = np.square(stddev_KD[k])
        arr_k_ND = data_ND - mu_KD[k]
        arr_k_ND = np.square(arr_k_ND)
        arr_k_ND = arr_k_ND / var_k_D
        mahal_dist_k_N = np.sum(arr_k_ND, axis=1)
        log_proba_list.append(
            - 0.5 * D * np.log(2 * np.pi) 
            - 0.5 * mahal_dist_k_N
            - np.sum(np.log(stddev_KD[k])))
    log_proba_NK = np.vstack(log_proba_list).T
    return log_proba_NK