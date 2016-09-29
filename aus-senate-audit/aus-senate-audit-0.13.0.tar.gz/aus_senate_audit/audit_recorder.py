# -*- coding: utf-8 -*-

""" Encapsulates Utilities for Interacting with Information about the Audit's Progress thus far. """

from json import load
from json import dumps
from os import makedirs
from os.path import exists

from aus_senate_audit.constants import AGGREGATE_BALLOTS_FILE_NAME
from aus_senate_audit.constants import AUDIT_DIR_NAME
from aus_senate_audit.constants import AUDIT_INFO_FILE_NAME
from aus_senate_audit.constants import AUDIT_ROUND_FILE_NAME
from aus_senate_audit.constants import COLUMN_HEADERS
from aus_senate_audit.constants import COLUMN_HEADER_DELIMS
from aus_senate_audit.constants import MATCH_HEADERS
from aus_senate_audit.constants import ROUND_DIR_NAME
from aus_senate_audit.constants import SELECTED_BALLOTS_FILE_NAME
from aus_senate_audit.constants import AUDIT_STAGE_KEY
from aus_senate_audit.constants import SAMPLE_SIZE_KEY


class AuditRecorder(object):
    """ Encapsulates utilities for interacting with information about the audit's progress thus far.

    :ivar str state: The abbreviated name of the state whose senate election is being audited.
    :ivar str audit_dir_name: The name of the directory storing all audit results.
    """
    def __init__(self, state, audit_dir_name=AUDIT_DIR_NAME):
        """ Initializes an :class:`AuditRecorder` object.

        :param str state: The abbreviated name of the state whose senate election is being audited.
        :param str audit_dir_name: The name of the directory storing all audit results (default: 'audit_{}').
        """
        self._state = state
        self.audit_dir_name = audit_dir_name
        if not exists(self.get_audit_dir_name()):
            makedirs('{}/{}'.format(self.get_audit_dir_name(), ROUND_DIR_NAME))
            self.record_audit_info(0, 0)
            self._initialize_aggregate_ballots_file()

    @staticmethod
    def remove_preferences_from_ballot(ballot):
        """ Returns the given ballot minus the formal preferences recorded by the ballot.

        :param str ballot: The ballot whose formal preferences are to be removed.

        :returns: The given ballot minus the formal preferences recorded by the ballot.
        :rtype: str
        """
        return ballot.split('"')[0]  # Works because the preferences column is wrapped in quotation marks.

    def get_audit_dir_name(self):
        """ Returns the audit directory name for the given state.

        :returns: The audit directory name for the given state.
        :rtype: str
        """
        return self.audit_dir_name.format(self._state)

    def get_file_path(self, file_name):
        """ Returns the file path for the given file name within the audit directory.

        :param str file_name: The name of the file for which the full path should be returned.

        :returns: The file path for the given file name within the audit directory.
        :rtype: str
        """
        return '{}/{}'.format(self.get_audit_dir_name(), file_name)

    def _initialize_aggregate_ballots_file(self):
        """ Initializes the aggregate ballots file with the appropriate headers. """
        with open(self.get_file_path(AGGREGATE_BALLOTS_FILE_NAME), 'w') as f:
            f.write('{}\n{}\n'.format(','.join(COLUMN_HEADERS), ','.join(COLUMN_HEADER_DELIMS)))

    def add_new_ballots_to_aggregate(self, path_to_selected_ballots_file):
        """ Adds the completed selected ballots to the aggregate ballots file.

        :param str path_to_selected_ballots_file: The path to the selected ballots file.
        """
        with open(self.get_file_path(AGGREGATE_BALLOTS_FILE_NAME), 'a') as f:
            with open(path_to_selected_ballots_file, 'r') as selected_ballots_file:
                selected_ballots_file.readline()  # Skip the header.
                new_ballots = [line for line in selected_ballots_file]
                for new_ballot in new_ballots:
                    f.write(new_ballot)

    def record_audit_info(self, audit_stage, sample_size):
        """ Sets information about the audit recorded thus far.

        :param int audit_stage: The new stage of the audit.
        :param int sample_size: The sample size of the audit.
        """
        open(self.get_file_path(AUDIT_INFO_FILE_NAME), 'w').write(
            dumps({AUDIT_STAGE_KEY: audit_stage, SAMPLE_SIZE_KEY: sample_size})
        )

    def get_audit_info(self):
        """ Returns information about the audit recorded thus far.

        Example of the audit information.

        .. code-block:: python

            {
                'audit_stage': 1,
                'sample_size': 1200,

            }

        :returns: A dictionary containing information about the audit recorded thus far.
        :rtype: dict
        """
        return load(open(self.get_file_path(AUDIT_INFO_FILE_NAME), 'r'))

    def get_current_audit_stage(self):
        """ Returns the current stage of the audit.

        :returns: The current stage of the audit.
        :rtype: int
        """
        return self.get_audit_info()[AUDIT_STAGE_KEY]

    def get_current_sample_size(self):
        """ Returns the number of ballots in the sample used by the audit thus far.

        :returns: The number of ballots in the sample used by the audit thus far.
        :rtype: int
        """
        return self.get_audit_info()[SAMPLE_SIZE_KEY]

    def record_selected_ballots(self, audit_stage, sample, quick):
        """ Writes the given sample of ballots to the appropriate selected ballots and round file.

        :param int audit_stage: The current stage of the audit.
        :param list sample: A list of ballots from the most recently drawn increment sample.
        :param boolean quick: A flag indicating whether the audit is manual (`quick` is False) or not manual.
        """
        # Write the new ballots in the sample to the selected ballots file, without specifying the original preferences.
        with open(SELECTED_BALLOTS_FILE_NAME, 'w') as f:
            f.write('{}\n'.format(','.join(COLUMN_HEADERS)))
            f.write(
                '\n'.join(
                    [ballot if quick else self.remove_preferences_from_ballot(ballot) for ballot in sample]
                ) + '\n'
            )
        # Write the new ballots in the sample to the audit round file.
        with open(self.get_file_path(AUDIT_ROUND_FILE_NAME.format(ROUND_DIR_NAME, audit_stage)), 'w') as f:
            f.write('{}\n'.format(','.join(COLUMN_HEADERS + MATCH_HEADERS)))
            f.write('\n'.join([ballot for ballot in sample]) + '\n')

    def record_current_audit_round_match_records(self, match_records):
        """ Writes the given match records to the current audit round file.

        :param list match_records: The match records to write to the current audit round file.
        """
        audit_round_file_name = self.get_file_path(AUDIT_ROUND_FILE_NAME.format(
            ROUND_DIR_NAME,
            self.get_current_audit_stage(),
        ))
        with open(audit_round_file_name, 'w') as f:
            f.write('{}\n'.format(','.join(COLUMN_HEADERS + MATCH_HEADERS)))
            f.write('\n'.join([match_record for match_record in match_records]))

    def get_current_audit_round_file_name(self):
        """ Returns the path to the current round file for the audit.

        :returns: The path to the current round file for the audit.
        :rtype: str
        """
        return self.get_file_path(AUDIT_ROUND_FILE_NAME.format(ROUND_DIR_NAME, self.get_audit_info()[AUDIT_STAGE_KEY]))
