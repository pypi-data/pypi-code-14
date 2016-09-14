# -*- coding: utf-8 -*-

""" Implements a Class for Representing a Simulated Senate Election. """

from collections import Counter
from random import random
from random import seed as set_seed
from time import asctime
from time import localtime

from aus_senate_audit.senate_election.base_senate_election import BaseSenateElection


class SimulatedSenateElection(BaseSenateElection):
    """ Implements a class for representing a simulated senate election.

    :ivar int _sample_increment_size: The number of ballots to add to the growing sample during each audit stage.

    NOTE: The :attr:`_candidates` and :attr:`_candidate_ids` instance attributes are set as a [1, ..., :attr:`_m`].
    """
    TYPE = 'Simulated'
    DEFAULT_ID = 'SimulatedElection{}'

    def __init__(self, seed, n, m, sample_increment_size):
        """ Initializes a :class:`SimulatedSenateElection` object.

        The number of seats in a simulated senate election is equal to the floor of the number of candidates in the
            election divided by two.

        :param int seed: The starting value for the random number generator.
        :param int n: The total number of ballots cast in the election.
        :param int m: The total number of candidates in the election.
        :param int sample_increment_size: The number of ballots to add to the growing sample during each audit stage.
        """
        super(SimulatedSenateElection, self).__init__()
        self._n = n
        self._m = m
        self._seats = int(self._m / 2)
        self._candidates = list(range(1, self._m + 1))
        self._candidate_ids = list(range(1, self._m + 1))
        self._election_id = SimulatedSenateElection.DEFAULT_ID.format(asctime(localtime()))
        self._sample_increment_size = sample_increment_size
        set_seed(seed)  # Set the initial value of the RNG.

    def draw_ballots(self):
        """ Adds simulated ballots to the sample of ballots drawn thus far.

        These ballots are biased so (1, 2, ..., m) is likely to be the winner. More precisely, each ballot candidate `i`
        is given a value `i + v * U` where `U = uniform(0, 1)` and `v` is the level of noise. Then the candidates are
        sorted into increasing order by these values. Note that the total number of ballots drawn may not exceed the
        total number of cast votes, :attr:`_n`.
        """
        v = self._m / 2.0  # Noise level to control position variance.
        batch_size = min(self._sample_increment_size, self._n - self._num_ballots_drawn)
        for _ in range(batch_size):
            candidate_values = [(i + v * random(), cid) for i, cid in enumerate(self._candidate_ids)]
            ballot = tuple(cid for val, cid in sorted(candidate_values))
            self.add_ballot(ballot, 1)

    def get_outcome(self, ballot_weights):
        """ Returns the outcome of a senate election with the given ballot weights.

        The social choice function used in the simulated senate election is Borda count.

        :param :class:`Counter` ballot_weights: A mapping from a ballot type to the number of ballots drawn of that
            type.

        :returns: The IDs of the candidates elected to the available seats, sorted in lexicographical order.
        :rtype: tuple
        """
        counter = Counter()
        for ballot, weight in ballot_weights.items():
            for i, cid in enumerate(ballot):
                counter[cid] += weight * i
        # Get the :attr:`_seat` candidates with the lowest Borda counts in increasing order.
        winners = counter.most_common()[-self._seats:][::-1]
        return tuple(sorted([cid for cid, count in winners]))
