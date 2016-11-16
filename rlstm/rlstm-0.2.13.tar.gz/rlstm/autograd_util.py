from autograd.core import FloatNode
import autograd.numpy as np

def autograd_apply(x, func):
    shape = x.shape
    x_flat = x.flatten()
    for i in range(x_flat.size):
        x_flat[i].value = func(x_flat[i].value)
    return x_flat.reshape(shape)


def autograd_extract(x):
    shape = x.shape
    x_flat = x.flatten()
    xc = [i.value for i in x_flat]
    return np.array(xc).reshape(shape)


def is_autograd_array(x):
    return isinstance(x.flatten()[0], FloatNode)
