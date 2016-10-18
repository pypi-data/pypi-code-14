import autograd.numpy as np
import autograd.numpy.random as npr
from autograd import value_and_grad
from rlstm.nn_util import sigmoid


def linear_predictions(weights, input_set, in_dim_count, out_dim_count):
    # Output_set probability of a label being true according to logistic model.
    weights = np.reshape(weights, (out_dim_count, in_dim_count))
    return np.dot(weights, input_set)


def training_loss(weights, input_set, output_set):
    # Training loss is the negative log-likelihood of the training labels.
    in_dim_count = input_set.shape[0]
    out_dim_count = output_set.shape[0]
    preds = linear_predictions(weights, input_set, in_dim_count, out_dim_count)
    loss = np.sum((output_set - preds)**2)
    return loss


def build(input_set, output_set):
    in_dim_count = input_set.shape[0]
    out_dim_count = output_set.shape[0]
    if len(input_set.shape) > 2:
        input_set = np.reshape(input_set, (in_dim_count, -1))
        output_set = np.reshape(output_set, (out_dim_count, -1))
    init_weights = npr.random((out_dim_count, in_dim_count)).flatten()
    train_iters = 10000

    loss = lambda weights: training_loss(weights, input_set, output_set)
    training_loss_and_grad = value_and_grad(loss)
    result = minimize(training_loss_and_grad, init_weights, jac=True, method='CG',
                      options={'maxiter': train_iters})
    weights = result.x
    pred_fun = lambda input_set: np.dot(
        np.reshape(weights, (out_dim_count, in_dim_count)), input_set)
    return pred_fun, weights
