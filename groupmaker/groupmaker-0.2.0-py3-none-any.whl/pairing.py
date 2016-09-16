"""Functions for counting pairs in historical groups."""
from itertools import chain, combinations_with_replacement

from .models import Pair
from .models import Group
from .models import GroupConfig


def _tuple_to_pair(t):
    """Convert a two tuple to a pair.

    >>> _tuple_to_pair(('A', 'B'))
    Pair('A', 'B')
    """
    return Pair(*t)


def calc_pairs_in_group(group):
    """Yield all pairs in a group in order.

    >>> list(calc_pairs_in_group(Group('A', 'B')))
    [Pair('A', 'A'), Pair('A', 'B'), Pair('B', 'B')]
    """
    pair_lists = combinations_with_replacement(group.names, 2)
    return map(_tuple_to_pair, pair_lists)


def calc_pairs_in_group_config(group_config):
    """Yield all pairs in a group config in order.

    >>> list(calc_pairs_in_group_config(GroupConfig(Group('A', 'B'), Group('C'))))
    [Pair('A', 'A'), Pair('A', 'B'), Pair('B', 'B'), Pair('C', 'C')]
    """
    return chain.from_iterable(
        calc_pairs_in_group(group) for group in group_config.groups)


def calc_pairs_in_group_configs(group_configs):
    """Yield all pairs in a list of group configs in order.

    >>> list(calc_pairs_in_group_configs([
    ...     GroupConfig(Group('A', 'B'), Group('C')),
    ...     GroupConfig(Group('A', 'C'), Group('B'))]))
    ... # doctest: +NORMALIZE_WHITESPACE
    [Pair('A', 'A'), Pair('A', 'B'), Pair('B', 'B'), Pair('C', 'C'),
     Pair('A', 'A'), Pair('A', 'C'), Pair('C', 'C'), Pair('B', 'B')]
    """
    return chain.from_iterable(
        calc_pairs_in_group_config(group_config)
        for group_config in group_configs)
