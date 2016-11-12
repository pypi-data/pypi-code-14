from __future__ import absolute_import
from __future__ import print_function

import autograd.numpy as np
import autograd.scipy.stats.norm as norm
from autograd import grad
from rlstm.nn_util import sigmoid


def unpack_layers(weights, layer_shapes):
    for m, n in layer_shapes:
        cur_layer_weights = weights[:m*n]     .reshape((m, n))
        cur_layer_biases  = weights[m*n:m*n+n].reshape((1, n))
        yield cur_layer_weights, cur_layer_biases
        weights = weights[(m+1)*n:]


def build(input_count,
          state_counts,
          output_count,
          weight_scale=10.0,
          noise_scale=0.1,
          nonlinearity=sigmoid):
    ''' Builds the multi-layer perceptron. Assume that any/all
        one-hot encoding has already been done. This supports
        continuous regression only.

        Args
        ----
        input_count : integer
                      number of features in observations
        output_count : integer
                       number of features in outputs
        state_counts : list
                       list of internal hidden units. Each index represents
                       a new hidden layer.
        weight_scale: float
                      Specifies Gaussian distribution
        noise_scale: float
                     Specifies Gaussian distribution

        Returns
        -------
        prediction: lambda function
                    inputs are (weights, observation)
        log_likelihood: lambda function
                        inputs are (weights, observation, outputs)
        num_weights: integer
                     number of weights in general
    '''

    layer_sizes = [input_count] + list(state_counts) + [output_count]
    layer_shapes = list(zip(layer_sizes[:-1], layer_sizes[1:]))
    num_weights = sum((m+1)*n for m,n in layer_shapes)

    def outputs(weights, inputs):
        ''' inputs must be 2D matrix. This is not for timeseries '''
        inputs = inputs.T
        for W, b in unpack_layers(weights, layer_shapes):
            targets = np.dot(inputs, W) + b
            inputs = nonlinearity(targets)
        return targets.T

    # log pred fun doesnt make sense here but we use a shared
    # sgd fnc that only takes logpred_funs .. it will be re-exp later...
    def log_prediction(weights, inputs):
        return np.log(outputs(weights, inputs))

    def log_likelihood(weights, inputs, targets):
        log_prior = np.sum(norm.logpdf(weights, 0, weight_scale))
        preds = outputs(weights, inputs)
        log_lik = np.sum(norm.logpdf(preds, targets, noise_scale))
        return log_prior + log_lik

    return log_prediction, log_likelihood, num_weights
