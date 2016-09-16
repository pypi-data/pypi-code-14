"""Functions for scoring current pairs based on historical pairings."""
from .models import Pair
from .models import PairCounts


def score_pairs(pairs, historical_pair_counts):
    """Given a current list of pairs, return a score of how many times
    current pairs have been paired together before.

    The higher the score, the more frequently they've been grouped together.
    Arbitrary units.

    >>> score_pairs(
    ...     [Pair('A', 'B'), Pair('A', 'C'), Pair('B', 'C')],
    ...     PairCounts((Pair('A', 'B'), 1), (Pair('A', 'C'), 2)))
    5
    """
    return sum(historical_pair_counts.get_count(pair) ** 2 for pair in pairs)
