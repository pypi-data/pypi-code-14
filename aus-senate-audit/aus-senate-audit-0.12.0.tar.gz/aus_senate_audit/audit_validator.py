# -*- coding: utf-8 -*-

""" Validates Paper Preferences Against Electronic Preferences. """

from aus_senate_audit.audit_recorder import AuditRecorder


class AuditValidator(object):
    """ Validates paper preferences against electronic preferences.

    :ivar str _path_to_selected_ballots_file: The path to the selected ballots file.
    :ivar :class:`AuditRecorder` _audit_recorder: An object for interfacing with information stored about the audit's
        progress thus far.
    """
    def __init__(self, path_to_selected_ballots_file, audit_recorder):
        """ Initializes a :class:`AuditValidator` object.

        :param str path_to_selected_ballots_file: The path to the file containing completed, selected ballots.
        :param :class:`AuditRecorder` audit_recorder: An object for interfacing with information stored about the
            audit's progress thus far.
        """
        self._path_to_selected_ballots_file = path_to_selected_ballots_file
        self._audit_recorder = audit_recorder

    @staticmethod
    def get_preferences_from_ballot(ballot):
        """ Returns the preferences for the given ballot.

        :param str ballot: The ballot whose preferences will be returned.

        :return: The preferences for the given ballot.
        :rtype: str
        """
        return ballot.split('"')[1]

    def get_paper_ballots(self):
        """ Returns the paper ballots recorded in the selected ballots file.

        :returns: The paper ballots recorded in the selected ballots file.
        :rtype: list
        """
        with open(self._path_to_selected_ballots_file, 'r') as f:
            f.readline()  # Skip the header.
            return [line.rstrip() for line in f]

    def get_electronic_ballots(self):
        """ Returns the electronic ballots recorded in the current audit round file.

        :returns: The electronic ballots recorded in the current audit round file.
        :rtype: list
        """
        audit_round_file_name = self._audit_recorder.get_current_audit_round_file_name()
        with open(audit_round_file_name, 'r') as f:
            f.readline()  # Skip the header.
            return [line.rstrip() for line in f]

    def compare(self):
        """ Compares the paper preferences against the electronic preferences.

        In addition, records the result of the comparison in the current audit round file and adds the new ballots to
        the file containing all ballots for the given sample.
        """
        paper_ballots = self.get_paper_ballots()
        electronic_ballots = self.get_electronic_ballots()
        match_records = []
        for paper_ballot, electronic_ballot in zip(paper_ballots, electronic_ballots):
            match = int(paper_ballot == electronic_ballot)
            match_records.append(electronic_ballot + ',{},"{}"\n'.format(
                match,
                AuditValidator.get_preferences_from_ballot(paper_ballot))
            )
        self._audit_recorder.record_current_audit_round_match_records(match_records)
        self._audit_recorder.add_new_ballots_to_aggregate(self._path_to_selected_ballots_file)
