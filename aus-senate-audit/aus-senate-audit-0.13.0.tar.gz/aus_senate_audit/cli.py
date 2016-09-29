# -*- coding: utf-8 -*-

""" Encapsulates a Utility Function for Creating the CLI. """

from argparse import ArgumentParser

from aus_senate_audit.constants import DEFAULT_SAMPLE_INCREMENT_SIZE
from aus_senate_audit.constants import DEFAULT_SEED_VALUE
from aus_senate_audit.constants import DEFAULT_SIMULATED_SENATE_ELECTION_NUM_BALLOTS
from aus_senate_audit.constants import DEFAULT_SIMULATED_SENATE_ELECTION_NUM_CANDIDATES
from aus_senate_audit.constants import DEFAULT_UNPOPULAR_FREQUENCY_THRESHOLD
from aus_senate_audit.constants import QUICK_MODE
from aus_senate_audit.constants import REAL_MODE
from aus_senate_audit.constants import SIMULATION_MODE
from aus_senate_audit.constants import STATES


def parse_command_line_args():
    """ Parses the command line arguments for running an audit. """
    parser = ArgumentParser()
    parser.add_argument(
        'mode',
        type=str,
        metavar='MODE',
        choices=[QUICK_MODE, REAL_MODE, SIMULATION_MODE],
        help='The mode in which to run the audit.',
    )
    parser.add_argument(
        '-s',
        '--seed',
        type=int,
        default=DEFAULT_SEED_VALUE,
        help='The starting value of the random number generator.',
    )
    parser.add_argument(
        '--num-ballots',
        type=int,
        default=DEFAULT_SIMULATED_SENATE_ELECTION_NUM_BALLOTS,
        help='The number of ballots cast for a simulated senate election.',
    )
    parser.add_argument(
        '--num-candidates',
        type=int,
        default=DEFAULT_SIMULATED_SENATE_ELECTION_NUM_CANDIDATES,
        help='The number of candidates for a simulated senate election.',
    )
    parser.add_argument(
        '--state',
        type=str,
        choices=STATES,
        help='The abbreviation of the state name to run the senate election audit for.',
    )
    parser.add_argument(
        '--selected-ballots',
        type=str,
        help='The path to the CSV file containing the selected ballots data.',
    )
    parser.add_argument(
        '--data',
        type=str,
        help='The path to all Australian senate election data.',
    )
    parser.add_argument(
        '--max-ballots',
        type=int,
        help='The maximum number of ballots to check for a real senate election audit.',
    )
    parser.add_argument(
        '-f',
        '--unpopular-frequency-threshold',
        type=float,
        default=DEFAULT_UNPOPULAR_FREQUENCY_THRESHOLD,
        help='The minimum frequency of trials in a single audit stage a candidate must be elected in order for the \
        candidate to be deemed unpopular (only applied on the last audit stage).',
    )
    parser.add_argument(
        '--sample-increment-size',
        type=int,
        default=DEFAULT_SAMPLE_INCREMENT_SIZE,
        help='The number of ballots to add to the growing sample during this audit stage.',
    )
    return parser.parse_args()
