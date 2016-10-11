import argh
from argh import arg
import cPickle
from os.path import join

import autograd.numpy as np


def normalize(X, axis=0):
    return np.divide(X.T, np.sum(X, axis=axis)).T


def toy_matrices():
    pi_mat = np.array([.5, .5, 0, 0, 0])
    trans_mat = np.array(([.5, .5, 0, 0, 0],
                          [.25, .5, .25, 0, 0],
                          [0, .25, .5, .25, 0],
                          [0, 0, .25, .5, .25],
                          [0, 0, 0, .5, .5]))
    obs_mat = np.array(([.5, .5, .5, 0, 0, 0, 0],
                        [0, .5, .5, .5, 0, 0, 0],
                        [0, 0, .5, .5, .5, 0, 0],
                        [0, 0, 0, .5, .5, .5, 0],
                        [0, 0, 0, 0, .5, .5, .5]))
    # obs_mat = np.array( ( [ 1, 0, 0, 0, 0, 0, 0 ], \
    #                       [ 0, 1, 0, 0, 0, 0, 0 ], \
    #                       [ 0, 0, 1, 0, 0, 0, 0 ], \
    #                       [ 0, 0, 0, 1, 0, 0, 0 ], \
    #                       [ 0, 0, 0, 0, 1, 0, 0 ] ) )
    return pi_mat, trans_mat, obs_mat


def spurious_matrices():
    pi_mat = np.array([.2, .2, .2, .2, .2])
    trans_mat = np.array(([.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2]))
    obs_mat = np.array(([.5, .5, .5, 0, 0, 0, 0],
                        [0, .5, .5, .5, 0, 0, 0],
                        [0, 0, .5, .5, .5, 0, 0],
                        [0, 0, 0, .5, .5, .5, 0],
                        [0, 0, 0, 0, .5, .5, .5]))
    return pi_mat, trans_mat, obs_mat


def create_toy_data(data_count, time_count, bias_mat=np.array([15, 15]),
                    weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                                         [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):
    # N is the number of samples and T is the length of the series.
    # Store data in DxTxN array because we'll want to slice by samples.

    # weight_mat is Ox(K+D)-dimensional.
    # bias_mat is O-dimensional (determines the proportion of 0s and 1s in
    # binary output).

    # Define the HMM:
    #   K is the number of states
    #   trans_mat(k,k') is the probability that we transition to k' from k (KxK-dimensional)
    # obs_mat(k,d) is the probability of 1 in dimension d in state k
    # (KxD-dimensional)
    state_count = 5  # number of states K (default = 5)
    # observation dimension D (default=7)
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]  # output dimension O (default=2)

    pi_mat, trans_mat, obs_mat = toy_matrices()

    # Create the sequences
    obs_set = np.zeros((dim_count, time_count, data_count), dtype=int)
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set = np.zeros((state_count, time_count, data_count), dtype=int)
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state = np.random.multinomial(1, pi_mat)
                state_set[:, 0, data_iter] = state
            else:
                tvec = np.dot(
                    state_set[:, time_iter - 1, data_iter], trans_mat)
                state = np.random.multinomial(1, tvec)
                state_set[:, time_iter, data_iter] = state
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            obs_vec = np.dot(state_set[:, time_iter, data_iter], obs_mat)
            obs = np.random.binomial(1, obs_vec)
            obs_set[:, time_iter, data_iter] = obs
            in_vec = np.hstack((state_set[:, time_iter, data_iter],
                                obs_set[:, time_iter, data_iter]))
            out_vec = 1 / \
                (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    # collect the outputs
    param_set = {'state_set': state_set,
                 'pi_mat': pi_mat,
                 'trans_mat': trans_mat,
                 'obs_mat': obs_mat,
                 'weight_mat': weight_mat,
                 'bias_mat': bias_mat}

    # output
    return obs_set, out_set, param_set


def create_2hmm_toy_data(data_count, time_count, bias_mat=np.array([15, 15]),
                         weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                                              [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):
    # Define two independent HMMs. Both will help generate the observations but one
    # one of them will generate the output. The HMM not modelling output is
    # basically noise.

    state_count = 5  # number of states K (default = 5)
    # observation dimension D (default=7)
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]  # output dimension O (default=2)

    pi_mat_1, trans_mat_1, obs_mat_1 = toy_matrices()  # hmm1
    pi_mat_2, trans_mat_2, obs_mat_2 = spurious_matrices()  # hmm2

    # store results here (int because only integers)
    obs_set = np.zeros((dim_count * 2, time_count, data_count), dtype=int)
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set_1 = np.zeros(
        (state_count, time_count, data_count), dtype=int)  # hmm1
    state_set_2 = np.zeros(
        (state_count, time_count, data_count), dtype=int)  # hmm2

    # create state sequences for both
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state_1 = np.random.multinomial(1, pi_mat_1)
                state_2 = np.random.multinomial(1, pi_mat_2)
                state_set_1[:, 0, data_iter] = state_1
                state_set_2[:, 0, data_iter] = state_2
            else:
                tvec_1 = np.dot(
                    state_set_1[:, time_iter - 1, data_iter], trans_mat_1)
                tvec_2 = np.dot(
                    state_set_2[:, time_iter - 1, data_iter], trans_mat_2)
                state_1 = np.random.multinomial(1, tvec_1)
                state_2 = np.random.multinomial(1, tvec_2)
                state_set_1[:, time_iter, data_iter] = state_1
                state_set_2[:, time_iter, data_iter] = state_2

    # generate obs and out matrices
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            # obs
            obs_vec_1 = np.dot(state_set_1[:, time_iter, data_iter], obs_mat_1)
            obs_vec_2 = np.dot(state_set_2[:, time_iter, data_iter], obs_mat_2)
            obs_1 = np.random.binomial(1, obs_vec_1)
            obs_2 = np.random.binomial(1, obs_vec_2)
            obs = np.hstack((obs_1, obs_2))  # concat together
            obs_set[:, time_iter, data_iter] = obs

            # out
            in_vec = np.hstack((state_set_1[:, time_iter, data_iter],  # only use hmm1 to make output
                                obs_set[:, time_iter, data_iter][:dim_count]))
            out_vec = 1 / \
                (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    # collect the outputs
    param_set = {
        'state_set_1': state_set_1,
        'pi_mat_1': pi_mat_1,
        'trans_mat_1': trans_mat_1,
        'obs_mat_1': obs_mat_1,
        'state_set_2': state_set_2,
        'pi_mat_2': pi_mat_2,
        'trans_mat_2': trans_mat_2,
        'obs_mat_2': obs_mat_2,
        'weight_mat': weight_mat,
        'bias_mat': bias_mat
    }

    return obs_set, out_set, param_set


@arg('data_type', help='select from toy_obs_only, toy_obs_and_out, toy_two_hmm')
@arg('-d', '--data_count', default=30, help='number of data groups')
@arg('-t', '--time_count', default=50, help='number of time indices per group')
@arg('-s', '--save_path', help='directory to save numpy files')
def output_toy_data(data_type, data_count=30, time_count=50, save_path=None):
    ''' Runs create_toy_data or create_2hmm_toy_data and saves
        it into the X_train, y_train, ... style
    '''

    if data_type == 'toy_obs_only':
        bias_mat = np.array([5, 5])
        weight_mat = np.array(([10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        obs_set, out_set, param_set = \
            create_toy_data(data_count, time_count, bias_mat, weight_mat)
    elif data_type == 'toy_obs_and_out':
        bias_mat = np.array([15, 15])
        weight_mat = np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))
        obs_set, out_set, param_set = \
            create_toy_data(data_count, time_count, bias_mat, weight_mat)
    elif data_type == 'toy_two_hmm':
        bias_mat = np.array([15, 15])
        weight_mat = np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))
        obs_set, out_set, param_set = \
            create_2hmm_toy_data(data_count, time_count, bias_mat, weight_mat)

    if save_path is None:
        save_path = join('datasets', data_type)

    np.save(join(save_path, 'obs_set.npy'), obs_set)
    np.save(join(save_path, 'out_set.npy'), out_set)
    with open(join(save_path, 'param_set.pkl'), 'wb') as fp:
        cPickle.dump(param_set, fp)

    # do a train_test_split by hand
    train_data_count = int(data_count * 0.35)
    test_data_count = int(data_count * 0.15) + train_data_count
    valid_data_count = int(data_count * 0.50) + test_data_count

    train_obs_set = obs_set[:, :, 0:train_data_count]
    train_out_set = out_set[:, :, 0:train_data_count]
    test_obs_set = obs_set[:, :, train_data_count:test_data_count]
    test_out_set = out_set[:, :, train_data_count:test_data_count]
    valid_obs_set = obs_set[:, :, test_data_count:valid_data_count]
    valid_out_set = out_set[:, :, test_data_count:valid_data_count]

    np.save(join(save_path, 'X_train.npy'), train_obs_set)
    np.save(join(save_path, 'y_train.npy'), train_out_set)
    np.save(join(save_path, 'X_test.npy'), test_obs_set)
    np.save(join(save_path, 'y_test.npy'), test_out_set)
    np.save(join(save_path, 'X_valid.npy'), valid_obs_set)
    np.save(join(save_path, 'y_valid.npy'), valid_out_set)

if __name__ == '__main__':
    argh.dispatch_command(output_toy_data)

