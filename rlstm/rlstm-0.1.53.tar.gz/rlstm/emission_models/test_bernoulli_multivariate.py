import autograd.numpy as np

from autograd import grad
from autograd.util import flatten
from scipy.optimize import fmin_l_bfgs_b

from bernoulli_multivariate import (
    init_natural_param_dict_from_data,
    calc_log_proba_data_arr_NK,
    mu2eta,
    eta2mu,
)

def make_problem(n_examples=1000, seed=0):
    prng = np.random.RandomState(seed)
    mu_KD = np.asarray([[0.1, 0.2, 0.3, 0.4, 0.5]])
    data_ND = prng.rand(n_examples, mu_KD.shape[1]) <= mu_KD
    return data_ND, mu_KD

if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=1)

    data_ND, true_mu_KD = make_problem(n_examples=100000, seed=0)
    K, D = true_mu_KD.shape

    param_dict = init_natural_param_dict_from_data(data_ND)
    init_flat_vec, unflatten_func = flatten(param_dict)

    def calc_neg_log_proba_dataset_wrt_flat_eta(flat_vector):
        param_dict = unflatten_func(flat_vector)
        return -1 * np.sum(
            calc_log_proba_data_arr_NK(data_ND, **param_dict))
    grad_of_neg_log_proba_dataset_wrt_flat_eta = \
        grad(calc_neg_log_proba_dataset_wrt_flat_eta)

    fromrand_flat_vec, fromrand_loss_val, fromrand_dict = fmin_l_bfgs_b(
        calc_neg_log_proba_dataset_wrt_flat_eta,
        init_flat_vec,
        fprime=grad_of_neg_log_proba_dataset_wrt_flat_eta)
    fromrand_mu_KD = eta2mu(**unflatten_func(fromrand_flat_vec))

    fromtrue_flat_vec, fromtrue_loss_val, fromtrue_dict = fmin_l_bfgs_b(
        calc_neg_log_proba_dataset_wrt_flat_eta,
        mu2eta(true_mu_KD).flatten(),
        fprime=grad_of_neg_log_proba_dataset_wrt_flat_eta)
    fromtrue_mu_KD = eta2mu(**unflatten_func(fromtrue_flat_vec))

    print "TRUE MU"
    print ' '.join(['%.3f' % a for a in true_mu_KD.flatten()])
    print "\n OPTIMAL MU FROM RAND INIT"
    print ' '.join(['%.3f' % a for a in fromrand_mu_KD.flatten()])
    print "\n OPTIMAL MU FROM TRUTH"
    print ' '.join(['%.3f' % a for a in fromtrue_mu_KD.flatten()])
