# -*- coding: utf-8 -*-

""" Implements a Class for Reading the Australian Senate Election Configuration File. """

from json import load

from aus_senate_audit.constants import CONFIG_FILE_PATH
from aus_senate_audit.constants import FORMAL_PREFERENCES_CSV_NUM_HEADER_LINES


class ConfigReader(object):
    """ Implements a class for reading the Australian senate election configuration file.

    :ivar str _data_file_path: The path to all Australian senate election data.
    :ivar dict _config: The Australian senate election configuration.

    NOTE: The configuration file is in a JSON format.
    """
    def __init__(self, data_file_path):
        """ Initializes a :class:`ConfigReader` object.

        :param str data_file_path: The path to all Australian senate election data.
        """
        self._data_file_path = data_file_path
        self._config = load(open('{}/{}'.format(data_file_path, CONFIG_FILE_PATH), 'r'))

    def get_config(self):
        """ Returns the configuration for the senate election.

        :returns: The configuration for the senate election.
        :rtype: dict
        """
        return self._config

    def get_all_ballots_for_state(self, state):
        """ Returns all cast ballots for the given state.

        :param str state: The abbreviated name of the state to retrieve all cast ballots for.

        :returns: All cast ballots for the given state.
        :rtype: list
        """
        for state_config in self._config['count']:
            if state_config['name'] == state:
                path_to_formal_preferences = state_config['aec-data']['formal-preferences']
                with open('{}/{}'.format(self._data_file_path, path_to_formal_preferences), 'r') as f:
                    return [line.rstrip() for line in f][FORMAL_PREFERENCES_CSV_NUM_HEADER_LINES:]
