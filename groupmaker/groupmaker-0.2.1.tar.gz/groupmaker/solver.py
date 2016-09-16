"""Functions for finding best groups."""
from .generation import generate_all_group_configs
from .models import Group
from .models import GroupConfig
from .models import Pair
from .models import PairCounts
from .models import Students
from .pairing import calc_pairs_in_group_config
from .scoring import score_pairs


def find_min_scoring_group_config(group_configs, historical_pair_counts):
    """Given a list of possible groups and historical pair counts, return which
    has the minimum score.

    >>> find_min_scoring_group_config([
    ...     GroupConfig(Group('A', 'B'), Group('C', 'D')),
    ...     GroupConfig(Group('A', 'C'), Group('B', 'D'))],
    ...     PairCounts((Pair('A', 'B'), 2), (Pair('B', 'D'), 1)))
    GroupConfig(Group('A', 'C'), Group('B', 'D'))
    """

    def _score_group_config_with_historical_pair_counts(group_config):
        return score_pairs(
            calc_pairs_in_group_config(group_config), historical_pair_counts
        )

    return min(
        group_configs, key=_score_group_config_with_historical_pair_counts
    )


def solve_for_min_scoring_groups(students, group_size, historical_pair_counts):
    """Figure out what is the minimum-scoring group config out of all possible
    group configs creatable from a list of students.

    >>> solve_for_min_scoring_groups(
    ...     Students('A', 'B', 'C'),
    ...     2,
    ...     PairCounts((Pair('A', 'B'), 1), (Pair('B', 'C'), 1)))
    GroupConfig(Group('A', 'C'), Group('B'))
    """
    all_group_configs = generate_all_group_configs(students, group_size)
    return find_min_scoring_group_config(
        all_group_configs, historical_pair_counts
    )
