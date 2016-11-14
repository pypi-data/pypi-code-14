"""
This module contains numerical functions.
"""

import numerical.decorators as decorators

__all__ = ['double_fact', 'integrate']


@decorators.non_negative_args
def double_fact(n):
    """Calculate the double factorial of n, n!!.

    If n is even
        n!! := n * (n-2) * (n-4) * ... * 2

    If n is odd
        n!! := n * (n-2) * (n-4) * ... * 1
    """
    df = 1
    for i in range(int(n), 0, -2):
        df *= i
    return df


@decorators.decimal_args
@decorators.rounding(prec=4)
def integrate(f, a, b, n=400):
    """Numerically integrate f between a and b using Simpson's rule with n
    pieces.
    """
    h = (b - a) / n

    def x(j):
        return a + (j * h)

    odd = sum(f(x(2*j)) for j in range(1, int(n) // 2))
    even = sum(f(x(2*j - 1)) for j in range(1, int(n) // 2 + 1))
    return (f(a) + (2 * odd) + (4 * even) + f(b)) * (h / 3)
