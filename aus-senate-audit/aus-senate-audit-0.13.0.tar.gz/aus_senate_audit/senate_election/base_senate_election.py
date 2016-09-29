# -*- coding: utf-8 -*-

""" Implements a Base Class for Representing a Senate Election. """

from collections import Counter


class BaseSenateElection(object):
    """ Implements a base class for representing a senate election.

    :ivar int _n: The total number of ballots cast in the election.
    :ivar int _m: The total number of candidates in the election.
    :ivar int _seats: The number of available seats in the election.
    :ivar int _num_ballots_drawn: The number of ballots drawn in the election thus far.
    :ivar :class:`Counter` _ballot_weights: A mapping from a ballot type to the number of ballots drawn of that type.
    :ivar list _candidates: The candidates participating in the election.
    :ivar list _candidate_ids: The IDs of the candidates participating in the election.
    :ivar str _election_id: The ID of the election.
    """
    TYPE = None

    def __init__(self):
        """ Initializes a :class:`BaseSenateElection` object. """
        self._n = 0
        self._m = 0
        self._seats = 0
        self._num_ballots_drawn = 0
        self._ballot_weights = Counter()
        self._candidates = []
        self._candidate_ids = []
        self._election_id = None

    def get_num_cast_ballots(self):
        """ Returns the number of cast ballots.

        :returns: The number of cast ballots.
        :rtype: int
        """
        return self._n

    def get_num_seats(self):
        """ Returns the number of available seats in the election.

        :returns: The number of available seats in the election.
        :rtype: int
        """
        return self._seats

    def get_num_ballots_drawn(self):
        """ Returns the total weight of the ballots drawn thus far.

        :returns: The total weight of the ballots drawn thus far.
        :rtype: int
        """
        return self._num_ballots_drawn

    def get_ballots(self):
        """ Returns the ballots drawn thus far.

        :returns: The ballots drawn thus far.
        :rtype: set
        """
        return self._ballot_weights.keys()

    def get_ballot_weight(self, ballot):
        """ Returns the weight of the given ballot type in the ballots drawn thus far.

        :param tuple ballot: The type of ballot.

        :returns: The weight of the given ballot type in the ballots drawn thus far.
        :rtype: int
        """
        return self._ballot_weights[ballot]

    def get_candidates(self):
        """ Returns the candidates participating in the election.

        :returns: The candidates participating in the election.
        :rtype: list
        """
        return self._candidates

    def get_candidate_ids(self):
        """ Returns the IDs of the candidates participating in the election.

        :returns: The IDs of the candidates participating in the election.
        :rtype: list
        """
        return self._candidate_ids

    def get_election_id(self):
        """ Returns the ID of the election.

        :returns: The ID of the election.
        :rtype: str
        """
        return self._election_id

    def get_type(self):
        """ Returns the type of the election.

        :returns: The type of the election.
        :rtype: str
        """
        return self.__class__.TYPE

    def add_ballot(self, ballot, weight):
        """ Adds the ballot type with the given weight to the ballots drawn thus far.

        :param tuple ballot: The ballot type to add to the ballots drawn thus far.
        :param int weight: The weight of the ballot type being added.
        """
        self._ballot_weights[ballot] += weight
        self._num_ballots_drawn += weight

    def draw_ballots(self):
        """ Adds cast ballots to the growing sample for the audit. """
        raise NotImplementedError

    def get_outcome(self, ballot_weights):
        """ Returns the outcome of a senate election with the given ballot weights.

        :param :class:`Counter` ballot_weights: A mapping from a ballot type to the number of ballots drawn of that
            type.

        :returns: The IDs of the candidates elected to the available seats, sorted in lexicographical order.
        :rtype: tuple
        """
        raise NotImplementedError
