from __future__ import division

from math import inf

from ._bracket import bracket
from ._brent import brent

_eps = 1.4901161193847656e-08

def minimize(f, x0=None, x1=None, a=-inf, b=+inf, gfactor=2,
             rtol=_eps, atol=_eps, maxiter=500):

    def func(x):
        func.nfev += 1
        return f(x)
    func.nfev = 0


    r, ecode = bracket(func, x0=x0, x1=x1, a=a, b=b, gfactor=gfactor, rtol=rtol,
                       atol=atol, maxiter=maxiter)

    x0, x1, x2, f0, f1, f2 = r[0], r[1], r[2], r[3], r[4], r[5]
    x0, f0 = brent(func, x0, x2, f0, f2, x1, f1, rtol, atol, maxiter)[0:2]
    return x0, f0, func.nfev
