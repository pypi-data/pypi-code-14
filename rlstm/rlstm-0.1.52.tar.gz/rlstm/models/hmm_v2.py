import sys
import os
import autograd.numpy as np

from autograd.scipy.misc import logsumexp

sys.path.append('../emission_models/')

def calc_loss_for_many_sequences(
        x_MD=None,
        y_MC=None,
        fenceposts_Np1=None,
        calc_log_proba_arr_for_x=None,
        eta_param_dict=None,
        start_log_proba_K=None,
        trans_log_proba_KK=None,
        **kwargs):
    ''' Compute loss (negative log probability) for many sequences given an HMM

    Args
    ----
    x_MD : 2D array, M x D, of real values
        Each row contains observed x data at one timestep of a sequence.
    y_MC : 2D array, M x C, of real values
        Each row contains observed y responses at one timestep of a sequence.
    fenceposts_Np1 : 1D array, N+1, positive integer values
        fenceposts_Np1[n] gives start index of sequence n
        fenceposts_Np1[n+1] gives stop index of sequence n
    calc_log_proba_arr_for_x : function
        Computes log proba of each observation under each possible state
        Returns T x K array
    eta_param_dict : dict
        Contains key/value pairs for each parameter array of emission model
        Must match expected "eta" args of calc_log_proba_arr_for_x
    start_log_proba_K : 1D array, size K
        Starting-state log probabilities for the HMM.
        np.exp(start_log_proba_K) must sum to one
    trans_log_proba_KK : 2D array, size K x K
        Transition log probabilities for the HMM.
        np.exp(trans_log_proba_KK) must sum to one along each row

    Returns
    -------
    loss_x : real scalar
    loss_y : real scalar
    '''
    n_seqs = fenceposts_Np1.size - 1
    n_dims = x_MD.shape[1]

    loss_x = 0.0
    loss_y = 0.0
    for n in xrange(n_seqs):
        # Get slice of x data corresp. to current sequence
        start_n = fenceposts_Np1[n]
        stop_n = fenceposts_Np1[n+1]
        x_n_TD = x_MD[start_n:stop_n]
        if y_MC is None:
            y_n_TC = None
        else:
            y_n_TC = y_MC[start_n:stop_n]

        loss_x_n, loss_y_n = calc_loss_for_one_sequence(
            x_n_TD=x_n_TD,
            y_n_TC=y_n_TC,
            calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
            eta_param_dict=eta_param_dict,
            start_log_proba_K=start_log_proba_K,
            trans_log_proba_KK=trans_log_proba_KK)
        loss_x = loss_x + loss_x_n
        loss_y = loss_y + loss_y_n
    return loss_x, loss_y

def calc_loss_for_one_sequence(
        x_n_TD=None,
        y_n_TC=None,
        calc_log_proba_arr_for_x=None,
        eta_param_dict=None,
        start_log_proba_K=None,
        trans_log_proba_KK=None,
        **kwargs):
    ''' Compute loss (negative log probability) for one sequence given an HMM

    Args
    ----
    x_n_TD : 2D array, T x D, of real values
        Each row contains observed x data at timestep t of the sequence.
    y_n_TC : 2D array, T x C, of real values
        Each row contains observed y responses at timestep t of the seq.
    calc_log_proba_arr_for_x : function
        Computes log proba of each observation under each possible state
        Returns T x K array
    eta_param_dict : dict
        Contains key/value pairs for each parameter array of emission model
        Must match expected "eta" args of calc_log_proba_arr_for_x
    start_log_proba_K : 1D array, size K
        Starting-state log probabilities for the HMM.
        np.exp(start_log_proba_K) must sum to one
    trans_log_proba_KK : 2D array, size K x K
        Transition log probabilities for the HMM.
        np.exp(trans_log_proba_KK) must sum to one along each row

    Returns
    -------
    loss_x : real scalar
    loss_y : real scalar
    '''
    n_timesteps = x_n_TD.shape[0]
    # Compute log proba array
    x_n_log_proba_TK = calc_log_proba_arr_for_x(
        x_n_TD,
        **eta_param_dict)

    # Initialize fwd belief vector at t = 0
    cur_belief_log_proba_K = start_log_proba_K + x_n_log_proba_TK[0]
    cur_x_log_proba = logsumexp(cur_belief_log_proba_K)
    cur_belief_log_proba_K = cur_belief_log_proba_K - cur_x_log_proba

    loss_x = -1 * cur_x_log_proba
    loss_y = 0.0

    # Recursively update forward beliefs via dynamic programming
    for t in range(1, n_timesteps):
        cur_belief_log_proba_K, cur_x_log_proba = update_belief_log_probas(
            cur_belief_log_proba_K,
            x_n_log_proba_TK[t],
            trans_log_proba_KK)

        # Compute log proba for x[t]
        loss_x = loss_x - cur_x_log_proba

        # Compute log proba for y[t]
        if y_n_TC is not None:
            raise NotImplementedError("TODO")

    return loss_x, loss_y


def update_belief_log_probas(
        prev_belief_log_proba_K,
        curr_data_log_proba_K,
        trans_log_proba_KK,
        return_norm_const=1):
    '''

    Examples
    --------
    # Uniform belief and uniform transitions, should just equal data probs
    >>> prev_belief_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> curr_data_log_proba_K = np.log(np.asarray([0.6, 0.4]))
    >>> trans_log_proba_KK = np.log(np.asarray([[0.5, 0.5], [0.5, 0.5]]))
    >>> curr_belief_log_proba_K = update_belief_log_probas(
    ...     prev_belief_log_proba_K, curr_data_log_proba_K, trans_log_proba_KK,
    ...     return_norm_const=0)
    >>> print np.exp(curr_belief_log_proba_K)
    [ 0.6  0.4]

    >>> prev_belief_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> curr_data_log_proba_K = np.log(np.asarray([0.5, 0.5]))
    >>> trans_log_proba_KK = np.log(np.asarray([[0.9, 0.1], [0.9, 0.1]]))
    >>> curr_belief_log_proba_K = update_belief_log_probas(
    ...     prev_belief_log_proba_K, curr_data_log_proba_K, trans_log_proba_KK,
    ...     return_norm_const=0)
    >>> print np.exp(curr_belief_log_proba_K)
    [ 0.9  0.1]
    '''
    cur_belief_log_proba_K = logsumexp(
        trans_log_proba_KK + prev_belief_log_proba_K[:, np.newaxis],
        axis=0)
    cur_belief_log_proba_K = cur_belief_log_proba_K \
        + curr_data_log_proba_K
    # Normalize in log space
    log_norm_const = logsumexp(cur_belief_log_proba_K)
    cur_belief_log_proba_K = cur_belief_log_proba_K - log_norm_const    
    if return_norm_const:
        return cur_belief_log_proba_K, log_norm_const
    else:
        return cur_belief_log_proba_K

if __name__ == '__main__':
    import bernoulli_multivariate as emission_module

    # Load simple toy dataset
    dataset_path = os.path.join(
        os.environ['HOME'],
        'git/interpretable-models/datasets/tiny_obs_and_out/')
    x_arr = np.load(os.path.join(dataset_path, 'obs_set.npy'))
    try:
        fenceposts_Np1 = np.load(os.path.join(dataset_path, 'fenceposts.npy'))
    except IOError:
        n_dims = x_arr.shape[0]
        n_timesteps, n_seqs = x_arr.shape[1:]
        x_MD = x_arr.swapaxes(0, 2).reshape((-1, n_dims))
        fenceposts_Np1 = np.arange(0, (n_seqs + 1) * n_timesteps, n_timesteps)

    # TEST #1
    # Make a parameter set with just one state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using the emission model to calc log probas
    K = 1
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_param_dict = emission_module.init_natural_param_dict_from_data(
        data_ND=x_MD,
        K=K)
    start_log_proba_K = np.log(np.ones(K) / float(K))
    trans_log_proba_KK = np.ones((K,K))
    trans_log_proba_KK /= trans_log_proba_KK.sum(axis=1)[:,np.newaxis]
    trans_log_proba_KK = np.log(trans_log_proba_KK)

    # Compute loss for single seq
    loss_x, loss_y = calc_loss_for_one_sequence(
        x_n_TD=x_MD[:10],
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_param_dict=eta_param_dict,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)
    x_log_proba_T = calc_log_proba_arr_for_x(x_MD[:10], **eta_param_dict)
    assert np.allclose(loss_x, -1 * np.sum(x_log_proba_T))


    # TEST #2
    # Make a parameter set with K=5 states
    # with trans probabilities that are UNIFORM from every state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using a mixture model
    K = 5
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_param_dict = emission_module.init_natural_param_dict_from_data(
        data_ND=x_MD,
        K=K)
    start_log_proba_K = np.log(np.ones(K) / float(K))
    trans_log_proba_KK = np.ones((K,K))
    trans_log_proba_KK /= trans_log_proba_KK.sum(axis=1)[:,np.newaxis]
    trans_log_proba_KK = np.log(trans_log_proba_KK)

    # Compute loss for single seq
    hmm_loss_x, _ = calc_loss_for_one_sequence(
        x_n_TD=x_MD[:10],
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_param_dict=eta_param_dict,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)

    x_log_proba_TK = calc_log_proba_arr_for_x(x_MD[:10], **eta_param_dict)
    prior_log_proba_K = start_log_proba_K
    mixture_loss_x = -1 * np.sum(logsumexp(
        x_log_proba_TK + prior_log_proba_K[np.newaxis, :], axis=1))
    assert np.allclose(hmm_loss_x, mixture_loss_x)

    # TEST #3
    # Make a parameter set with K=5 states
    # with trans probabilities that are same but not uniform from every state
    # Verify that loss calculation for full hmm
    # is exactly equal to just using a mixture model
    K = 4
    calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    eta_param_dict = emission_module.init_natural_param_dict_from_data(
        data_ND=x_MD,
        K=K,
        seed=123)
    start_log_proba_K = np.log(np.asarray([0.1, 0.2, 0.3, 0.4]))
    trans_log_proba_KK = np.tile(start_log_proba_K, (4,1))
    # Compute loss for single seq
    hmm_loss_x, _ = calc_loss_for_one_sequence(
        x_n_TD=x_MD[:10],
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_param_dict=eta_param_dict,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)
    # Compute loss for same data under mixture model
    x_log_proba_TK = calc_log_proba_arr_for_x(x_MD[:10], **eta_param_dict)
    prior_log_proba_K = start_log_proba_K
    mixture_loss_x = -1 * np.sum(logsumexp(
        x_log_proba_TK + prior_log_proba_K[np.newaxis, :], axis=1))
    assert np.allclose(hmm_loss_x, mixture_loss_x)

    # Finally, compute loss over many sequences
    hmm_loss_x, _ = calc_loss_for_many_sequences(
        x_MD=x_MD,
        fenceposts_Np1=fenceposts_Np1,
        calc_log_proba_arr_for_x=calc_log_proba_arr_for_x,
        eta_param_dict=eta_param_dict,
        start_log_proba_K=start_log_proba_K,
        trans_log_proba_KK=trans_log_proba_KK)
