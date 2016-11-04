import autograd.numpy as np


def split_dataset(in_data, out_data=None, frac=0.80):
    ''' splitting dataset into training/testing sets '''
    num_data = in_data.shape[1]
    num_tr_data = int(np.floor(num_data * frac))
    indices = np.random.permutation(num_data)

    tr_idx, te_idx = indices[:num_tr_data], indices[num_tr_data:]
    tr_in_data, te_in_data = in_data[:, tr_idx], in_data[:, te_idx]

    if not out_data is None:
        tr_out_data, te_out_data = out_data[:, tr_idx], out_data[:, te_idx]
        return (tr_in_data, te_in_data), (tr_out_data, te_out_data)

    return (tr_in_data, te_in_data)


def sample_dataset(goal_length, inputs, outputs, indexes, heuristic='even'):
    ''' If a dataset is to large, sample it intelligently.

        Args
        ----
        goal_length : integer
                      desired length of dataset
        heuristic : string
                    ['even', 'random', 'first', 'last']
                    metho of subsampling
    '''

    if not heuristic in ['even', 'random', 'first', 'last']:
        raise ValueError('heuristic ({}) not recognized.'.format(heuristic))

    num_length = inputs.shape[0]
    if len(set(outputs.shape[0], indexes.shape[0], inputs.shape[0])) > 1:
        return ValueError('matrices are different sizes.')

    positions = np.range(num_length)
    n = num_length / goal_length

    if heuristic == 'even':
        positions = positions[::n]
    elif heuristic == 'random':
        positions = np.random.choice(positions,
                                     size=goal_length,
                                     replace=False).sort()
    elif heuristic == 'first':
        positions = positions[:goal_length]
    else:
        positions = positions[goal_length:]

    return inputs[positions], outputs[positions], indexes[positions]
