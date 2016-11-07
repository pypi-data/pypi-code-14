import autograd.numpy as np

from autograd import grad
from autograd.util import flatten
from scipy.optimize import fmin_l_bfgs_b

from diagonal_gaussian_multivariate import (
    init_natural_param_dict_from_data,
    calc_log_proba_data_arr_NK,
    mu2eta,
    eta2mu,
)

def make_problem(n_examples=1000, seed=0):
    prng = np.random.RandomState(seed)
    n_dims = 6
    mu_KD = np.asarray([[-2, -1, 0.0, 1, 2, 5]])
    stddev_KD = np.asarray([[0.1, 1.0, 10.0, 1.0, 0.1, 0.001]])
    data_ND = mu_KD[0] + stddev_KD[0] * prng.randn(n_examples, n_dims)
    return data_ND, dict(
        mu_KD=mu_KD, stddev_KD=stddev_KD)

if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=1)

    data_ND, true_param_dict = make_problem(n_examples=10000, seed=0)

    init_param_dict = init_natural_param_dict_from_data(data_ND)
    randinit_flat_vec, unflatten_func = flatten(init_param_dict)
    trueinit_flat_vec, _ = flatten(mu2eta(**true_param_dict))

    def calc_neg_log_proba_dataset_wrt_flat_eta(flat_vector):
        param_dict = unflatten_func(flat_vector)
        return -1 * np.sum(
            calc_log_proba_data_arr_NK(data_ND, **param_dict))
    grad_of_neg_log_proba_dataset_wrt_flat_eta = \
        grad(calc_neg_log_proba_dataset_wrt_flat_eta)

    fromrand_flat_vec, fromrand_loss_val, fromrand_dict = fmin_l_bfgs_b(
        calc_neg_log_proba_dataset_wrt_flat_eta,
        randinit_flat_vec,
        fprime=grad_of_neg_log_proba_dataset_wrt_flat_eta)
    fromrand_param_dict = eta2mu(**unflatten_func(fromrand_flat_vec))

    fromtrue_flat_vec, fromtrue_loss_val, fromtrue_dict = fmin_l_bfgs_b(
        calc_neg_log_proba_dataset_wrt_flat_eta,
        trueinit_flat_vec,
        fprime=grad_of_neg_log_proba_dataset_wrt_flat_eta)
    fromtrue_param_dict = eta2mu(**unflatten_func(fromtrue_flat_vec))

    def pprint_param_dict(label='', mu_KD=None, stddev_KD=None):
        print label
        print  'mean vec   ' + \
            ' '.join(['% 9.5f' % a for a in mu_KD.flatten()])
        print 'stddev vec ' + \
            ' '.join(['% 9.5f' % a for a in stddev_KD.flatten()])

    pprint_param_dict('TRUE PARAMS', **true_param_dict)
    pprint_param_dict('FROMRAND ESTIMATED PARAMS', **fromrand_param_dict)
    print fromrand_loss_val

    pprint_param_dict('FROMTRUE ESTIMATED PARAMS', **fromtrue_param_dict)
    print fromtrue_loss_val