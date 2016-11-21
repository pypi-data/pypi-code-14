import qlda.utilities as utilities
import os
import numpy as np


def load_model(path_model):
    # read setting
    path_setting_file = path_model + '/setting.txt'
    if not os.path.exists(path_setting_file):
        print('setting file not found!!!')
    else:
        setting = utilities.read_setting(path_setting_file)
    # print(setting)

    # read_beta
    beta = np.zeros((setting['num_topics'], setting['num_terms']))
    path_beta_file = path_model + '/beta_final.dat'
    if not os.path.exists(path_beta_file):
        print('beta file not found!!!')
    else:
        i = 0
        with open(path_beta_file, 'r') as file:
            for topic in file:
                t = np.array(list(map(float, topic.split())))
                beta[i] = t
                i += 1
                # print(t)
        # print(beta)
    return beta, setting['alpha'], setting['iter_infer']

def read_doc(data):
    doc = data.split()
    num_terms = int(doc[0])
    ids = np.zeros(num_terms, dtype=np.int32)
    cts = np.zeros(num_terms, dtype=np.int32)
    for i in range(1, num_terms + 1):
        term = doc[i].split(':')
        ids[i - 1] = int(term[0])
        cts[i - 1] = int(term[1])
    return ids, cts


# def infer_doc(alphad, betad, iter_infer, ids, cts, weight):
def infer_doc(model, data, weight):
    # load model, data
    ids, cts = read_doc(data)
    alphad = model[0]
    betad = model[1]
    iter_infer = model[2]
    # locate cache memory
    # locate cache memory
    beta = betad[:, ids]
    # Initialize theta randomly
    theta = np.random.rand(betad.shape[0]) + 1
    theta /= sum(theta)

    x = np.dot(theta, beta)
    # Loop
    T = [1, 0]
    for l in range(1, iter_infer):
        # Pick fi uniformly
        T[np.random.randint(2)] += 1
        # Select a vertex with the largest value of
        # derivative of the function F
        df = T[0] * np.dot(beta, cts / x) + T[1] * (alphad - 1) / theta
        index = np.argmax(df)
        alpha = 1.0 / (l + 1)
        # Update theta
        theta *= 1 - alpha
        theta[index] += alpha
        # Update x
        x = x+alpha * (beta[index, :] - x)

    dict = {}
    i = 0
    for p in theta:
        if p > weight:
            dict[i] = p
        i += 1

    # sort_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

    return dict
