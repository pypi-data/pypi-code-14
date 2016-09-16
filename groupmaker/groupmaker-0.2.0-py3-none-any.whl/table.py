"""Functions to print tables of student pairings."""
from tabulate import tabulate

from .models import Pair
from .models import Students
from .models import PairCounts


def print_student_pair_count_matrix(students, pair_counts, file=None):
    """Print out a matrix of pair counts of all students.

    >>> print_student_pair_count_matrix(
    ...     Students('A', 'B'),
    ...     PairCounts((Pair('A', 'A'), 2), (Pair('A', 'B'), 1)))
    +----+-----+-----+
    |    |   A |   B |
    |----+-----+-----|
    | A  |   2 |   1 |
    | B  |   1 |   0 |
    +----+-----+-----+
    """
    pair_count_matrix = _calc_pair_count_matrix(students, pair_counts)
    _print_student_pair_count_matrix(students, pair_count_matrix, file)


def _calc_pair_count_matrix(students, pair_counts):
    """Produce a matrix of how often names have been paired together in a set
    of groups.

    Returns an ordered list of names and the matrix in that order.

    >>> _calc_pair_count_matrix(
    ...     Students('A', 'B'),
    ...     PairCounts((Pair('A', 'A'), 2), (Pair('A', 'B'), 1)))
    [[2, 1], [1, 0]]
    """
    return [[pair_counts.get_count(Pair(name1, name2))
                     for name2 in students.names] for name1 in students.names]


def _print_student_pair_count_matrix(students, count_matrix, file=None):
    """Print a matrix of students and counts.

    >>> _print_student_pair_count_matrix(Students('A', 'B', 'C'),
    ...                         [[0, 1, 1], [1, 0, 2], [1, 2, 0]])
    +----+-----+-----+-----+
    |    |   A |   B |   C |
    |----+-----+-----+-----|
    | A  |   0 |   1 |   1 |
    | B  |   1 |   0 |   2 |
    | C  |   1 |   2 |   0 |
    +----+-----+-----+-----+
    """
    table = [[name] + counts
             for name, counts in zip(students.names, count_matrix)]
    print(tabulate(table, students.names, tablefmt='psql'), file=file)
