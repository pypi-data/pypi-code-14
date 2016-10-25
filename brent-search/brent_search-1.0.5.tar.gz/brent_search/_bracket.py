from __future__ import division

from math import copysign

inf = float("inf")

_eps = 1.4901161193847656e-08

def bracket(f, x0=None, x1=None, a=-inf, b=+inf, gfactor=2,
            rtol=_eps, atol=_eps, maxiter=500):


    ecode = 0

    # ecode = 0 unknown
    # ecode = 1 found bracket
    # ecode = 2 hit the boundary
    # ecode = 3 too close points
    # ecode = 4 maxiter reached
    # ecode = 5 not strictly convex function

    assert gfactor > 1
    assert maxiter > 0

    x0, x1 = _initialize_interval(x0, x1, a, b, gfactor, rtol, atol)

    f0 = f(x0)
    f1 = f(x1)

    if f0 < f1:
        x0, x1 = x1, x0
        f0, f1 = f1, f0

    if x0 + 2 * _tol(x0, rtol, atol) > x1:
        ecode = 3
        return _sort(x0, x1, x1, f0, f1, f1), ecode

    if f0 == f1:
        return _resolve_equal_fvalue(f, x0, x1, f0, f1)

    assert a <= x0 <= b
    assert a <= x1 <= b
    assert x0 != x1
    assert f0 != f1

    if _boundary_equal(x1, a, b):
        x2 = x1
        f2 = f1
        ecode = 2
        return _sort(x0, x1, x2, f0, f1, f2), ecode

    x2 = _ensure_boundary(x1 + (x1 - x0) * gfactor, a, b)
    f2 = f(x2)

    if f1 == f2:
        return _resolve_equal_fvalue(f, x1, x2, f1, f2)

    nit = 0
    while not(f0 > f1 < f2) and nit < maxiter and _boundary_inside(x2, a, b):
        nit += 1

        xt = _ensure_boundary(x2 + gfactor * (x2 - x1), a, b)
        ft = f(xt)

        x0, x1, x2 = x1, x2, xt
        f0, f1, f2 = f1, f2, ft

    assert x0 <= x1 <= x2

    if f0 > f1 < f2:
        ecode = 1
        return _sort(x0, x1, x2, f0, f1, f2), ecode

    if nit == maxiter:
        ecode = 4
        return _sort(x0, x1, x2, f0, f1, f2), ecode

    ecode = 2
    return _sort(x0, x1, x2, f0, f1, f2), ecode

def _sort(x0, x1, x2, f0, f1, f2):
    if x0 > x2:
        x0, x1, x2 = x2, x1, x0
        f0, f1, f2 = f2, f1, f0
    return x0, x1, x2, f0, f1, f2

def _boundary_equal(x, a, b):
    return x == a or x == b

def _boundary_inside(x, a, b):
    return a < x < b

def _ensure_boundary(x, a, b):
    return max(min(x, b), a)

# def _tol(x0, x1, rtol, atol):
#     return max(abs(x0), abs(x1)) * rtol + atol

def _tol(x, rtol, atol):
    return abs(x) * rtol + atol

def _initialize_interval(x0, x1, a, b, gfactor, rtol, atol):
    x = sorted([xi for xi in [x0, x1] if xi is not None])

    if len(x) == 0:
        x0 = min(max(0, a), b)
    elif len(x) == 1:
        x0 = x[0]
    elif len(x) == 2:
        x0, x1 = x[0], x[1]

    if x1 is None:
        if x0 - a > b - x0:
            x1 = x0 - 10 * gfactor * _tol(x0, rtol, atol)
            x1 = max(x1, a)
        else:
            x1 = x0 + 10 * gfactor * _tol(x0, rtol, atol)
            x1 = min(x1, b)

    return x0, x1

def _resolve_equal_fvalue(f, x0, x1, f0, f1):
    x2 = x0/2 + x1/2
    f2 = f(x2)
    x2, x1 = x1, x2
    f2, f1 = f1, f2
    if not(f0 > f1 < f2):
        ecode = 5
    else:
        ecode = 1
    return _sort(x0, x1, x2, f0, f1, f2), ecode
