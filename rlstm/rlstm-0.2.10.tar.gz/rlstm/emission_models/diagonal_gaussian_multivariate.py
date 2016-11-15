'''
Gaussian Multivariate observation model, with unknown mean and diag covariance.

Parameters
----------
K : num states
D : num dimensions for each observation

mu_DK : mean position for cluster k at dimension d
stddev_DK : standard deviation for cluster k at dimension d
'''

import autograd.numpy as np
from autograd.util import flatten
import sys
import pdb
import os

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
    mu_DK = prng.randn(K, D).T
    stddev_DK = 0.1 + 0.1 * prng.rand(D, K)
    return mu2eta(
        mu_DK=mu_DK,
        stddev_DK=stddev_DK)


def eta2mu(eta_mu_DK=None, eta_stddev_DK=None, eps=0.00001, **kwargs):
    ''' Convert unconstrained to mean parameters

    Returns
    -------
    mu_DK : 2D array, D x K
    stddev_DK : 2D array, D x K
    '''
    mu_DK = eta_mu_DK
    stddev_DK = eps + np.log(1.0 + np.exp(eta_stddev_DK))
    return dict(mu_DK=mu_DK, stddev_DK=stddev_DK)


def mu2eta(mu_DK=None, stddev_DK=None, eps=0.00001, **kwargs):
    ''' Convert mean to unconstrained parameters

    Returns
    -------
    eta_mu_DK : 2D array, D x K
    eta_stddev_DK : 2D array, D x K

    Examples
    --------
    >>> np.set_printoptions(suppress=1, precision=3)
    >>> mu_DK = np.zeros((4, 1))
    >>> stddev_DK = np.asarray([[0.1, 0.5, 1.0, 9.0]]).T
    >>> eta_dict = mu2eta(mu_DK=mu_DK, stddev_DK=stddev_DK)
    >>> print eta_dict['eta_mu_DK'].T
    [[ 0.  0.  0.  0.]]
    >>> print eta_dict['eta_stddev_DK'].T
    [[-2.252 -0.433  0.541  9.   ]]

    # Verify invertibility. If we transform then invert, we get original input.
    >>> mu_dict = eta2mu(**eta_dict)
    >>> np.allclose(mu_dict['mu_DK'], mu_DK)
    True
    >>> np.allclose(mu_dict['stddev_DK'], stddev_DK)
    True
    '''
    eta_mu_DK = mu_DK
    stddev_DK = np.maximum(stddev_DK, eps)
    eta_stddev_DK = np.log(np.exp(stddev_DK - eps) - 1.0)
    return dict(eta_mu_DK=eta_mu_DK, eta_stddev_DK=eta_stddev_DK)

def calc_log_proba_data_arr_NK(
        data_DN,
        mu_DK=None,
        stddev_DK=None,
        eta_mu_DK=None,
        eta_stddev_DK=None,
        **kwargs):
    ''' Compute log probability of each dataset observation under each cluster

    Args
    ----
    data_DN : 2D array, n_dims x n_examples, with real values
        data_DN[d, n] = observed value for observation n's d-th dimension
    mu_DK : 2D array, n_dims x n_states, with real values

    Returns
    -------
    log_proba_NK : 2D array, n_examples x n_states, with real values
        entry n,k gives log probability of data row n under state k

    Examples
    --------
    >>> np.set_printoptions(suppress=0, precision=3)
    >>> prng = np.random.RandomState(0)

    # Verify the log proba calc is correct (integrates to unity)
    >>> data_DN = np.linspace(-5, 5, 100)[:,np.newaxis].T
    >>> mu_DK = np.asarray([[0.0, 1.0]])
    >>> stddev_DK = np.asarray([[1.0, 0.5]])
    >>> log_proba_NK = calc_log_proba_data_arr_NK(
    ...     data_DN, mu_DK=mu_DK, stddev_DK=stddev_DK)
    >>> assert log_proba_NK.ndim == 2
    >>> sum_proba_1 = np.trapz(np.exp(log_proba_NK[:,0]), data_DN[0, :])
    >>> np.allclose(1.0, sum_proba_1)
    True
    >>> sum_proba_2 = np.trapz(np.exp(log_proba_NK[:,1]), data_DN[0, :])
    >>> np.allclose(1.0, sum_proba_2)
    True
    '''
    N = data_DN.shape[1]
    if eta_mu_DK is not None:
        mu_dict = eta2mu(eta_mu_DK=eta_mu_DK, eta_stddev_DK=eta_stddev_DK)
        mu_DK = mu_dict['mu_DK']
        stddev_DK = mu_dict['stddev_DK']

    D, K = mu_DK.shape
    log_proba_list = list()
    for k in xrange(K):
        # pdb.set_trace()
        var_k_D = np.square(stddev_DK[:, k])
        arr_k_ND = data_DN.T - mu_DK[:, k]
        arr_k_ND = np.square(arr_k_ND)
        arr_k_ND = arr_k_ND / var_k_D
        mahal_dist_k_N = np.sum(arr_k_ND, axis=1)
        log_proba_list.append(
            - 0.5 * D * np.log(2 * np.pi)
            - 0.5 * mahal_dist_k_N
            - np.sum(np.log(stddev_DK[:, k])))
    log_proba_NK = np.vstack(log_proba_list).T
    return log_proba_NK


# -- wrapper functions to handle single param vector --

def make_eta_D2K(eta_mu_DK, eta_stddev_DK):
    return np.hstack((eta_mu_DK, eta_stddev_DK))


def split_eta_D2K(eta_D2K):
    D, K2 = eta_D2K.shape
    K = int(K2 / 2)
    return eta_D2K[:, :K], eta_D2K[:, K:]


def calc_log_proba_data_arr_NK_flat(data_DN, eta_DK=None):
    ''' wrapper around calc_log_proba_data_arr_NK function that accepts
        a single array with the concatenated eta_mu_DK and eta_stdev_DK
    '''

    if eta_DK is not None:
        eta_mu_DK, eta_stddev_DK = split_eta_D2K(eta_DK)

    log_proba_NK = calc_log_proba_data_arr_NK(
        data_DN,
        eta_mu_DK=eta_mu_DK,
        eta_stddev_DK=eta_stddev_DK)

    return log_proba_NK
