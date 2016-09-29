# -*- coding: utf-8 -*-

""" Implements a class for tracking elected candidates for real audit. """

from dividebatur.results import BaseResults


class RealSenateElectionResults(BaseResults):
    """ Records relevant results about an election.

    This class is a minimal implementation of :class:`dividebatur.results.BaseResults` abstraction. It simply tracks
    which candidates were elected in a given contest. Almost all methods are stubs of the base class.
    """
    def __init__(self):
        """ Initializes a :class:`RealSenateElectionResults` object. """
        self._candidates_elected = []

    def get_elected_candidates(self):
        """ Returns the IDs of the candidates elected during the election.

        :returns: The IDs of the candidates elected during the election.
        :rtype: list
        """ 
        return self._candidates_elected

    def round_begin(self, round_number):
        pass

    def round_complete(self):
        pass

    def exclusion_distribution_performed(self, obj):
        pass

    def election_distribution_performed(self, obj):
        pass

    def candidate_aggregates(self, obj):
        pass

    def candidate_elected(self, obj):
        """ Adds elected candidate to list of candidates elected thus far.

        Called whenever a candidate is elected. :param:`obj` is an instance of
        :class:`dividebatur.results.CandidateElected` which has a `candidate_id` attribute.
        """
        self._candidates_elected.append(obj.candidate_id)

    def candidates_excluded(self, obj):
        pass

    def provision_used(self, obj):
        pass

    def started(self, vacancies, total_papers, quota):
        pass

    def finished(self):
        pass
