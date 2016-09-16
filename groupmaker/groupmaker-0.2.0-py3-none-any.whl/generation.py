"""Functions for generating group configs from students."""
from itertools import permutations, zip_longest

from .models import Group
from .models import GroupConfig
from .models import Students


def _is_not_none(x):
    """Return if a value is not None.

    >>> _is_not_none(1)
    True
    >>> _is_not_none(None)
    False
    """
    return x is not None


def _filter_nones(iterable):
    """Filter all Nones out of an iterable.

    >>> list(_filter_nones([None, 1, None, 2, None]))
    [1, 2]
    """
    return filter(_is_not_none, iterable)


def _chunk(iterable, size):
    """Take an iterable and chunk it into iterables of a given size.
    Last chunk might be shorter.

    >>> list(list(chunk) for chunk in _chunk([1, 2, 3, 4], 3))
    [[1, 2, 3], [4]]
    """
    copies = [iter(iterable)] * size
    chunks = zip_longest(*copies)
    return map(_filter_nones, chunks)


def _groups_from_ordering(ordering, group_size):
    """Yield groups from an ordering of students by chunking every group size.

    >>> list(_groups_from_ordering(['A', 'B', 'C'], 2))
    [Group('A', 'B'), Group('C')]
    """
    return (Group(*names) for names in _chunk(ordering, group_size))


def generate_all_group_configs(students, group_size):
    """Yield all possible unique groups of a given size from all students.

    Generates every unique ordering of students, then chunks each into groups.
    Very permutive.

    >>> list(generate_all_group_configs(Students('A', 'B', 'C'), 2))
    ... # doctest: +NORMALIZE_WHITESPACE
    [GroupConfig(Group('A'),      Group('B', 'C')),
     GroupConfig(Group('A', 'B'), Group('C')),
     GroupConfig(Group('A', 'C'), Group('B'))]
    """
    return sorted(frozenset(GroupConfig(*_groups_from_ordering(ordering,
                                                           group_size))
            for ordering in permutations(students.names)))
