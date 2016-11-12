import pdb
import autograd.numpy as np
from autograd.scipy.misc import logsumexp
from rlstm.models.hmm import *


if __name__ == '__main__':
    from rlstm.emission_models import bernoulli_multivariate as emission_module

    # Load simple toy dataset
    dataset_path = os.path.join('../../datasets/tiny_obs_and_out/')
    x_arr = np.load(os.path.join(dataset_path, 'obs_set.npy'))

    n_dims, n_timesteps, n_seqs = x_arr.shape
    x_DM = x_arr.swapaxes(0, 2).reshape((-1, n_dims)).T
    fenceposts_Np1 = np.arange(0, (n_seqs + 1) * n_timesteps, n_timesteps)

    # TEST #1
    # Make a parameter set with just one state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using the emission model to calc log probas
    K = 1
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_DK = emission_module.init_natural_param_array_from_data(
        data_DN=x_DM,
        K=K)
    start_log_proba_K = np.log(np.ones(K) / float(K))
    trans_log_proba_KK = np.ones((K,K))
    trans_log_proba_KK /= trans_log_proba_KK.sum(axis=1)[:,np.newaxis]
    trans_log_proba_KK = np.log(trans_log_proba_KK)

    # Compute loss for single seq
    loss_x, loss_y, _ = calc_loss_for_one_sequence(
        x_n_DT=x_DM,
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_DK=eta_DK,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)

    x_log_proba_T = calc_log_proba_arr_for_x(x_DM, eta_DK=eta_DK)
    assert np.allclose(loss_x, np.sum(x_log_proba_T))
    print('>> PASSED TEST #1')

    # TEST #2
    # Make a parameter set with K=5 states
    # with trans probabilities that are UNIFORM from every state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using a mixture model
    K = 5
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_DK = emission_module.init_natural_param_array_from_data(
        data_DN=x_DM,
        K=K)
    start_log_proba_K = np.log(np.ones(K) / float(K))
    trans_log_proba_KK = np.ones((K,K))
    trans_log_proba_KK /= trans_log_proba_KK.sum(axis=1)[:,np.newaxis]
    trans_log_proba_KK = np.log(trans_log_proba_KK)

    # Compute loss for single seq
    hmm_loss_x, _, _ = calc_loss_for_one_sequence(
        x_n_DT=x_DM,
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_DK=eta_DK,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)

    x_log_proba_TK = calc_log_proba_arr_for_x(x_DM, eta_DK=eta_DK)
    prior_log_proba_K = start_log_proba_K
    mixture_loss_x = -1 * np.sum(logsumexp(
        x_log_proba_TK + prior_log_proba_K[np.newaxis, :], axis=1))
    assert np.allclose(hmm_loss_x, -mixture_loss_x)
    print('>> PASSED TEST #2')

    # TEST #3
    # Make a parameter set with K=5 states
    # with trans probabilities that are same but not uniform from every state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using a mixture model
    K = 4
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_DK = emission_module.init_natural_param_array_from_data(
        data_DN=x_DM,
        K=K,
        seed=123)
    start_log_proba_K = np.log(np.asarray([0.1, 0.2, 0.3, 0.4]))
    trans_log_proba_KK = np.tile(start_log_proba_K, (4,1))

    # Compute loss for single seq
    hmm_loss_x, _, _ = calc_loss_for_one_sequence(
        x_n_DT=x_DM,
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_DK=eta_DK,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)

    # Compute loss for same data under mixture model
    x_log_proba_TK = calc_log_proba_arr_for_x(x_DM, eta_DK)
    prior_log_proba_K = start_log_proba_K
    mixture_loss_x = -1 * np.sum(logsumexp(
        x_log_proba_TK + prior_log_proba_K[np.newaxis, :], axis=1))
    assert np.allclose(hmm_loss_x, -mixture_loss_x)
    print('>> PASSED TEST #3')

    # Finally, compute loss over many sequences
    hmm_loss_x, _, _ = calc_loss_for_many_sequences(
        x_DM=x_DM,
        fenceposts_Np1=fenceposts_Np1,
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_DK=eta_DK,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)
    print('ALL SEQ LOSS: {}'.format(hmm_loss_x))
    assert np.allclose(hmm_loss_x, -1933.99577891)
