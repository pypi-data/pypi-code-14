# -*- coding: utf-8 -*-

""" Default Constants Used for the Australian Senate Election Audit. """


# The modes in which to run the senate election audit.
SIMULATION_MODE = 'simulation'
QUICK_MODE = 'quick'
REAL_MODE = 'real'

# The Australian states with senate election data available to audit.
STATES = [
    'ACT',
    'NSW',
    'NT',
    'QLD',
    'SA',
    'TAS',
    'VIC',
    'WA',
]

# The default number of cast ballots in a simulated senate election audit.
DEFAULT_SIMULATED_SENATE_ELECTION_NUM_BALLOTS = 1000000

# The default number of candidates in a simulated senate election audit.
DEFAULT_SIMULATED_SENATE_ELECTION_NUM_CANDIDATES = 100

# The default upper bound on the fraction of trials a candidate must lose in a round of an audit to be considered
# unpopular.
DEFAULT_UNPOPULAR_FREQUENCY_THRESHOLD = 0.03

# The default number of ballots to add to a growing sample at the start of an audit stage.
DEFAULT_SAMPLE_INCREMENT_SIZE = 1500

# The default random number seed value.
DEFAULT_SEED_VALUE = 1

# The number of header lines in a formal preferences CSV file.
FORMAL_PREFERENCES_CSV_NUM_HEADER_LINES = 2

# The keys of the audit configuration JSON.
AUDIT_STAGE_KEY = 'audit_stage'
SAMPLE_SIZE_KEY = 'sample_size'

# The default file name for the election configuration file.
CONFIG_FILE_PATH = 'aec_fed2016.json'

# The names of files created by the aus-senate-audit software.
AUDIT_DIR_NAME = 'audit_{}'
ROUND_DIR_NAME = 'rounds'
AUDIT_INFO_FILE_NAME = 'info.json'
AUDIT_ROUND_FILE_NAME = '{}/round_{}.csv'
AGGREGATE_BALLOTS_FILE_NAME = 'aggregate.csv'
SELECTED_BALLOTS_FILE_NAME = 'selected_ballots.csv'

# The column headers of a formal preferences file (first header line).
COLUMN_HEADERS = [
    'ElectorateNm',
    'VoteCollectionPointNm',
    'VoteCollectionPointId',
    'BatchNo',
    'PaperNo',
    'Preferences',
]

# The column header delimiters of a formal preferences file (second header line).
COLUMN_HEADER_DELIMS = [
    '------------',
    '---------------------',
    '---------------------',
    '-------',
    '-------',
    '-----------',
]

# The column headers used to track preference matches between electronic ballots and paper ballot interpretations.
MATCH_HEADERS = [
    'Match',
    'PreferencesAfterAudit',
]
