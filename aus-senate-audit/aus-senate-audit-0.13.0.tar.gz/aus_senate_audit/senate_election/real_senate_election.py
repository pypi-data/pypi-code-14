# -*- coding: utf-8 -*-

""" Implements a Class for Representing a Real Senate Election. """

import dividebatur.counter as cnt
import dividebatur.senatecount as sc

from aus_senate_audit.audit_recorder import AuditRecorder
from aus_senate_audit.audit_tie_breaker import AuditTieBreaker
from aus_senate_audit.config_reader import ConfigReader
from aus_senate_audit.constants import AGGREGATE_BALLOTS_FILE_NAME
from aus_senate_audit.constants import FORMAL_PREFERENCES_CSV_NUM_HEADER_LINES
from aus_senate_audit.senate_election.base_senate_election import BaseSenateElection
from aus_senate_audit.senate_election.real_senate_election_results import RealSenateElectionResults


class RealSenateElection(BaseSenateElection):
    """ Implements a class for representing a real senate election. """
    TYPE = 'Real'

    def __init__(self, seed, state, data_file_path, max_ballots=None):
        """ Initializes a :class:`RealSenateElection` object.

        :param int seed: The starting value for the random number generator.
        :param str state: The abbreviated name of the state whose senate election is being audited.
        :param str data_file_path: The path to all Australian senate election data.
        :param int max_ballots: The maximum number of ballots to check when performing the senate election audit
            (default: None).
        """
        super(RealSenateElection, self).__init__()
        # Read the configuration file for the election data.
        election_config = ConfigReader(data_file_path).get_config()
        self._election_id = election_config['title']
        for contest in election_config['count']:
            if contest['name'] == state:
                contest_config = contest
        self._seats = contest_config['vacancies']

        try:
            # Remove this key to suppress verification checks which would
            # not be valid for a subsample of the ballots from the contest.
            del contest_config['verified']
        except KeyError:
            pass

        # Get the social choice function.
        input_cls = sc.get_input_method(contest_config['aec-data']['format'])

        data_options = {}  # Passed when getting data from :mod:`dividebatur`.
        if max_ballots is not None:
            data_options['max_ballots'] = max_ballots

        path_to_formal_preferences_file = '{}/{}'.format(
            data_file_path,
            contest_config['aec-data']['formal-preferences'],
        )
        total_num_lines = sum(1 for _ in open(path_to_formal_preferences_file, 'r'))
        self._n = total_num_lines - FORMAL_PREFERENCES_CSV_NUM_HEADER_LINES
        contest_config['aec-data']['senate-candidates'] \
            = '{}/{}'.format(data_file_path, contest_config['aec-data']['senate-candidates'])
        contest_config['aec-data']['all-candidates'] \
            = '{}/{}'.format(data_file_path, contest_config['aec-data']['all-candidates'])
        contest_config['aec-data']['formal-preferences'] = AuditRecorder(state).get_file_path(
            AGGREGATE_BALLOTS_FILE_NAME,
        )

        # Get election data.
        self._data = sc.get_data(input_cls, '', contest_config, **data_options)

        # Build remaining ticket data structure from tickets and randomly shuffle for sampling.
        for ticket, weight in sorted(self._data.tickets_for_count):
            self.add_ballot(ticket, weight)

        # Get candidate data.
        self._candidate_ids = self._data.get_candidate_ids()
        self._candidates = self._data.candidates.candidates

        # Initialize AuditTieBreaker with tie-breaking information from the contest.
        self._tie_breaker = AuditTieBreaker(self._candidate_ids, seed=seed)
        self._tie_breaker.load_events(
            contest_config['election_order_ties'],
            contest_config['election_ties'],
            contest_config['exclusion_ties'],
        )

    def draw_ballots(self):
        """ Real senate election audit does not draw ballots through this interface. """
        pass

    def get_outcome(self, ballot_weights):
        """ Returns the outcome of a senate election with the given ballot weights.

        :param :class:`Counter` ballot_weights: A mapping from a ballot type to the number of ballots drawn of that
            type.

        :returns: The IDs of the candidates elected to the available seats, sorted in lexicographical order.
        :rtype: tuple
        """
        # Reset tickets for count.
        self._data.tickets_for_count = sc.PapersForCount()
        for ballot, weight in ballot_weights.items():
            self._data.tickets_for_count.add_ticket(tuple(ballot), weight)

        # Set up and run counter.
        results = RealSenateElectionResults()
        _ = cnt.SenateCounter(
            results,
            self._seats,
            self._data.tickets_for_count,
            self._tie_breaker.break_election_order_tie,
            self._tie_breaker.break_exclusion_tie,
            self._tie_breaker.break_election_tie,
            self._data.get_candidate_ids(),
            self._data.get_candidate_order,
            disable_bulk_exclusions=True,
        ).run()

        return tuple(sorted(results.get_elected_candidates()))
