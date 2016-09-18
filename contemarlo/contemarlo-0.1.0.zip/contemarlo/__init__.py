"""
ConteMarlo
A "Monte-Carlo-Like" tester.
-Ryan Birmingham

The concept is simple (and probably already done better): detailed Monte-Carlo
but without the randomness or memory dependence.
Despite the memory independence, generators default to safe mode not to flood
the memory space.

I to construct tests, so I know I don't break things.

Classes:
    Resolver - A generator for the next distribution value pair
    Distribution - A distribution, samplable at [0,1]
"""

__all__ = ["Distribution", "Resolver", "Resolver_md"]
from Distribution import Distribution
from Resolver import Resolver, Resolver_md
