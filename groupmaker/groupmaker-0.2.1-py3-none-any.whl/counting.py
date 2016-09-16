"""Functions for creating counts of pairs."""
from collections import Counter

from .models import Pair
from .models import PairCounts


def count_pairs(pairs):
    """Calculate a summary of pair counts from a list of pairs.

    >>> count_pairs([
    ...     Pair('A', 'A'), Pair('A', 'A'), Pair('A', 'B')])
    PairCounts((Pair('A', 'A'), 2), (Pair('A', 'B'), 1))
    """
    counter = Counter(pairs)
    return PairCounts(*counter.items())
